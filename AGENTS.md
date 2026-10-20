# AGENTS Instructions

## Skills

- Each skill lives in `skills/<name>/SKILL.md`; the directory name matches the frontmatter `name`.
- Every skill runs in both Claude Code and Codex. Put Claude Code settings in `SKILL.md` frontmatter and Codex settings in `agents/openai.yaml`; a user-invoked skill sets both `disable-model-invocation: true` and `policy.allow_implicit_invocation: false`.
- Read arguments from the text after the skill name. Codex documents no argument substitution, so skills avoid `$ARGUMENTS`.
- Load the `writing-for-agents` skill before creating or editing a skill or this file.

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
