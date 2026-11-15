#!/usr/bin/env python3
"""Trusted-main workflow_run dispatcher: PR bytes execute only in Oracle sandbox.

The persistent runner downloads bounded regular Git blobs, invokes the installed
queue client, then uses trusted-main verifier code to inspect returned evidence.
It never imports, runs or checks out PR code on the persistent runner.
"""
import argparse
import base64
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request

REPOSITORY='sloik/post-ai-worlds'
REPOSITORY_ID=1448630173
SOURCE_WORKFLOW='.github/workflows/checks.yml'
SOURCE_NAME='Public research checks'
DISPATCH_WORKFLOW=REPOSITORY+'/.github/workflows/oracle-pr-tla.yml@refs/heads/main'
CHECK_NAME='validate'
TRUSTED_ROOT=Path(__file__).resolve().parents[1]
SHA=re.compile('[0-9a-f]{40}')
MAX_BLOB=8*1024*1024
MAX_SOURCE=64*1024*1024
MAX_FILES=20000
REQUIRED={'tools/check.py','tools/run_models.py','tools/remote_models.py','tools/campaign.py','worlds/registry.json'}
SOURCE_RECEIPT='.oracle-source.json'
RESULT_RECEIPT='.oracle-result.json'
PHASES=['git_index','ordinary','unittest','navigation','website_build','website_diff']
BOOTSTRAP="import json,os,pathlib,shutil,subprocess,sys,tempfile,time\nroot=pathlib.Path.cwd()\nsource=json.loads((root/'.oracle-source.json').read_text())\nassert source['schema_version']==1 and isinstance(source['tracked_files'],list)\ntracked=list(source['tracked_files'])\nassert tracked and len(set(tracked))==len(tracked)\nassert all(isinstance(x,str) and not x.startswith('/') and all(p not in ('','.','..') for p in x.split('/')) for x in tracked)\nreport={'native_authority':'separate immutable queue job; diagnostic report only','schema_version':1,'source_head':source['source_head'],'source_run_id':source['source_run_id'],'source_kind':source['source_kind'],'execution':source['execution'],'complete':False,'phases':[]}\nenv=dict(os.environ)\nenv.update(PYTHONDONTWRITEBYTECODE='1',GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_SYSTEM='/dev/null',GIT_CONFIG_GLOBAL='/dev/null',GIT_CONFIG_COUNT='0',GIT_TERMINAL_PROMPT='0')\nfor k in ('GIT_DIR','GIT_WORK_TREE','GIT_INDEX_FILE','GIT_OBJECT_DIRECTORY','GIT_ALTERNATE_OBJECT_DIRECTORIES'):\n    env.pop(k,None)\ndef phase(name,argv):\n    start=time.time()\n    print('ORACLE_PHASE_START '+name,flush=True)\n    child=subprocess.run(argv,cwd=root,env=env)\n    report['phases'].append({'name':name,'argv':argv,'exit_code':child.returncode,'started':start,'finished':time.time()})\n    print('ORACLE_PHASE_END '+name+' '+str(child.returncode),flush=True)\n    if child.returncode:raise SystemExit(child.returncode)\ntry:\n    # No commit or fabricated HEAD: only an index for tracked-document discovery.\n    # Git metadata lives in a fresh private directory after candidate execution;\n    # no hooks/templates/global/system config or Git network can be inherited.\n    git=root/'.git'\n    if git.is_symlink() or git.is_file():git.unlink()\n    elif git.exists():shutil.rmtree(git)\n    gitdir=pathlib.Path(tempfile.mkdtemp(prefix='.oracle-git-',dir=root))\n    template=pathlib.Path(tempfile.mkdtemp(prefix='.oracle-template-',dir=root))\n    env['GIT_TEMPLATE_DIR']=str(template)\n    prefix=['git','--literal-pathspecs','-c','core.hooksPath=/dev/null','-c','core.fsmonitor=false','-c','protocol.allow=never','--git-dir='+str(gitdir),'--work-tree='+str(root)]\n    subprocess.run(prefix+['init','--template=','--quiet'],check=True,env=env)\n    git.write_text('gitdir: '+str(gitdir)+'\\n')\n    subprocess.run(prefix+['add','--force','--pathspec-from-file=-','--pathspec-file-nul'],input=b'\\0'.join(x.encode() for x in tracked)+b'\\0',check=True,env=env)\n    report['phases'].append({'name':'git_index','argv':['trusted-bootstrap:validated-tracked-index'],'exit_code':0})\n    phase('ordinary',[sys.executable,'-B','tools/check.py'])\n    phase('unittest',[sys.executable,'-B','-m','unittest','discover','-s','tests','-v'])\n    phase('navigation',[sys.executable,'-B','tools/build_navigation.py'])\n    phase('website_build',[sys.executable,'-B','website/build.py'])\n    phase('website_diff',['git','-c','core.hooksPath=/dev/null','-c','protocol.allow=never','diff','--exit-code','--','website'])\n    report['complete']=True\nfinally:\n    output=root/'.oracle-result.json'\n    with output.open('w') as f:\n        json.dump(report,f,sort_keys=True);f.flush();os.fsync(f.fileno())\n"


