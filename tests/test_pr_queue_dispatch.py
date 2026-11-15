"""Trusted dispatcher controls: no candidate code is executed on the runner."""
import base64
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('pr_dispatch',ROOT/'ci/queue_pr_models.py')
d=importlib.util.module_from_spec(spec);spec.loader.exec_module(d)
HEAD='a'*40
TREE='b'*40
PREFIX='/repos/'+d.REPOSITORY


def context():
    env={'GITHUB_SERVER_URL':'https://github.com','GITHUB_REPOSITORY':d.REPOSITORY,
         'GITHUB_EVENT_NAME':'workflow_run','GITHUB_REF':'refs/heads/main',
         'GITHUB_WORKFLOW_REF':d.DISPATCH_WORKFLOW,'GITHUB_WORKFLOW_SHA':'c'*40,
         'GITHUB_RUN_ID':'12345','GITHUB_RUN_ATTEMPT':'1'}
    run={'id':99,'run_attempt':1,'name':d.SOURCE_NAME,'event':'pull_request','status':'completed',
         'conclusion':'success','workflow_id':100,'head_sha':HEAD,'head_branch':'feature/source',
         'head_repository':{'id':1459282618,'full_name':'fork/post-ai-worlds'},
         'repository':{'id':d.REPOSITORY_ID,'full_name':d.REPOSITORY}}
    event={'action':'completed','repository':{'id':d.REPOSITORY_ID,'full_name':d.REPOSITORY,'fork':False},'workflow_run':run}
    return event,env


def pr():
    return {'number':1,'state':'open','head':{'sha':HEAD,'ref':'feature/source','repo':{'id':1459282618,'full_name':'fork/post-ai-worlds'}},'base':{'repo':{'id':d.REPOSITORY_ID,'full_name':d.REPOSITORY}}}


class FakeAPI:
    def __init__(self):
        self.run=context()[0]['workflow_run'];self.pull=pr();self.writes=[]
    def call(self,path,method='GET',body=None):
        if method!='GET':
            self.writes.append((path,method,copy.deepcopy(body)));return {'id':101}
        routes={PREFIX+'/actions/runs/99/attempts/'+str(self.run['run_attempt']):self.run,PREFIX+'/actions/workflows/100':{'path':d.SOURCE_WORKFLOW},
                PREFIX+'/commits/'+HEAD+'/pulls?per_page=100':[pr()],PREFIX+'/pulls/1':self.pull}
        if path.startswith(PREFIX+'/pulls?'):return []
        return copy.deepcopy(routes[path])


class EventTests(unittest.TestCase):
    def test_only_exact_default_branch_dispatcher_and_completed_pr_source(self):
        event,env=context();self.assertEqual(99,d.validate_event(event,env)['id'])
        for key,value in [('GITHUB_REF','refs/heads/other'),('GITHUB_EVENT_NAME','pull_request_target'),('GITHUB_WORKFLOW_REF','other'),('GITHUB_REPOSITORY','foreign/repo')]:
            changed=dict(env);changed[key]=value
            with self.subTest(key=key),self.assertRaises(d.Refused):d.validate_event(event,changed)
        for key,value in [('id',True),('event','workflow_dispatch'),('status','requested'),('head_sha','../escape'),('name','attacker workflow')]:
            changed=copy.deepcopy(event);changed['workflow_run'][key]=value
            with self.subTest(key=key),self.assertRaises(d.Refused):d.validate_event(changed,env)

    def test_authoritative_run_and_workflow_path_must_match(self):
        event,_=context();api=FakeAPI()
        self.assertEqual(99,d.source_run(api,event['workflow_run'])['id'])
        api.run['head_sha']='c'*40
        with self.assertRaises(d.Refused):d.source_run(api,event['workflow_run'])
        api=FakeAPI();real=api.call
        with mock.patch.object(api,'call',side_effect=lambda path,**kw:{'path':'attacker.yml'} if '/actions/workflows/' in path else real(path,**kw)):
            with self.assertRaises(d.Refused):d.source_run(api,event['workflow_run'])

    def test_head_association_must_be_open_and_exact(self):
        api=FakeAPI();self.assertEqual(1,d.current_prs(api,api.run)[0]['number'])
        with mock.patch.object(api,'call',return_value=[dict(pr(),head={'sha':'c'*40})]):
            with self.assertRaises(d.Refused):d.current_prs(api,api.run)


