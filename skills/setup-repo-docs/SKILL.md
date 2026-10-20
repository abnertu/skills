---
name: setup-repo-docs
description: Write a repository's README.md (user-facing) and AGENTS.md (agent-facing). Append a language keyword to set the README language, e.g. `中文`.
argument-hint: [language]
disable-model-invocation: true
---

Write two documents for the current repository: `README.md` for users and `AGENTS.md` for agents. Every sentence in both carries information; cut filler, restatement and marketing.

## 1. Survey the repo

Read the manifest, existing docs, license, CI config and entry points. Collect what the project is, how to install it, how to use it, and its license. When a `README.md` or `AGENTS.md` already exists, treat its content as source material: keep what is still accurate, merge it into the new structure.

Done when you can state the project's purpose in one sentence and name its install and usage commands from the files themselves.

## 2. Settle the README language

A language keyword after the skill name sets it (`中文`, `English`, `日本語`, ...); match the script it is written in (`中文` → Traditional Chinese, `中文简体` → Simplified Chinese). With no keyword, ask the user and wait. `AGENTS.md` is always English.

## 3. Write `README.md`

Written for someone deciding whether to use the project, then using it:

1. Title and one-line description.
2. Badges: core facts only, each linking to its official page: license, CI status, published package version, primary runtime. Leave out convention badges (SemVer, Conventional Commits) and per-dependency badges. Three or four at most.
3. Install.
4. Usage: the shortest real example that works.
5. License.

Add a section only when users need it (configuration, supported platforms). Contributor workflow belongs in `AGENTS.md`.

## 4. Write `AGENTS.md`

Start from this template. Add repo-specific facts an agent cannot find by looking (unwritten conventions, gotchas, the reason behind a choice); leave out what the manifest, config or directory layout already states.

```markdown
# AGENTS Instructions

## Git

- Write commits in [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/) format.
- Author commits as the user alone, with no `Co-Authored-By` or other co-author trailers.
- Commit as the plan progresses. Before pushing, squash related commits into one to keep history clean.
- Push only after the user approves that push.
- Version releases with [Semantic Versioning 2.0.0](https://semver.org/).

## Tests

- A test enters the repo only when it guards behaviour no existing test covers and fails when that behaviour breaks. Weigh this before adding each one.
- Run throwaway tests freely to check your work; keep them out of the repo unless they pass that bar.

## Docs

- Keep this file, `README.md` and every other doc concise and plain: each sentence carries information, with no filler.
```

## 5. Review

Reread both files against the bar: every sentence informs, README is in the settled language, badges are core-only and link to official pages, `AGENTS.md` contains every template rule. Show the user both files.
