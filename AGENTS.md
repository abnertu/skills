# AGENTS Instructions

## Skills

- Put each skill in `skills/<name>/SKILL.md`. The directory name must match the frontmatter `name`.
- `.claude-plugin/` packages the repo as one plugin for both Claude Code and Codex. List each skill directory in `skills` of `plugin.json`.
- Each skill must run in both Claude Code and Codex. Put Claude Code settings in the `SKILL.md` frontmatter and Codex settings in `agents/openai.yaml`.
- A user-invoked skill sets both `disable-model-invocation: true` and `policy.allow_implicit_invocation: false`.
- Read arguments from the text after the skill name. Codex documents no argument substitution, so do not use `$ARGUMENTS`.
- Quote a frontmatter value that starts with `[` or `{`. Otherwise YAML reads it as a sequence or a mapping.
- Load the `writing-for-agents` skill before you create or edit a skill or this file.

## Git

- Write commits in [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/) format.
- Start the type, the scope and the description in lowercase. Keep the case of code identifiers and proper nouns.
- For a non-trivial change, write a commit body that explains why.
- Mark a breaking change with `!` and a `BREAKING CHANGE:` footer.
- Author commits as the user alone. Add no agent trailers or links, such as `Co-Authored-By` or a session URL.
- Commit as the plan progresses.
- Before you push, squash related commits into one commit to keep the history clean.
- Push only after the user approves that push.
- Version releases with [Semantic Versioning 2.0.0](https://semver.org/) in the `version` of `.claude-plugin/plugin.json`. Installed plugins update only when it changes.

## Tests

- Add a test to the repo only when it guards behavior that no existing test covers.
- The test must fail when that behavior breaks. Weigh this before you add each test.
- Run throwaway tests freely to check your work.
- Keep throwaway tests out of the repo unless they meet the bar above.
- Before you push, run `scripts/check-skills.py`. CI runs it too. It needs PyYAML.

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