class AttemptTests(unittest.TestCase):
    def execution(self,source_attempt=1,dispatcher_attempt=1):
        event,env=context();event['workflow_run']['run_attempt']=source_attempt
        env['GITHUB_RUN_ATTEMPT']=str(dispatcher_attempt)
        return d.execution_context(env,event['workflow_run'],'workflow_run:pull_request')

    def test_same_attempt_is_stable_but_each_source_or_dispatcher_rerun_is_fresh(self):
        first=self.execution();same=dict(reversed(list(first.items())))
        for phase in ('native','tests','check'):
            key=d.execution_key(phase,first)
            self.assertEqual(key,d.execution_key(phase,same))
            self.assertLessEqual(len(key),96)
            self.assertNotEqual(key,d.execution_key(phase,self.execution(source_attempt=2)))
            self.assertNotEqual(key,d.execution_key(phase,self.execution(dispatcher_attempt=2)))
        self.assertNotEqual(d.execution_key('native',first),d.execution_key('tests',first))

    def test_exact_source_attempt_endpoint_and_api_binding(self):
        event,_=context();event['workflow_run']['run_attempt']=2;api=FakeAPI()
        api.run=copy.deepcopy(event['workflow_run'])
        with mock.patch.object(api,'call',wraps=api.call) as call:
            self.assertEqual(2,d.source_run(api,event['workflow_run'])['run_attempt'])
        self.assertEqual(PREFIX+'/actions/runs/99/attempts/2',call.call_args_list[0].args[0])
        for actual in (1,True,"2",None):
            api=FakeAPI();api.run=copy.deepcopy(event['workflow_run']);api.run['run_attempt']=actual
            original=api.call
            with self.subTest(actual=actual),mock.patch.object(api,'call',side_effect=lambda path:copy.deepcopy(api.run) if '/actions/runs/' in path else original(path)),self.assertRaises(d.Refused):
                d.source_run(api,event['workflow_run'])

    def test_missing_or_invalid_attempt_context_never_submits_or_publishes(self):
        for name in ('GITHUB_RUN_ID','GITHUB_RUN_ATTEMPT','GITHUB_WORKFLOW_SHA'):
            for value in (None,'','0','-1','true','1.5'):
                event,env=context()
                if value is None:del env[name]
                else:env[name]=value
                api=FakeAPI()
                with self.subTest(name=name,value=value),mock.patch.object(d,'queue_job') as queue,self.assertRaises(d.Refused):
                    d.dispatch(api,event,env)
                queue.assert_not_called();self.assertEqual([],api.writes)
        for value in (None,0,True,'1'):
            event,env=context();event['workflow_run']['run_attempt']=value
            with self.subTest(value=value),self.assertRaises(d.Refused):d.validate_event(event,env)

    def test_published_check_and_source_receipt_bind_identical_execution(self):
        execution=self.execution(source_attempt=2,dispatcher_attempt=3);api=FakeAPI()
        d.publish(api,HEAD,execution,'in_progress')
        self.assertEqual(d.execution_key('check',execution),api.writes[0][2]['external_id'])
        self.assertEqual(HEAD,api.writes[0][2]['head_sha'])
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary)
            d.write_source_receipt(root,HEAD,99,'workflow_run:pull_request',['README.md'],execution)
            receipt=json.loads((root/d.SOURCE_RECEIPT).read_text())
            self.assertEqual(execution,receipt['execution'])
            wrong=dict(execution,source_run_id=100)
            with self.assertRaises(d.Refused):
                d.write_source_receipt(root,HEAD,99,'workflow_run:pull_request',['README.md'],wrong)

    def test_native_attempt_receipt_mismatch_stops_before_verification_or_test_job(self):
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary);source=root/'source';source.mkdir();execution=self.execution()
            def prepare(candidate,destination):
                (destination/'subject').mkdir(parents=True);return destination/'subject'
            def queue(client,payload,command,outputs,key,fetch):
                self.assertIn(d.SOURCE_RECEIPT,outputs)
                fetch.mkdir();value=json.loads((payload/d.SOURCE_RECEIPT).read_text())
                value['execution']['source_run_attempt']=999
                (fetch/d.SOURCE_RECEIPT).write_text(json.dumps(value))
                return {'id':'a'*32}
            with mock.patch.object(d,'prepare_native',side_effect=prepare),mock.patch.object(d,'queue_job',side_effect=queue) as launch,mock.patch.object(d,'verify_returned') as verify,self.assertRaisesRegex(d.Refused,'attempt receipt mismatch'):
                d.execute_phases('/client',source,HEAD,99,'workflow_run:pull_request',['README.md'],root,execution)
            self.assertEqual(1,launch.call_count);verify.assert_not_called()

    def test_manual_rerun_gets_new_execution_without_inventing_upstream_success(self):
        published=[];executions=[]
        for attempt in (1,2):
            _,env=context();env.update(GITHUB_EVENT_NAME='workflow_dispatch',GITHUB_WORKFLOW_REF=d.REPOSITORY+'/.github/workflows/oracle-tla.yml@refs/heads/main',GITHUB_RUN_ID='99',GITHUB_RUN_ATTEMPT=str(attempt),GITHUB_SHA=HEAD)
            api=FakeAPI();api.run.update(event='workflow_dispatch',head_branch='main',run_attempt=attempt)
            original=api.call
            def call(path,*args,**kwargs):
                if path.endswith('/actions/workflows/100'):return {'path':'.github/workflows/oracle-tla.yml'}
                return original(path,*args,**kwargs)
            def snapshot(fake,head,root):root.mkdir();return {'tracked_files':['README.md']}
            with mock.patch.object(api,'call',side_effect=call),mock.patch.object(d.shutil,'which',return_value='/client'),mock.patch.object(d,'snapshot',side_effect=snapshot),mock.patch.object(d,'execute_phases',return_value={'native_job':'a'*32,'tests_job':'b'*32}) as phases:
                self.assertEqual(0,d.dispatch_manual(api,env))
            executions.append(phases.call_args.args[-1]);published.append(api.writes[0][2]['external_id'])
            self.assertEqual(attempt,executions[-1]['source_run_attempt'])
            self.assertEqual(attempt,executions[-1]['dispatcher_run_attempt'])
            self.assertIn('No upstream success is assumed',api.writes[0][2]['output']['summary'])
        self.assertNotEqual(published[0],published[1])
        for phase in ('native','tests'):
            self.assertNotEqual(d.execution_key(phase,executions[0]),d.execution_key(phase,executions[1]))