class Refused(ValueError):pass


def require(value,message):
    if not value:raise Refused(message)


def integer(value):
    return type(value) is int and value>0


def environment_integer(env,name):
    value=env.get(name)
    require(isinstance(value,str) and re.fullmatch('[1-9][0-9]{0,19}',value),'invalid '+name)
    return int(value)


def execution_context(env,run,kind):
    require(integer(run.get('id')) and integer(run.get('run_attempt')),'invalid source execution attempt')
    require(isinstance(run.get('head_sha'),str) and SHA.fullmatch(run['head_sha']),'invalid execution head')
    require(kind in ('manual','workflow_run:push','workflow_run:pull_request'),'invalid execution kind')
    workflow_sha=env.get('GITHUB_WORKFLOW_SHA')
    require(isinstance(workflow_sha,str) and SHA.fullmatch(workflow_sha) and workflow_sha!='0'*40,'invalid dispatcher workflow SHA')
    workflow_ref=env.get('GITHUB_WORKFLOW_REF')
    expected=REPOSITORY+'/.github/workflows/oracle-tla.yml@refs/heads/main' if kind=='manual' else DISPATCH_WORKFLOW
    require(workflow_ref==expected,'execution dispatcher workflow mismatch')
    return {'schema_version':1,'repository':REPOSITORY,'source_head':run['head_sha'],
            'source_run_id':run['id'],'source_run_attempt':run['run_attempt'],'source_kind':kind,
            'dispatcher_run_id':environment_integer(env,'GITHUB_RUN_ID'),
            'dispatcher_run_attempt':environment_integer(env,'GITHUB_RUN_ATTEMPT'),
            'dispatcher_workflow_ref':workflow_ref,'dispatcher_workflow_sha':workflow_sha}


def execution_key(phase,execution):
    require(phase in ('native','tests','check'),'invalid execution phase')
    encoded=json.dumps(execution,sort_keys=True,separators=(',',':')).encode()
    return 'post-ai-'+phase+'-'+hashlib.sha256(encoded).hexdigest()


def attempt_path(run_id,attempt):
    require(integer(run_id) and integer(attempt),'invalid workflow attempt identity')
    return '/repos/'+REPOSITORY+'/actions/runs/'+str(run_id)+'/attempts/'+str(attempt)


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        raise Refused('GitHub API redirect refused')


class API:
    def __init__(self,token):
        require(bool(token),'GitHub token required for trusted check publication')
        self.token=token
        self.opener=urllib.request.build_opener(NoRedirect)

    def call(self,path,method='GET',body=None):
        require(path.startswith('/repos/'+REPOSITORY+'/'),'API path outside owning repository')
        request=urllib.request.Request('https://api.github.com'+path,
            data=None if body is None else json.dumps(body).encode(),method=method,
            headers={'Authorization':'Bearer '+self.token,'Accept':'application/vnd.github+json',
                     'X-GitHub-Api-Version':'2022-11-28','User-Agent':'post-ai-oracle-dispatcher'})
        with self.opener.open(request,timeout=60) as response:
            raw=response.read(16*1024*1024+1)
        require(len(raw)<=16*1024*1024,'GitHub API response exceeds cap')
        return json.loads(raw)


