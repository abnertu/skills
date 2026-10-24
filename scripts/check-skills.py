#!/usr/bin/env python3
"""Validate the plugin manifests and each skill's metadata.

Usage: check-skills.py [REPO]

Checks that each SKILL.md front matter and agents/openai.yaml parse as YAML,
that the plugin lists exactly the skill directories, and that user-invoked
skills disable invocation in both Claude Code and Codex.
"""
import json
import pathlib
import sys

import yaml


def front_matter(path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("no front matter")
    block, separator, _ = text[4:].partition("\n---\n")
    if not separator:
        raise ValueError("front matter is not closed")
    data = yaml.safe_load(block)
    if not isinstance(data, dict):
        raise ValueError("front matter is not a mapping")
    return data


def check(repo):
    errors = []
    plugin = json.loads((repo / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
    json.loads((repo / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
    listed = {(repo / entry).resolve() for entry in plugin.get("skills", [])}
    present = {path.parent.resolve() for path in (repo / "skills").glob("*/SKILL.md")}
    for missing in sorted(present - listed):
        errors.append(f"{missing.relative_to(repo.resolve())}: not listed in plugin.json")
    for extra in sorted(listed - present):
        errors.append(f"plugin.json: {extra} has no SKILL.md")

    for skill in sorted(present):
        where = skill.relative_to(repo.resolve())
        try:
            meta = front_matter(skill / "SKILL.md")
        except (ValueError, yaml.YAMLError) as error:
            errors.append(f"{where}/SKILL.md: {error}")
            continue
        if meta.get("name") != skill.name:
            errors.append(f"{where}/SKILL.md: name {meta.get('name')!r} differs from the directory")
        if not isinstance(meta.get("description"), str) or not meta["description"].strip():
            errors.append(f"{where}/SKILL.md: description is missing")

        codex = skill / "agents/openai.yaml"
        policy = {}
        if codex.exists():
            try:
                policy = (yaml.safe_load(codex.read_text(encoding="utf-8")) or {}).get("policy", {})
            except (AttributeError, yaml.YAMLError) as error:
                errors.append(f"{where}/agents/openai.yaml: {error}")
                continue
        if meta.get("disable-model-invocation") is True and policy.get("allow_implicit_invocation") is not False:
            errors.append(f"{where}: user-invoked, but agents/openai.yaml allows implicit invocation")
    return errors


if __name__ == "__main__":
    root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    problems = check(root)
    for problem in problems:
        print(problem, file=sys.stderr)
    sys.exit(1 if problems else 0)