class ForkAssociationTests(unittest.TestCase):
    def fixture(self,commit_matches=False):
        # Real-shaped PR12 control: both source-run and commit associations empty,
        # fork repository name differs from the base, same source branch/head.
        run=copy.deepcopy(context()[0]['workflow_run'])
        run.update(id=43767225989,head_sha='e3a214a'+'0'*33,
                   head_branch='verify/oracle-queue-190-fork',pull_requests=[],
                   head_repository={'id':1459282618,'full_name':'LekkoTechnologiczny/post-ai-worlds-oracle-queue-probe'})
        pull=pr();pull.update(number=12)
        pull['head'].update(sha=run['head_sha'],ref=run['head_branch'],repo=copy.deepcopy(run['head_repository']))
        state={'run':run,'pull':pull,'commits':[copy.deepcopy(pull)] if commit_matches else [],'open':[copy.deepcopy(pull)],'calls':[]}
        def call(path):
            state['calls'].append(path)
            if '/commits/' in path:return copy.deepcopy(state['commits'])
            if path.startswith(PREFIX+'/pulls?'):return copy.deepcopy(state['open'])
            if path==PREFIX+'/pulls/12':return copy.deepcopy(state['pull'])
            self.fail('unexpected API route '+path)
        state['api']=type('API',(),{'call':staticmethod(call)})()
        return state

    def test_empty_fork_associations_use_encoded_authoritative_head_query_and_direct_get(self):
        state=self.fixture();found=d.current_prs(state['api'],state['run'])
        self.assertEqual([12],[x['number'] for x in found])
        self.assertEqual([],state['run']['pull_requests'])
        query=d.urllib.parse.parse_qs(d.urllib.parse.urlsplit(state['calls'][1]).query)
        self.assertEqual({'state':['open'],'head':['LekkoTechnologiczny:verify/oracle-queue-190-fork'],'per_page':['100']},query)
        self.assertIn('%3Averify%2Foracle-queue-190-fork',state['calls'][1])
        self.assertEqual(PREFIX+'/pulls/12',state['calls'][2])
        d.recheck_target(state['api'],state['run'],('pull_request',found))
        self.assertEqual(PREFIX+'/pulls/12',state['calls'][-1])

    def test_valid_commit_association_keeps_full_identity_and_direct_get_without_fallback(self):
        state=self.fixture(commit_matches=True)
        self.assertEqual(12,d.current_prs(state['api'],state['run'])[0]['number'])
        self.assertFalse(any(path.startswith(PREFIX+'/pulls?') for path in state['calls']))
        self.assertEqual(PREFIX+'/pulls/12',state['calls'][-1])

    def test_source_branch_query_metacharacters_remain_encoded_data(self):
        state=self.fixture();branch='verify/fork&state=closed'
        state['run']['head_branch']=branch;state['pull']['head']['ref']=branch
        state['open']=[copy.deepcopy(state['pull'])]
        self.assertEqual(12,d.current_prs(state['api'],state['run'])[0]['number'])
        query=d.urllib.parse.parse_qs(d.urllib.parse.urlsplit(state['calls'][1]).query)
        self.assertEqual(['open'],query['state'])
        self.assertEqual(['100'],query['per_page'])
        self.assertEqual(['LekkoTechnologiczny:'+branch],query['head'])

    def mutations(self,pull):
        changes=[]
        for path,value in ((('state',),'closed'),(('number',),True),
                           (('head','repo','id'),1),(('head','repo','id'),True),
                           (('head','repo','full_name'),'wrong-owner/post-ai-worlds-oracle-queue-probe'),
                           (('head','repo','full_name'),'LekkoTechnologiczny/wrong-repository'),
                           (('head','ref'),'verify/other'),(('head','sha'),'c'*40),
                           (('base','repo','id'),1),(('base','repo','id'),True),
                           (('base','repo','full_name'),'fork/post-ai-worlds')):
            changed=copy.deepcopy(pull);target=changed
            for name in path[:-1]:target=target[name]
            target[path[-1]]=value;changes.append((path,value,changed))
        return changes

    def test_fallback_does_not_accept_wrong_owner_repo_ref_sha_base_or_closed_pr(self):
        baseline=self.fixture()
        for path,value,changed in self.mutations(baseline['pull']):
            with self.subTest(path=path,value=value):
                state=self.fixture();state['open']=[changed]
                with self.assertRaises(d.Refused):d.current_prs(state['api'],state['run'])

    def test_direct_get_before_and_after_native_must_keep_all_identity_fields(self):
        baseline=self.fixture()
        for path,value,changed in self.mutations(baseline['pull']):
            with self.subTest(phase='before',path=path,value=value):
                state=self.fixture();state['pull']=changed
                with self.assertRaises(d.Refused):d.current_prs(state['api'],state['run'])
            with self.subTest(phase='after',path=path,value=value):
                state=self.fixture();found=d.current_prs(state['api'],state['run']);state['pull']=changed
                with self.assertRaises(d.Refused):d.recheck_target(state['api'],state['run'],('pull_request',found))

    def test_ambiguous_or_truncated_responses_and_missing_source_identity_refused(self):
        for route in ('commits','open'):
            for values in (None,{},[self.fixture()['pull']]*100):
                with self.subTest(route=route,size=len(values) if values is not None else None):
                    state=self.fixture();state[route]=values
                    with self.assertRaises(d.Refused):d.current_prs(state['api'],state['run'])
        state=self.fixture();state['open']*=2
        with self.assertRaises(d.Refused):d.current_prs(state['api'],state['run'])
        for field,value in (('head_repository',None),('head_repository',{'id':True,'full_name':'owner/repo'}),
                            ('head_repository',{'id':123,'full_name':'owner/repo?other=1'}),
                            ('head_branch',None),('head_branch',''),('head_branch','x\nquery')):
            state=self.fixture();state['run'][field]=value
            with self.subTest(field=field,value=value),self.assertRaises(d.Refused):d.current_prs(state['api'],state['run'])

    def test_unverified_event_pr_metadata_does_not_select_fallback_target(self):
        state=self.fixture();state['run']['pull_requests']=[{'number':999,'head':{'sha':'f'*40}}]
        self.assertEqual(12,d.current_prs(state['api'],state['run'])[0]['number'])
        self.assertFalse(any('/pulls/999' in path for path in state['calls']))
        event,_=context();event['workflow_run']['head_repository']={'id':1,'full_name':'forged-owner/forged-repository'}
        api=FakeAPI();authoritative=d.source_run(api,event['workflow_run'])
        self.assertEqual(api.run['head_repository'],authoritative['head_repository'])
        self.assertNotEqual(event['workflow_run']['head_repository'],authoritative['head_repository'])