def validate_event(event,env):
    require(env.get('GITHUB_SERVER_URL')=='https://github.com','wrong GitHub server')
    require(env.get('GITHUB_REPOSITORY')==REPOSITORY,'wrong repository context')
    require(env.get('GITHUB_EVENT_NAME')=='workflow_run','workflow_run required')
    require(env.get('GITHUB_REF')=='refs/heads/main','dispatcher must be maintained main')
    require(env.get('GITHUB_WORKFLOW_REF')==DISPATCH_WORKFLOW,'wrong trusted dispatcher workflow')
    require(event.get('action')=='completed','upstream run must complete first')
    repo=event.get('repository',{})
    require(type(repo.get('id')) is int and repo['id']==REPOSITORY_ID and repo.get('full_name')==REPOSITORY and repo.get('fork') is False,'wrong repository identity')
    run=event.get('workflow_run',{})
    require(integer(run.get('id')),'invalid source run ID')
    require(integer(run.get('run_attempt')),'invalid source run attempt')
    require(run.get('name')==SOURCE_NAME and run.get('event') in ('pull_request','push'),'not an approved source workflow')
    require(run.get('status')=='completed','upstream run incomplete')
    require(isinstance(run.get('head_sha'),str) and SHA.fullmatch(run['head_sha']),'invalid exact source SHA')
    return run


def source_run(api,event_run):
    run=api.call(attempt_path(event_run['id'],event_run['run_attempt']))
    require(integer(run.get('id')) and integer(run.get('run_attempt')),'invalid API source attempt')
    for name in ('id','run_attempt','head_sha','head_branch','event','status','conclusion','workflow_id'):
        require(run.get(name)==event_run.get(name),'event/API source-run mismatch: '+name)
    require(run.get('name')==SOURCE_NAME and run.get('event') in ('pull_request','push') and run.get('status')=='completed','wrong source run')
    repo=run.get('repository',{})
    require(type(repo.get('id')) is int and repo['id']==REPOSITORY_ID and repo.get('full_name')==REPOSITORY,'source run belongs to another repository')
    require(integer(run.get('workflow_id')),'invalid source workflow ID')
    workflow=api.call('/repos/'+REPOSITORY+'/actions/workflows/'+str(run['workflow_id']))
    require(workflow.get('path')==SOURCE_WORKFLOW,'source workflow path mismatch')
    return run


def current_prs(api,run):
    prs=api.call('/repos/'+REPOSITORY+'/commits/'+run['head_sha']+'/pulls?per_page=100')
    require(isinstance(prs,list) and len(prs)<100,'PR association unavailable/truncated')
    found=[]
    for pr in prs:
        head=pr.get('head',{});base=pr.get('base',{}).get('repo',{})
        if (pr.get('state')=='open' and head.get('sha')==run['head_sha']
                and base.get('id')==REPOSITORY_ID and base.get('full_name')==REPOSITORY):
            require(integer(pr.get('number')),'invalid associated PR number')
            found.append(pr)
    require(found,'no open PR at the exact approved source head')
    return found


def source_path(path):
    require(isinstance(path,str) and 0<len(path)<=1024 and '\\' not in path and not any(ord(x)<32 for x in path),'invalid Git path')
    p=PurePosixPath(path)
    require(not p.is_absolute() and all(x not in ('','.','..') for x in path.split('/')),'Git path escape')
    return path


