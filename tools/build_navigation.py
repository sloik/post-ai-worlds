#!/usr/bin/env python3
"""Build public document navigation from tracked Markdown links, not semantic claims."""

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from urllib.parse import quote, unquote

REPOSITORY = "https://github.com/sloik/post-ai-worlds"
ROOT = Path(__file__).resolve().parents[1]
OUTPUT = "graphs/canonical-navigation.json"


def tracked_documents(root):
    names = subprocess.check_output(
        ["git", "-C", str(root), "ls-files", "-z", "--", "*.md"], text=True
    ).split("\0")
    return sorted(
        n
        for n in names
        if n
        and not n.startswith("graphs/")
        and not any(part.startswith(".") for part in Path(n).parts)
    )


def link_lines(text):
    """Simple inline-link input only; skip frontmatter, fences and inline code."""
    lines = text.splitlines()
    front = bool(lines and lines[0].strip() == "---")
    fence = None
    for number, line in enumerate(lines, 1):
        if front:
            if number > 1 and line.strip() == "---":
                front = False
            continue
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if marker:
            token, suffix = marker.groups()
            if fence is None:
                fence = (token[0], len(token))
            elif token[0] == fence[0] and len(token) >= fence[1] and not suffix.strip():
                fence = None
            continue
        if fence is None:
            yield number, re.sub(r"(`+).*?\1", "", line)


def build(root):
    paths = tracked_documents(root)
    if not {
        "CANONICAL.md",
        "README.md",
        "post-ai/README.md",
        "omnicorp/README.md",
    } <= set(paths):
        raise ValueError("missing canonical owning documents")
    contents = {}
    for name in paths:
        path = root / name
        if path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
            raise ValueError("tracked source escapes public root")
    # Validate every tracked path before reading even the controlling declaration.
    for name in paths:
        contents[name] = (root / name).read_bytes()
    source = contents["CANONICAL.md"].decode("utf-8")
    if (
        REPOSITORY not in source
        or "[post-ai/](post-ai/README.md)" not in source
        or "[omnicorp/](omnicorp/README.md)" not in source
    ):
        raise ValueError("canonical declaration changed; review owner routes")
    nodes = [
        {
            "id": REPOSITORY,
            "label": "Post-AI Era Vision & Omnicorp — canonical repository",
            "url": REPOSITORY,
            "kind": "repository",
            "provenance": "CANONICAL.md",
        }
    ]
    for name in paths:
        content = contents[name]
        title = next(
            (
                line.lstrip("# ").strip()
                for line in content.decode().splitlines()
                if line.startswith("# ")
            ),
            name,
        )
        nodes.append(
            {
                "id": name,
                "label": title,
                "url": REPOSITORY + "/blob/main/" + quote(name),
                "kind": "document",
                "sha256": hashlib.sha256(content).hexdigest(),
            }
        )
    edges = [
        {
            "source": REPOSITORY,
            "target": name,
            "relation": "canonical_track",
            "source_file": "CANONICAL.md",
        }
        for name in ("post-ai/README.md", "omnicorp/README.md")
    ]
    known = set(paths)
    found = {}
    for name in paths:
        for number, line in link_lines(contents[name].decode("utf-8")):
            for target in re.findall(r"\]\(([^\s)]+)(?:\s+[^)]*)?\)", line):
                if target.startswith("#") or re.match(r"^[A-Za-z]+:", target):
                    continue
                plain, _, anchor = unquote(target).partition("#")
                path = (root / name).parent / plain
                try:
                    relative = path.resolve().relative_to(root.resolve()).as_posix()
                except ValueError:
                    continue
                if relative not in known:
                    continue
                key = (name, relative)
                item = found.setdefault(
                    key,
                    {
                        "source": name,
                        "target": relative,
                        "relation": "markdown_link",
                        "source_file": name,
                        "source_lines": [],
                        "anchors": [],
                    },
                )
                if number not in item["source_lines"]:
                    item["source_lines"].append(number)
                if anchor and anchor not in item["anchors"]:
                    item["anchors"].append(anchor)
    edges.extend(found[k] for k in sorted(found))
    return {
        "schema_version": 1,
        "directed": True,
        "scope": "tracked_public_markdown_navigation_only",
        "canonical_repository": REPOSITORY,
        "assurance": "navigation_only_not_semantic_or_formal_proof",
        "source_rule": "Tracked non-hidden Markdown; generated graphs/ excluded to avoid circular identity. Only simple inline links outside frontmatter/fences/code spans are parsed, not complete CommonMark. Links collapse at document level; source lines and anchors retained.",
        "semantic_extraction_tokens": 0,
        "nodes": nodes,
        "links": edges,
    }


def verify(root):
    expected = build(root)
    actual = json.loads((root / OUTPUT).read_text(encoding="utf-8"))
    if actual != expected:
        raise ValueError(
            "stale or incomplete canonical navigation; regenerate and review"
        )
    ids = {n["id"] for n in actual["nodes"]}
    if len(ids) != len(actual["nodes"]):
        raise ValueError("duplicate node")
    if any(e["source"] not in ids or e["target"] not in ids for e in actual["links"]):
        raise ValueError("missing edge endpoint")
    return len(actual["nodes"]), len(actual["links"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    if args.write:
        out = root / OUTPUT
        out.parent.mkdir(exist_ok=True)
        out.write_text(
            json.dumps(build(root), indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
    nodes, edges = verify(root)
    print(
        f"PASS: {nodes} public navigation nodes, {edges} explicit links; no semantic proof."
    )


if __name__ == "__main__":
    main()