class PushAndManualTests(unittest.TestCase):
    def test_all_push_heads_include_main_feature_tag_and_detached_source(self):
        for branch in ('main','feature/source','v1.0',None):
            event,env=context();event['workflow_run'].update(event='push',head_branch=branch)
            api=FakeAPI();api.run=copy.deepcopy(event['workflow_run'])
            self.assertEqual('push',d.validate_event(event,env)['event'])
            self.assertEqual(('push',HEAD),d.current_target(api,api.run))
            # No current-branch lookup: moved/deleted branch cannot erase the
            # original immutable push's coverage, and check SHA stays exact.
            d.recheck_target(api,api.run,('push',HEAD))

    def test_manual_main_has_explicit_authority_without_fake_upstream_success(self):
        _,env=context();env.update(GITHUB_EVENT_NAME='workflow_dispatch',GITHUB_WORKFLOW_REF=d.REPOSITORY+'/.github/workflows/oracle-tla.yml@refs/heads/main',GITHUB_RUN_ID='99',GITHUB_SHA=HEAD)
        api=FakeAPI();api.run.update(event='workflow_dispatch',head_branch='main')
        real=api.call
        def call(path,*args,**kwargs):
            if path.endswith('/actions/workflows/100'):return {'path':'.github/workflows/oracle-tla.yml'}
            return real(path,*args,**kwargs)
        def snapshot(fake,head,root):root.mkdir();return {'tracked_files':['README.md']}
        with mock.patch.object(api,'call',side_effect=call),mock.patch.object(d.shutil,'which',return_value='/client'),mock.patch.object(d,'snapshot',side_effect=snapshot),mock.patch.object(d,'execute_phases',return_value={'native_job':'a'*32,'tests_job':'b'*32}) as phases:
            self.assertEqual(0,d.dispatch_manual(api,env))
        self.assertEqual('manual',phases.call_args.args[4])
        self.assertIn('No upstream success is assumed',api.writes[0][2]['output']['summary'])
        self.assertEqual('success',api.writes[-1][2]['conclusion'])
        wrong=dict(env);wrong['GITHUB_REF']='refs/heads/feature'
        with self.assertRaises(d.Refused):d.dispatch_manual(api,wrong)