def snapshot(api,head,destination):
    require(isinstance(head,str) and SHA.fullmatch(head),'invalid snapshot head')
    commit=api.call('/repos/'+REPOSITORY+'/git/commits/'+head)
    require(commit.get('sha')==head,'commit identity mismatch')
    tree_sha=commit.get('tree',{}).get('sha')
    require(isinstance(tree_sha,str) and SHA.fullmatch(tree_sha),'invalid tree identity')
    tree=api.call('/repos/'+REPOSITORY+'/git/trees/'+tree_sha+'?recursive=1')
    require(tree.get('sha')==tree_sha and tree.get('truncated') is False,'tree identity/truncation failure')
    selected={};tracked=[];total=0
    for entry in tree.get('tree',[]):
        path=source_path(entry.get('path'))
        if entry.get('type')=='tree':continue
        require(path not in (SOURCE_RECEIPT,RESULT_RECEIPT) and '.git' not in PurePosixPath(path).parts and not path.startswith(('.oracle-git-','.oracle-template-')),'reserved source path')
        require(entry.get('type')=='blob' and entry.get('mode') in ('100644','100755'),'non-regular PR source refused: '+path)
        require(path not in selected,'duplicate PR source')
        require(type(entry.get('size')) is int and 0<=entry['size']<=MAX_BLOB,'PR source size exceeds cap')
        require(isinstance(entry.get('sha'),str) and SHA.fullmatch(entry['sha']),'invalid blob identity')
        total+=entry['size'];require(total<=MAX_SOURCE and len(selected)<MAX_FILES,'PR source closure exceeds cap')
        selected[path]=entry
        tracked.append(path)
    require(REQUIRED<=set(selected),'missing native producer inputs')
    require(not any('/'.join(p.split('/')[:i]) in selected for p in selected for i in range(1,len(p.split('/')))),'conflicting source paths')
    destination.mkdir(mode=0o700)
    for path,entry in sorted(selected.items()):
        if path.startswith('formal/evidence/'):
            continue
        blob=api.call('/repos/'+REPOSITORY+'/git/blobs/'+entry['sha'])
        require(blob.get('encoding')=='base64' and blob.get('sha')==entry['sha'],'blob envelope mismatch')
        try:data=base64.b64decode(''.join(blob['content'].split()),validate=True)
        except (ValueError,TypeError,KeyError) as exc:raise Refused('invalid blob encoding') from exc
        require(len(data)==entry['size'],'blob size mismatch')
        digest=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        require(digest==entry['sha'],'blob content hash mismatch')
        target=destination/path;target.parent.mkdir(parents=True,exist_ok=True)
        fd=os.open(target,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o755 if entry['mode']=='100755' else 0o644)
        with os.fdopen(fd,'wb') as f:f.write(data)
    return {'files':selected,'tracked_files':sorted(tracked)}


def trusted_modules():
    # Only maintained-main modules from this checkout are imported. PR paths are
    # never cwd/sys.path/module names, including during evidence verification.
    tools=TRUSTED_ROOT/'tools'
    sys.path.insert(0,str(tools))
    import check
    import campaign
    import remote_models
    for module in (check,campaign,remote_models):
        require(Path(module.__file__).resolve().parent==tools.resolve(),'untrusted verifier import refused')
    return check,campaign,remote_models


def verify_returned(snapshot_root,fetched):
    checker,campaign,adapter=trusted_modules()
    adapter.merge_evidence(fetched,snapshot_root,campaign.RUNS)
    checker.check_registry(checker.load(snapshot_root/'worlds/registry.json'))
    for run_id, _, _, _ in campaign.RUNS:
        text=(snapshot_root/'formal/evidence'/(run_id+'.log')).read_text()
        require('/Users/' not in text and '/home/' not in text,'private native path in returned capture')
    manifest=checker.load(snapshot_root/'formal/evidence/manifest.json')
    java=Path('/usr/bin/java').resolve()
    require(manifest.get('java_executable')==str(java),'returned JDK executable identity mismatch')
    require(manifest.get('java_sha256')==checker.digest(java),'returned JDK binary identity mismatch')
    return checker.verify_evidence(snapshot_root)


