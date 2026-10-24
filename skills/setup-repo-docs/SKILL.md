---
name: setup-repo-docs
description: Write a repo's README.md (user-facing) and AGENTS.md (agent-facing). Append a mode (`rewrite` or `optimize`) and optionally a README language, e.g. `optimize 中文`.
argument-hint: "[rewrite|optimize] [language]"
disable-model-invocation: true
---

Write `README.md` for users and `AGENTS.md` for agents in the current repo. Reconcile the other docs with them.

## 1. Settle the mode and README language

Read the mode and the language from the text after the skill name. If a value is missing and this step gives no default, ask for it in one question and wait.

- **Mode** applies when a `README.md` or `AGENTS.md` exists. If neither exists, write both fresh and skip the mode.
  - `rewrite` (`重寫`): this skill is authoritative. Its structure and rules replace the existing docs. The existing docs still supply facts.
  - `optimize` (`優化`): the repo is authoritative. Keep what is still accurate and merge it into the new structure. If a repo convention conflicts with the template, keep the repo's convention. List the conflict for the user.
  - Some rules need judgment: which sections to split, which docs need pointers, how complete a list is and which badges to show. If the existing docs already made such a call, keep it in both modes.
- **Language** sets the README language (`中文`, `English`, `日本語`, ...). If no language is given, use the language of the existing `README.md`. Match the script of the keyword: `中文` is Traditional Chinese and `中文简体` is Simplified Chinese. Write `AGENTS.md` in English always.

## 2. Survey the repo

Read the package manifest, such as `package.json`, `pyproject.toml` or `Cargo.toml`. Lockfiles and CI files are not manifests. Also read the existing docs, the CI config and the entry points. Collect what the project is, how to install it and how to use it.

Identify the host from `git remote get-url origin`. It is GitHub or GitLab, either gitlab.com or a self-hosted instance. A `.gitlab-ci.yml` also signals GitLab. Note the owner or namespace, the project name and the default branch. GitLab namespaces can contain subgroups. If there is no remote, or the host is neither, ask the user.

Dig for `AGENTS.md` facts: unwritten conventions, gotchas and the reasons behind choices. Look in these places:

- Git history: reverts, repeated fixes to one spot and commit bodies that explain a choice.
- Code signals: `HACK`, `FIXME`, comments that say "must" or "never", `scripts/`, `.env.example` and unusual CI steps.
- The existing docs.

Show the candidates to the user with their sources. Ask which candidates hold and what else is unwritten. Only confirmed facts go into `AGENTS.md`.

This step is done when all of these are true:

- You can state the project's purpose in one sentence.
- You can name the install and usage commands from the files. Ask the user for what the files do not settle, as in a new repo.
- You can name the host, the namespace, the project and the default branch.
- Each candidate fact has a source: a `file:line`, a commit or the user.

## 3. Plan the other docs

Sort each other doc into one kind and plan its action:

| Kind | Examples | Action |
| --- | --- | --- |
| Agent instructions that tools load for this repo | `CLAUDE.md`, `GEMINI.md`, `.cursorrules`, `.github/copilot-instructions.md` | Merge them into `AGENTS.md`. Reduce `CLAUDE.md` to the single line `@AGENTS.md`. Propose to delete the others. |
| User docs that overlap the README | `docs/installation.md`, `docs/usage.md` | Keep the short form in the README and link to the doc. |
| Contributor docs that overlap `AGENTS.md` | `CONTRIBUTING.md`, `docs/development.md` | Put each shared rule in one of the two files. Link to it from the other. |
| All other docs | `CHANGELOG.md`, `SECURITY.md`, ADRs, API docs, files that the repo installs elsewhere | Keep their content. Note the problems you find, such as stale commands or contradictions, for the report. |

Everyday readers skip some sections completely. Move such a section from the README or `AGENTS.md` to `docs/` and leave a one-line link.

Rewrite the wording of each other doc to the writing rules in the template's `## Docs` section. Change only the wording, not the facts or the rules. Keep these parts unchanged:

- Headings, because links point to their anchors.
- Code blocks, and text that tests or tools read.
- Measured data and release history.
- Generated files, such as a changelog that a tool builds from commits.

This step is done when each doc has a kind and a planned action.

## 4. Draft `README.md`

Write for a reader who decides whether to use the project, and then uses it:

1. Title and one-line description.
2. Badges. Build them with [`badges.md`](badges.md).
3. Install. List the requirements that users install separately. Base system utilities are not requirements.
4. Usage: the shortest real example that works.

Add a section only when users need it, such as configuration or supported platforms. Put the contributor workflow in `AGENTS.md`.

For a non-English README, write the English draft first, then translate it as the template's `## Docs` section describes. Write only the translation to the repo.

