---
name: setup-repo-docs
description: Write a repository's README.md (user-facing) and AGENTS.md (agent-facing). Append a mode (`rewrite` or `optimize`) and a README language, e.g. `optimize 中文`.
argument-hint: [rewrite|optimize] [language]
disable-model-invocation: true
---

Write two documents for the current repository: `README.md` for users and `AGENTS.md` for agents, reconciling the other docs that overlap them. Every sentence in both carries information.

## 1. Settle the mode and README language

Read both from the text after the skill name. Ask for whichever is missing in one question and wait.

- **Mode** applies when a `README.md` or `AGENTS.md` already exists. With neither, write both fresh and skip it.
  - `rewrite` (`重寫`): this skill is authoritative. Its structure and explicit rules replace the existing docs, which still supply facts.
  - `optimize` (`優化`): the repo is authoritative. Keep what is still accurate and merge it into the new structure. Where an existing convention conflicts with the template, keep the repo's and list the conflict for the user.
  - In both modes, where a rule needs judgment (which sections to split, which docs need pointers, how complete a list is, which runtime or framework a badge shows) and the existing docs already made the call, keep it.
- **Language** sets the README (`中文`, `English`, `日本語`, ...); match the script it is written in (`中文` → Traditional Chinese, `中文简体` → Simplified Chinese). `AGENTS.md` is always English.

## 2. Survey the repo

Read the package manifest (`package.json`, `pyproject.toml`, `Cargo.toml` and the like; lockfiles and CI files are not manifests), existing docs, CI config and entry points. Collect what the project is, how to install it and how to use it.

Identify the host from `git remote get-url origin`: GitHub, or GitLab (gitlab.com or a self-hosted instance, which `.gitlab-ci.yml` also signals). Note the owner or namespace (GitLab namespaces may nest subgroups), the project name and the default branch. With no remote, or a host that is neither, ask the user.

Dig for `AGENTS.md` facts: unwritten conventions, gotchas and reasons behind choices that the code does not state. Look in git history (reverts, repeated fixes to one spot, commit bodies that explain a choice), code signals (`HACK`, `FIXME`, comments saying "must" or "never", `scripts/`, `.env.example`, unusual CI steps) and existing docs. Show the user the candidates with their sources and ask which hold and what else is unwritten; only confirmed facts enter `AGENTS.md`.

Done when you can state the project's purpose in one sentence, name its install and usage commands from the files (asking the user for what the files do not settle, as in a new repo), name the host, namespace, project and default branch, and cite a `file:line`, commit or the user for every candidate fact.

## 3. Plan the other docs

Sort every other doc into one kind and plan its action:

| Kind | Examples | Action |
| --- | --- | --- |
| Agent instructions tools load for this repo | `CLAUDE.md`, `GEMINI.md`, `.cursorrules`, `.github/copilot-instructions.md` | Merge into `AGENTS.md`. Reduce `CLAUDE.md` to the single line `@AGENTS.md`; propose deleting the rest. |
| User docs overlapping the README | `docs/installation.md`, `docs/usage.md` | The README keeps the short form and links to the doc. |
| Contributor docs overlapping `AGENTS.md` | `CONTRIBUTING.md`, `docs/development.md` | Each shared rule lives in one of the two; the other links to it. |
| Everything else | `CHANGELOG.md`, `SECURITY.md`, ADRs, API docs, files the repo installs elsewhere | Leave as is. Note problems you find (stale commands, contradictions) for the report. |

When the README or `AGENTS.md` would carry a section that everyday readers skip whole, move it to `docs/` and leave a one-line link.

Done when every doc has a kind and a planned action.

## 4. Draft `README.md`

Written for someone deciding whether to use the project, then using it:

1. Title and one-line description.
2. Badges, built by [`badges.md`](badges.md).
3. Install. A requirement list names what users install separately, not base system utilities.
4. Usage: the shortest real example that works.

Add a section only when users need it (configuration, supported platforms). Contributor workflow belongs in `AGENTS.md`.

Done when every command and path in the draft comes from the survey.

## 5. Draft `AGENTS.md`

Start from the template below and keep every section, including ones the repo does not use yet: each sets the rule for when it does. In `optimize` mode a conflicting repo convention replaces the template rule.

- Add confirmed repo facts an agent cannot find by looking. A line that only restates what the manifest, config or directory layout holds stays out; one that adds a reason, intent or prohibition stays. In `rewrite` mode this also prunes existing lines.
- Put a fact about Git, tests or CI in that section; group the rest under `##` headings by topic. Existing lines and sections keep their place.
- Under `## Docs`, give each doc an agent needs (other than `README.md`), or each directory of like guides, one pointer: `Read docs/architecture.md before changing module boundaries.` Move such pointers there from elsewhere in the file.
- Sources go in your report to the user, not the file.

```markdown
# AGENTS Instructions

## Git

- Write commits in [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/) format, with a body explaining why for non-trivial changes. Mark breaking changes with `!` and a `BREAKING CHANGE:` footer.
- Author commits as the user alone, with no `Co-Authored-By` or other co-author trailers.
- Commit as the plan progresses. Before pushing, squash related commits into one to keep history clean.
- Push only after the user approves that push.
- Version releases with [Semantic Versioning 2.0.0](https://semver.org/).

## Tests

- A test enters the repo only when it guards behaviour no existing test covers and fails when that behaviour breaks. Weigh this before adding each one.
- Run throwaway tests freely to check your work; keep them out of the repo unless they pass that bar.

## CI

- Keep a CI check only when it catches a concrete failure no existing check covers; identify that failure before adding or retaining it. Apply the test admission rule to CI too.
- Run repository entry points against real inputs or isolated fixtures. Reject duplicate checks, source-text assertions, copied inventories and checks that only prove a command or file exists.
- Name workflows, jobs and steps by their target and action. Propagate command failures; missing prerequisites and skipped required coverage cannot count as success.
- After changing these rules, audit the repository against them. Validate locally, then verify required CI on the pushed commit; report any uncovered contract or unavailable check.

## Docs

- Keep this file, `README.md` and every other doc concise and plain: each sentence carries information, with no filler.
```

Done when every template rule is present, or replaced by a repo convention in `optimize` mode, and every added fact is confirmed.

## 6. Review

Reread both drafts: every sentence informs, the README is in the settled language, `AGENTS.md` holds every template rule or its repo replacement, doc pointers sit under `## Docs`, and every step 3 action is carried out. Verify every badge as [`badges.md`](badges.md) describes.

## 7. Write and commit

In `rewrite` mode, or with no existing docs, write `README.md` and `AGENTS.md` directly. In `optimize` mode, show the diff and the listed conflicts, and write after the user approves. Creating, moving or deleting any other file waits for approval in every mode: list each with its reason.

After a move, merge or deletion, grep the repo for links to the old paths and anchors and fix them. Run `git diff --check` and the checks the repo's `AGENTS.md` prescribes for doc changes (its general validation when it names none); fix failures.

Commit everything in one commit: a Conventional Commits `docs:` message, or the repo's own convention in `optimize` mode. Pushing waits for the user. Report the commit, the badge results, the fact sources and the problems noted in untouched docs.