def write_source_receipt(source,head,run_id,kind,tracked_files,execution,role='candidate-tests'):
    require(isinstance(head,str) and SHA.fullmatch(head),'invalid source receipt head')
    require(integer(run_id),'invalid source receipt run')
    require(execution.get('source_head')==head and execution.get('source_run_id')==run_id
            and execution.get('source_kind')==kind and integer(execution.get('source_run_attempt'))
            and integer(execution.get('dispatcher_run_id')) and integer(execution.get('dispatcher_run_attempt')),
            'source receipt execution binding mismatch')
    require(role in ('candidate-tests','trusted-native'),'invalid bundle role')
    names=sorted(source_path(x) for x in tracked_files)
    require(len(names)==len(set(names)),'duplicate tracked source')
    (source/SOURCE_RECEIPT).write_text(json.dumps({'schema_version':1,'source_head':head,'source_run_id':run_id,
        'source_kind':kind,'tracked_files':names,'execution':execution,'bundle_role':role},sort_keys=True))


def prepare_native(candidate,destination):
    checker,campaign,adapter=trusted_modules()
    producers=['tools/check.py','tools/run_models.py','tools/remote_models.py','tools/campaign.py']
    for path in producers:
        require(checker.digest(candidate/path)==checker.digest(TRUSTED_ROOT/path),'unsupported producer/campaign change; reviewed maintained-baseline update required: '+path)
    data={'worlds/registry.json'}
    for run_id,model,_,_ in campaign.RUNS:
        data.update('formal/'+name for name in campaign.DEPENDENCIES[model]);data.add('formal/'+run_id+'.cfg')
    destination.mkdir()
    for path in producers:
        raw=(TRUSTED_ROOT/path).read_bytes()
        for folder in ('producer','subject'):
            target=destination/folder/path;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)
    adapter.snapshot_inputs(candidate,destination/'subject',sorted(data))
    return destination/'subject'


def queue_job(client,source,command,outputs,key,fetch,timeout=1800):
    submit=[client,'submit','--project',REPOSITORY,'--source',str(source),'--request-key',key,'--timeout',str(timeout)]
    for path in outputs:submit+=['--output',path]
    submit+=['--',*command]
    accepted=subprocess.run(submit,cwd=TRUSTED_ROOT,text=True,capture_output=True)
    require(accepted.returncode==0,'Oracle submission failed; no local fallback')
    ack=json.loads(accepted.stdout);job=ack.get('job')
    require(ack.get('job_id',job)==job,'conflicting queue acknowledgement aliases')
    require(isinstance(job,str) and re.fullmatch('[0-9a-f]{32}',job),'invalid durable queue acknowledgement')
    require(ack.get('request_key')==key,'queue request-key binding mismatch')
    result=subprocess.run([client,'wait',job,'--fetch',str(fetch)],cwd=TRUSTED_ROOT)
    status=subprocess.run([client,'status',job],cwd=TRUSTED_ROOT,text=True,capture_output=True)
    require(status.returncode==0,'Oracle status unavailable');row=json.loads(status.stdout)
    require(row.get('id')==job and row.get('project')==REPOSITORY and row.get('request_key')==key,'queue result identity mismatch')
    require(result.returncode==0 and row.get('status')=='completed' and type(row.get('native_exit')) is int and row['native_exit']==0,'Oracle phase incomplete or failed: '+str(row.get('status'))+'/'+str(row.get('native_exit')))
    return row


