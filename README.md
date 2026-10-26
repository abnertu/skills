# skills

Personal agent skills. Each skill is a `SKILL.md` that Claude Code and other agents load.

[![check](https://github.com/abnertu/skills/actions/workflows/check.yml/badge.svg?branch=main)](https://github.com/abnertu/skills/actions/workflows/check.yml)

## Skills

| Skill | Purpose |
| --- | --- |
| [`converge`](skills/converge/SKILL.md) | Plan a change, review the plan until a review finds nothing in scope, then build and verify it |
| [`setup-agent-prefs`](skills/setup-agent-prefs/SKILL.md) | Apply abnertu's preferences to Claude Code and Codex |
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

Invoke a skill by its name. For `converge`, append the task. Append `codex` to use Codex for reviews and delegated work. Codex use needs Claude Code with [codex-plugin-cc](https://github.com/openai/codex-plugin-cc).

For `setup-repo-docs`, append a mode. Optionally, append a README language. Without it, the skill keeps the language of the existing README:

- `rewrite` replaces the existing docs with the skill's structure.
- `optimize` keeps the repo's conventions and asks before it writes.

| Agent | Command |
| --- | --- |
| Claude Code | `/abnertu-skills:setup-repo-docs optimize English` |
| Codex | `$setup-repo-docs optimize English`, or pick it from `/skills` |