class QueueEnvelopeTests(unittest.TestCase):
    def test_minimal_real_submit_envelope_and_status_binding(self):
        job='a'*32;key='test-key'
        row={'id':job,'project':d.REPOSITORY,'request_key':key,'status':'completed','native_exit':0}
        replies=[subprocess.CompletedProcess([],0,stdout=json.dumps({'job':job,'request_key':key,'status':'queued'})),subprocess.CompletedProcess([],0),subprocess.CompletedProcess([],0,stdout=json.dumps(row))]
        with mock.patch.object(d.subprocess,'run',side_effect=replies) as launch:
            self.assertEqual(job,d.queue_job('/client',Path('/source'),['true'],['out'],key,Path('/fetch'))['id'])
        self.assertEqual(['submit','wait','status'],[x.args[0][1] for x in launch.call_args_list])

    def test_status_wrong_job_project_key_bool_exit_or_nonzero_wait_refused(self):
        job='a'*32;key='test-key'
        for field,value,wait in [('id','b'*32,0),('project','foreign/repo',0),('request_key','other',0),('native_exit',False,0),('native_exit',1,0),('status','interrupted',0),('native_exit',0,75)]:
            row={'id':job,'project':d.REPOSITORY,'request_key':key,'status':'completed','native_exit':0};row[field]=value
            replies=[subprocess.CompletedProcess([],0,stdout=json.dumps({'job':job,'request_key':key})),subprocess.CompletedProcess([],wait),subprocess.CompletedProcess([],0,stdout=json.dumps(row))]
            with self.subTest(field=field,value=value,wait=wait),mock.patch.object(d.subprocess,'run',side_effect=replies),self.assertRaises(d.Refused):
                d.queue_job('/client',Path('/source'),['true'],['out'],key,Path('/fetch'))