def execute_phases(client,source,head,run_id,kind,tracked_files,temporary,execution):
    # A alone produces native authority: trusted code + candidate subject DATA.
    native=temporary/'native';subject=prepare_native(source,native);native_fetch=temporary/'native-fetch'
    write_source_receipt(native,head,run_id,kind,tracked_files,execution,role='trusted-native')
    expected=(native/SOURCE_RECEIPT).read_bytes()
    a=queue_job(client,native,['/usr/bin/python3','-B','producer/tools/run_models.py','--root','subject','--java','/usr/bin/java','--jar','/opt/tla/tla2tools-1.7.4.jar'],['subject/formal/evidence','subject/formal/RegistrySnapshot.tla',SOURCE_RECEIPT],execution_key('native',execution),native_fetch)
    require((native_fetch/SOURCE_RECEIPT).read_bytes()==expected,'native source/attempt receipt mismatch')
    count=verify_returned(subject,native_fetch/'subject');require(count==12,'trusted current campaign must qualify all twelve cases')
    _,campaign,adapter=trusted_modules()
    adapter.merge_evidence(native_fetch/'subject',source,campaign.RUNS)
    write_source_receipt(source,head,run_id,kind,tracked_files,execution)
    # B cannot replace root-owned A artifacts. Its mutable JSON is diagnostic;
    # actual exit of fixed isolated trusted driver composes candidate tests.
    b=queue_job(client,source,['/usr/bin/python3','-I','-B','-c',BOOTSTRAP],[RESULT_RECEIPT],execution_key('tests',execution),temporary/'tests-fetch',timeout=3600)
    return {'native_job':a['id'],'tests_job':b['id'],'native_cases':count,'execution':execution}


def current_target(api,run):
    if run['event']=='pull_request':return ('pull_request',current_prs(api,run))
    # Push run identity binds an immutable commit, including feature branches and
    # tags. GitHub attaches checks to that exact SHA, never a later branch head.
    # Do not drop a legitimate push merely because its branch moved/deleted.
    require(run['event']=='push','unsupported source event')
    return ('push',run['head_sha'])


def recheck_target(api,run,target):
    kind,value=target
    if kind=='pull_request':
        for pr in value:
            current=api.call('/repos/'+REPOSITORY+'/pulls/'+str(pr['number']))
            require(current.get('state')=='open' and current.get('head',{}).get('sha')==run['head_sha'],'PR head changed/closed while Oracle phases ran')
    else:
        actual=api.call(attempt_path(run['id'],run['run_attempt']))
        require(actual.get('head_sha')==value and actual.get('event')=='push'
                and actual.get('run_attempt')==run['run_attempt'],'push run attempt identity changed')


def publish(api,head,execution,status,conclusion=None,summary=''):
    body={'name':CHECK_NAME,'head_sha':head,'status':status,
          'external_id':execution_key('check',execution),
          'output':{'title':'Static checks and Oracle finite models','summary':summary[:60000]}}
    if conclusion:
        body.update(conclusion=conclusion,completed_at=datetime.now(timezone.utc).isoformat())
    return api.call('/repos/'+REPOSITORY+'/check-runs','POST',body)


def update(api,check_id,conclusion,summary):
    require(integer(check_id),'invalid check-run ID')
    return api.call('/repos/'+REPOSITORY+'/check-runs/'+str(check_id),'PATCH',
        {'status':'completed','conclusion':conclusion,'completed_at':datetime.now(timezone.utc).isoformat(),
         'output':{'title':'Static checks and Oracle finite models','summary':summary[:60000]}})


def dispatch(api,event,env):
    run=source_run(api,validate_event(event,env));head=run['head_sha']
    execution=execution_context(env,run,'workflow_run:'+run['event'])
    if run.get('conclusion')!='success':
        publish(api,head,execution,'completed','failure','Upstream public source/static checks did not succeed; no native job submitted.');return 1
    try:target=current_target(api,run)
    except (Refused,urllib.error.HTTPError):
        publish(api,head,execution,'completed','failure','The exact approved source head is no longer current; no native job submitted.');return 1
    check_run=publish(api,head,execution,'in_progress',summary='Hosted structural checks succeeded. Trusted native captures and complete candidate test phases queued for exact head '+head+'. Execution '+json.dumps(execution,sort_keys=True))
    require(integer(check_run.get('id')),'missing created check-run ID')
    try:
        client=shutil.which('tla-queue');require(client is not None,'Oracle queue client unavailable; no local fallback')
        with tempfile.TemporaryDirectory(prefix='post-ai-source-') as temp:
            temporary=Path(temp);source=temporary/'source';inputs=snapshot(api,head,source)
            receipt=execute_phases(client,source,head,run['id'],'workflow_run:'+run['event'],inputs['tracked_files'],temporary,execution)
            recheck_target(api,run,target)
        update(api,check_run['id'],'success','Hosted structural checks, trusted verification of twelve fresh native captures, and complete candidate test/static/site phases passed for exact head '+head+'. Native job '+receipt['native_job']+'; tests job '+receipt['tests_job']+'. No candidate Python ran on the persistent runner; candidate outputs are not native authority.');return 0
    except Exception as exc:
        message=type(exc).__name__+': '+str(exc)
        update(api,check_run['id'],'failure','Oracle verification failed for exact head '+head+'. '+message[:4000]);print(message,file=sys.stderr);return 1


