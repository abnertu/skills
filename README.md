# skills

Personal agent skills. Each skill is a `SKILL.md` that Claude Code and other agents load.

## Skills

| Skill | Purpose |
| --- | --- |
| [`setup-repo-docs`](skills/setup-repo-docs/SKILL.md) | Write a repo's user-facing `README.md` and agent-facing `AGENTS.md` |

## Install

Claude Code:

```sh
claude plugin marketplace add abnertu/skills
claude plugin install abnertu-skills@abnertu
```

Codex:

```sh
codex plugin marketplace add abnertu/skills
codex plugin add abnertu-skills@abnertu
```

## Usage

Invoke a skill by its name. For `setup-repo-docs`, append a mode and a README language:

- `rewrite` replaces the existing docs with the skill's structure.
- `optimize` keeps the repo's conventions and asks before it writes.

| Agent | Command |
| --- | --- |
| Claude Code | `/abnertu-skills:setup-repo-docs optimize English` |
| Codex | `$setup-repo-docs optimize English`, or pick it from `/skills` |