class BootstrapProcessTests(unittest.TestCase):
    def fixture(self,root,fail=False):
        files={
            'README.md':'# Fixture\n',
            'tools/check.py':('import pathlib,sys;pathlib.Path(".oracle-result.json").write_text(\'{"complete":true}\');sys.exit(1)' if fail else 'print("ordinary fixture passed")'),
            'tools/build_navigation.py':'import subprocess;assert "README.md" in subprocess.check_output(["git","ls-files"],text=True)',
            'tests/test_fixture.py':'import unittest\nclass Fixture(unittest.TestCase):\n def test_required(self):self.assertTrue(True)\n',
            'website/build.py':'print("website fixture unchanged")'}
        for name,text in files.items():
            p=root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
        event,env=context();execution=d.execution_context(env,event['workflow_run'],'workflow_run:pull_request')
        d.write_source_receipt(root,HEAD,99,'workflow_run:pull_request',list(files),execution)

    def test_fixed_isolated_driver_runs_all_non_native_phases_without_fake_head(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);self.fixture(root)
            result=subprocess.run([sys.executable,'-I','-B','-c',d.BOOTSTRAP],cwd=root,text=True,capture_output=True)
            self.assertEqual(0,result.returncode,result.stdout+result.stderr)
            report=json.loads((root/d.RESULT_RECEIPT).read_text())
            self.assertIs(True,report['complete']);self.assertEqual(d.PHASES,[x['name'] for x in report['phases']])
            self.assertEqual(json.loads((root/d.SOURCE_RECEIPT).read_text())['execution'],report['execution'])
            self.assertNotIn('native',[x['name'] for x in report['phases']])
            head=subprocess.run(['git','rev-parse','--verify','HEAD'],cwd=root,capture_output=True)
            self.assertNotEqual(0,head.returncode)

    def test_failed_candidate_phase_cannot_replace_driver_exit_with_fake_report(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);self.fixture(root,fail=True)
            result=subprocess.run([sys.executable,'-I','-B','-c',d.BOOTSTRAP],cwd=root,text=True,capture_output=True)
            self.assertEqual(1,result.returncode)
            report=json.loads((root/d.RESULT_RECEIPT).read_text())
            self.assertIs(False,report['complete'])
            self.assertEqual(['git_index','ordinary'],[x['name'] for x in report['phases']])


class SnapshotTests(unittest.TestCase):
    def fixture(self):
        files={name:b'source fixture' for name in d.REQUIRED}
        files['formal/Example.tla']=b'---- MODULE Example ----\n===='
        entries=[];blobs={}
        for path,data in files.items():
            sha=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
            entries.append({'path':path,'type':'blob','mode':'100644','size':len(data),'sha':sha})
            blobs[sha]={'sha':sha,'encoding':'base64','content':base64.b64encode(data).decode()}
        tree={'sha':TREE,'truncated':False,'tree':entries}
        def call(path):
            if '/git/commits/' in path:return {'sha':HEAD,'tree':{'sha':TREE}}
            if '/git/trees/' in path:return copy.deepcopy(tree)
            return copy.deepcopy(blobs[path.rsplit('/',1)[1]])
        return tree,blobs,type('API',(),{'call':staticmethod(call)})()

    def test_snapshot_materializes_verified_regular_blobs_without_exec(self):
        tree,blobs,api=self.fixture()
        with tempfile.TemporaryDirectory() as temp,mock.patch.object(d.subprocess,'run',side_effect=AssertionError('no candidate exec')):
            target=Path(temp)/'snapshot';selected=d.snapshot(api,HEAD,target)
            self.assertEqual({x['path'] for x in tree['tree']},set(selected['files']))
            self.assertEqual(b'source fixture',(target/'tools/check.py').read_bytes())
            self.assertFalse((target/'.git').exists())

    def test_link_submodule_path_duplicate_and_truncated_tree_refused(self):
        for mutation in ('symlink','submodule','path','duplicate','truncated','size'):
            tree,blobs,api=self.fixture()
            if mutation=='symlink':tree['tree'][0]['mode']='120000'
            if mutation=='submodule':tree['tree'][0].update(type='commit',mode='160000')
            if mutation=='path':tree['tree'][0]['path']='tools/../escape'
            if mutation=='duplicate':tree['tree'].append(copy.deepcopy(tree['tree'][0]))
            if mutation=='truncated':tree['truncated']=True
            if mutation=='size':tree['tree'][0]['size']=d.MAX_BLOB+1
            with tempfile.TemporaryDirectory() as temp,self.subTest(mutation=mutation),self.assertRaises(d.Refused):d.snapshot(api,HEAD,Path(temp)/'snapshot')

    def test_git_blob_hash_and_size_are_verified(self):
        tree,blobs,api=self.fixture()
        one=next(iter(blobs.values()));one['content']=base64.b64encode(b'different bytes').decode()
        with tempfile.TemporaryDirectory() as temp,self.assertRaises(d.Refused):d.snapshot(api,HEAD,Path(temp)/'snapshot')

    def test_old_evidence_is_not_submitted_as_fresh(self):
        tree,blobs,api=self.fixture();tree['tree'].append({'path':'formal/evidence/fake.log','type':'blob','mode':'100644','size':3,'sha':'c'*40})
        with tempfile.TemporaryDirectory() as temp:
            target=Path(temp)/'snapshot';d.snapshot(api,HEAD,target)
            self.assertFalse((target/'formal/evidence').exists())