This step is done when each command and path in the draft comes from the survey.

## 5. Draft `AGENTS.md`

Start from the template below. Keep each section, also the sections that the repo does not use yet: each one sets the rule for later. In `optimize` mode, a conflicting repo convention replaces the template rule.

- Add the confirmed repo facts that an agent cannot find by looking.
- Leave out a line that only restates the manifest, the config or the directory layout. Keep a line that adds a reason, an intent or a prohibition. In `rewrite` mode, apply this rule to the existing lines too.
- Put a fact about Git, tests or CI in that section. Group the other facts under `##` headings by topic. Existing lines and sections keep their place.
- Under `## Docs`, give one pointer to each doc that an agent needs, other than `README.md`. A directory of similar guides gets one pointer. Example: `Read docs/architecture.md before you change module boundaries.` Move such pointers to `## Docs` from other parts of the file.
- Put the sources in your report to the user, not in the file.

```markdown
# AGENTS Instructions

## Git

- Write commits in [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/) format.
- For a non-trivial change, write a commit body that explains why.
- Mark a breaking change with `!` and a `BREAKING CHANGE:` footer.
- Author commits as the user alone, without `Co-Authored-By` or other co-author trailers.
- Commit as the plan progresses.
- Before you push, squash related commits into one commit to keep the history clean.
- Push only after the user approves that push.
- Version releases with [Semantic Versioning 2.0.0](https://semver.org/).

## Tests

- Add a test to the repo only when it guards behavior that no existing test covers.
- The test must fail when that behavior breaks. Weigh this before you add each test.
- Run throwaway tests freely to check your work.
- Keep throwaway tests out of the repo unless they meet the bar above.

## CI

- Keep a CI check only when it catches a concrete failure that no existing check covers.
- Identify that failure before you add or keep the check.
- Apply the test rules to CI checks too.
- Run the repo's entry points against real inputs or isolated fixtures.
- Reject duplicate checks, source-text assertions, copied inventories and checks that only prove that a command or file exists.
- Name each workflow, job and step by its target and its action.
- Propagate command failures.
- Count a missing prerequisite or skipped required coverage as a failure.
- After you change these rules, audit the repo against them.
- Validate changes locally. Then verify the required CI on the pushed commit.
- Report each uncovered contract and each unavailable check.

## Docs

- Keep each doc concise and plain. Each sentence must carry information.
- Write English docs in US English, to the [ASD-STE100](https://www.asd-ste100.org/) writing rules:
  - Give one instruction in each sentence.
  - Write instructions in the imperative and in the active voice.
  - Use one word for one meaning, and one meaning for one word.
  - An instruction has 20 words or fewer. A description has 25 words or fewer.
- Review each sentence over these limits. Split it if it holds more than one instruction or fact. A list of items can stay in one sentence. Make a bullet list from more than five items.
- Write a non-English doc in two passes:
  1. Write an English draft to these rules.
  2. Translate the draft. Keep its sentence boundaries and one term for each concept. Keep commands, paths and code unchanged. Use the natural word order of the target language.
```

This step is done when each template rule is present, or a repo convention replaces it in `optimize` mode. Each added fact must be confirmed.

## 6. Review

Run `python3 <skill-dir>/scripts/check-sentences.py FILE...` on each English doc that you drafted or rewrote. `<skill-dir>` is the directory of this `SKILL.md`. For a translated doc, check its English draft in a temporary file outside the repo. The script lists the sentences over 20 words.

Read the drafts again and check these points:

- Each sentence carries information.
- Each listed sentence is a description of 25 words or fewer, or a single list of items. Split the others.
- Each English sentence obeys the other writing rules in the template's `## Docs` section.
- A prohibition that repeats the positive instruction before it is deleted. Prohibitions stay only as guardrails, such as for secrets.
- The README is in the settled language. A translation reads naturally and uses one term for each concept.
- `AGENTS.md` holds each template rule or its repo replacement.
- The doc pointers are under `## Docs`.
- Each action from step 3 is done.

Verify each badge as [`badges.md`](badges.md) describes.

## 7. Write and commit

In `rewrite` mode, or when no docs exist, write the docs directly. In `optimize` mode, show the diff and the listed conflicts. Write after the user approves.

To create, move or delete any other file, get approval in each mode. List each file with its reason.

After a move, merge or deletion, search the repo for links to the old paths and anchors. Fix those links.

Run `git diff --check`. Also run the checks that the repo's `AGENTS.md` prescribes for doc changes. If it names none, run its general validation. Fix the failures.

Commit all changes in one commit. Use a Conventional Commits `docs:` message, or the repo's own convention in `optimize` mode. Push only after the user approves.

Report the commit, the badge results, the fact sources and the problems that you noted in the other docs.
