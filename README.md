# skills

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

Personal agent skills. Each skill is a `SKILL.md` that Claude Code and other agents load.

## Skills

| Skill | Purpose |
| --- | --- |
| [`setup-repo-docs`](skills/setup-repo-docs/SKILL.md) | Write a repo's user-facing `README.md` and agent-facing `AGENTS.md` |

## Install

Clone the repo, then link a skill into each agent's user skills directory:

```sh
git clone https://github.com/abnertu/skills.git && cd skills

# Claude Code
ln -s "$PWD/skills/setup-repo-docs" ~/.claude/skills/setup-repo-docs

# Codex
ln -s "$PWD/skills/setup-repo-docs" ~/.agents/skills/setup-repo-docs
```

## Usage

Invoke the skill by name. Append a language keyword to set the README language:

| Agent | Command |
| --- | --- |
| Claude Code | `/setup-repo-docs English` |
| Codex | `$setup-repo-docs English` |

## License

[MIT](LICENSE)