class TrustedVerifierTests(unittest.TestCase):
    def candidate(self,root):
        for folder in ('tools','formal','worlds'):
            shutil.copytree(ROOT/folder,root/folder,ignore=shutil.ignore_patterns('__pycache__'))

    def test_hostile_candidate_producer_refused_before_native_authority(self):
        import shutil
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);source=root/'source';source.mkdir()
            for folder in ('tools','formal','worlds'):
                shutil.copytree(ROOT/folder,source/folder,ignore=shutil.ignore_patterns('__pycache__'))
            (source/'tools/check.py').write_text('raise AssertionError("hostile candidate")')
            with self.assertRaisesRegex(d.Refused,'unsupported producer'):
                d.prepare_native(source,root/'native')
            self.assertFalse((root/'native').exists())

    def test_native_payload_contains_only_trusted_code_and_candidate_data(self):
        import shutil
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);source=root/'source';source.mkdir()
            for folder in ('tools','formal','worlds'):
                shutil.copytree(ROOT/folder,source/folder,ignore=shutil.ignore_patterns('__pycache__'))
            (source/'tools/malicious.py').write_text('raise AssertionError("not native input")')
            subject=d.prepare_native(source,root/'native')
            self.assertEqual((ROOT/'tools/check.py').read_bytes(),(root/'native/producer/tools/check.py').read_bytes())
            self.assertEqual((ROOT/'tools/check.py').read_bytes(),(subject/'tools/check.py').read_bytes())
            self.assertFalse((root/'native/producer/tools/malicious.py').exists())
            self.assertFalse((subject/'tools/malicious.py').exists())
            self.assertFalse((subject/'formal/evidence').exists())

    def test_candidate_test_artifacts_never_replace_separate_native_authority(self):
        import shutil
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);source=root/'source';source.mkdir()
            for folder in ('tools','formal','worlds'):
                shutil.copytree(ROOT/folder,source/folder,ignore=shutil.ignore_patterns('__pycache__'))
            calls=[];authority={}
            def queue(client,payload,command,outputs,key,fetch,timeout=1800):
                calls.append((command,outputs))
                if len(calls)==1:
                    (fetch/'subject/formal').mkdir(parents=True)
                    shutil.copytree(ROOT/'formal/evidence',fetch/'subject/formal/evidence')
                    shutil.copyfile(ROOT/'formal/RegistrySnapshot.tla',fetch/'subject/formal/RegistrySnapshot.tla')
                    authority['manifest']=fetch/'subject/formal/evidence/manifest.json'
                    authority['bytes']=authority['manifest'].read_bytes()
                    shutil.copyfile(payload/d.SOURCE_RECEIPT,fetch/d.SOURCE_RECEIPT)
                    return {'id':'a'*32}
                # Simulate hostile B rewriting its copied proof/report. A is in
                # another terminal queue job and not declared as a B output.
                (payload/'formal/evidence/manifest.json').write_text('fake native success')
                fetch.mkdir();(fetch/d.RESULT_RECEIPT).write_text('{"native_cases":999,"complete":true}')
                self.assertEqual([d.RESULT_RECEIPT],outputs)
                return {'id':'b'*32,'native_cases':999}
            tracked=['tools/check.py','formal/RegistrySnapshot.tla','formal/evidence/manifest.json']
            with mock.patch.object(d,'queue_job',side_effect=queue),mock.patch.object(d,'verify_returned',return_value=12) as verifier:
                event,env=context();execution=d.execution_context(env,event['workflow_run'],'workflow_run:pull_request')
                result=d.execute_phases('/client',source,HEAD,99,'workflow_run:pull_request',tracked,root,execution)
            self.assertEqual(12,result['native_cases']);self.assertEqual('a'*32,result['native_job'])
            self.assertEqual(authority['bytes'],authority['manifest'].read_bytes())
            self.assertEqual(1,verifier.call_count)
            self.assertEqual(['/usr/bin/python3','-I','-B','-c'],calls[1][0][:4])
            self.assertNotIn("phase('native'",d.BOOTSTRAP)
            self.assertIn("'--pathspec-file-nul'",d.BOOTSTRAP)
            self.assertNotIn("git commit",d.BOOTSTRAP)