def dispatch_manual(api,env):
    require(env.get('GITHUB_SERVER_URL')=='https://github.com' and env.get('GITHUB_REPOSITORY')==REPOSITORY,'wrong manual repository/server')
    require(env.get('GITHUB_EVENT_NAME')=='workflow_dispatch' and env.get('GITHUB_REF')=='refs/heads/main','manual main only')
    require(env.get('GITHUB_WORKFLOW_REF')==REPOSITORY+'/.github/workflows/oracle-tla.yml@refs/heads/main','wrong manual workflow')
    run_text=env.get('GITHUB_RUN_ID','');head=env.get('GITHUB_SHA','')
    require(isinstance(run_text,str) and run_text.isdigit() and int(run_text)>0,'invalid manual run ID')
    require(isinstance(head,str) and SHA.fullmatch(head),'invalid manual head')
    run_id=int(run_text);attempt=environment_integer(env,'GITHUB_RUN_ATTEMPT');run=api.call(attempt_path(run_id,attempt))
    require(integer(run.get('id')) and integer(run.get('run_attempt')) and run.get('id')==run_id and run.get('run_attempt')==attempt and run.get('event')=='workflow_dispatch' and run.get('head_sha')==head and run.get('head_branch')=='main','manual API identity mismatch')
    require(run.get('repository',{}).get('id')==REPOSITORY_ID,'manual repository ID mismatch')
    require(integer(run.get('workflow_id')),'invalid manual workflow ID')
    workflow=api.call('/repos/'+REPOSITORY+'/actions/workflows/'+str(run['workflow_id']))
    require(workflow.get('path')=='.github/workflows/oracle-tla.yml','manual workflow path mismatch')
    execution=execution_context(env,run,'manual')
    check_run=publish(api,head,execution,'in_progress',summary='Explicit manual main verification; structural, native and full candidate phases will run on Oracle. No upstream success is assumed. Execution '+json.dumps(execution,sort_keys=True))
    require(integer(check_run.get('id')),'missing manual check ID')
    try:
        client=shutil.which('tla-queue');require(client is not None,'Oracle queue client unavailable; no local fallback')
        with tempfile.TemporaryDirectory(prefix='post-ai-manual-') as temp:
            temporary=Path(temp);source=temporary/'source';inputs=snapshot(api,head,source)
            receipt=execute_phases(client,source,head,run_id,'manual',inputs['tracked_files'],temporary,execution)
        update(api,check_run['id'],'success','Explicit manual main verification passed structural/native/full tests for exact head '+head+'. Native job '+receipt['native_job']+'; tests job '+receipt['tests_job']+'.');return 0
    except Exception as exc:
        update(api,check_run['id'],'failure','Manual Oracle verification failed: '+type(exc).__name__+': '+str(exc)[:4000]);return 1


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--event',type=Path,default=os.environ.get('GITHUB_EVENT_PATH'))
    parser.add_argument('--manual',action='store_true')
    args=parser.parse_args()
    if args.manual:return dispatch_manual(API(os.environ.get('GITHUB_TOKEN')),os.environ)
    require(args.event is not None,'workflow_run event file required')
    event=json.loads(args.event.read_text())
    return dispatch(API(os.environ.get('GITHUB_TOKEN')),event,os.environ)


if __name__=='__main__':
    try:raise SystemExit(main())
    except (Refused,OSError,ValueError,urllib.error.URLError) as exc:
        print(type(exc).__name__+': '+str(exc),file=sys.stderr);raise SystemExit(1)
