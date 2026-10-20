# skills

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

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

Invoke a skill by name. Append a language keyword to set the README language:

| Agent | Command |
| --- | --- |
| Claude Code | `/abnertu-skills:setup-repo-docs English` |
| Codex | `$setup-repo-docs English`, or pick it from `/skills` |

## License

[MIT](LICENSE)