class VerdictTests(unittest.TestCase):
    def exercise(self,api,native_exit=0,verify=12,after_native=None):
        event,env=context()
        def snapshot(fake_api,head,root):root.mkdir();return {'tracked_files':['README.md']}
        def execute(*args):
            if native_exit:raise d.Refused('Oracle command failed')
            if verify!=12:raise d.Refused('trusted native captures did not qualify')
            if after_native:after_native()
            return {'native_job':'a'*32,'tests_job':'b'*32,'native_cases':12}
        with mock.patch.object(d,'snapshot',side_effect=snapshot),mock.patch.object(d.shutil,'which',return_value='/installed/tla-queue'),mock.patch.object(d,'execute_phases',side_effect=execute) as phases:
            result=d.dispatch(api,event,env)
        return result,phases,phases

    def test_combined_success_requires_upstream_native_and_trusted_artifacts(self):
        api=FakeAPI();result,launch,verifier=self.exercise(api)
        self.assertEqual(0,result);self.assertEqual(1,launch.call_count);self.assertEqual(1,verifier.call_count)
        created=api.writes[0][2];completed=api.writes[-1][2]
        self.assertEqual('validate',created['name']);self.assertEqual(HEAD,created['head_sha'])
        self.assertEqual('success',completed['conclusion'])
        self.assertEqual('/installed/tla-queue',launch.call_args.args[0])

    def test_unsuccessful_hosted_check_never_submits_native_job(self):
        event,env=context();event['workflow_run']['conclusion']='failure';api=FakeAPI();api.run['conclusion']='failure'
        with mock.patch.object(d.subprocess,'run') as launch:
            self.assertEqual(1,d.dispatch(api,event,env))
        launch.assert_not_called();self.assertEqual('failure',api.writes[-1][2]['conclusion'])

    def test_static_failure_publishes_even_without_open_pr(self):
        event,env=context();event['workflow_run']['conclusion']='cancelled';api=FakeAPI();api.run['conclusion']='cancelled'
        real=api.call
        with mock.patch.object(api,'call',side_effect=lambda path,*args,**kw:[] if '/commits/' in path else real(path,*args,**kw)),mock.patch.object(d.subprocess,'run') as launch:
            self.assertEqual(1,d.dispatch(api,event,env))
        launch.assert_not_called();self.assertEqual('failure',api.writes[-1][2]['conclusion'])

    def test_stale_head_before_submission_publishes_non_success_without_queue(self):
        event,env=context();api=FakeAPI();real=api.call
        with mock.patch.object(api,'call',side_effect=lambda path,*args,**kw:[] if '/commits/' in path else real(path,*args,**kw)),mock.patch.object(d.subprocess,'run') as launch:
            self.assertEqual(1,d.dispatch(api,event,env))
        launch.assert_not_called();self.assertEqual('failure',api.writes[-1][2]['conclusion'])

    def test_successful_exit_without_qualified_artifacts_never_passes(self):
        api=FakeAPI();result,launch,verifier=self.exercise(api,verify=11)
        self.assertEqual(1,result);self.assertEqual('failure',api.writes[-1][2]['conclusion'])

    def test_native_nonzero_never_reaches_artifact_success(self):
        api=FakeAPI();result,launch,verifier=self.exercise(api,native_exit=75)
        self.assertEqual(1,result);self.assertEqual('failure',api.writes[-1][2]['conclusion'])

    def test_candidate_test_job_failure_cannot_publish_success(self):
        event,env=context();api=FakeAPI()
        def snapshot(fake,head,root):root.mkdir();return {'tracked_files':['README.md']}
        with mock.patch.object(d,'snapshot',side_effect=snapshot),mock.patch.object(d.shutil,'which',return_value='/client'),mock.patch.object(d,'execute_phases',side_effect=d.Refused('B trusted driver exit1; fake success report ignored')):
            self.assertEqual(1,d.dispatch(api,event,env))
        self.assertEqual('failure',api.writes[-1][2]['conclusion'])

    def test_stale_head_after_native_success_is_not_credited(self):
        api=FakeAPI()
        result,launch,verifier=self.exercise(api,after_native=lambda:api.pull['head'].update(sha='c'*40))
        self.assertEqual(1,result);self.assertEqual('failure',api.writes[-1][2]['conclusion'])
        self.assertEqual(1,launch.call_count)
        self.assertEqual(HEAD,api.writes[0][2]['head_sha'])


if __name__=='__main__':unittest.main()
