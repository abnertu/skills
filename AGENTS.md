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
- For a non-trivial change, write a commit body that explains why.
- Mark a breaking change with `!` and a `BREAKING CHANGE:` footer.
- Author commits as the user alone, without `Co-Authored-By` or other co-author trailers.
- Commit as the plan progresses.
- Before you push, squash related commits into one commit to keep the history clean.
- Push only after the user approves that push.
- Version releases with [Semantic Versioning 2.0.0](https://semver.org/) in the `version` of `.claude-plugin/plugin.json`. Installed plugins update only when it changes.

## Tests

- Add a test to the repo only when it guards behaviour that no existing test covers.
- The test must fail when that behaviour breaks. Weigh this before you add each test.
- Run throwaway tests freely to check your work.
- Keep throwaway tests out of the repo unless they meet the bar above.

## Docs

- Keep each doc concise and plain. Each sentence must carry information.
- Write English docs to the [ASD-STE100](https://www.asd-ste100.org/) writing rules:
  - An instruction has 20 words or fewer. A description has 25 words or fewer.
  - Give one instruction in each sentence.
  - Write instructions in the imperative and in the active voice.
  - Use one word for one meaning, and one meaning for one word.
