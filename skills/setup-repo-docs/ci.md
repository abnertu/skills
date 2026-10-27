# CI host lines

Add the block for the repo's host to `## CI` in `AGENTS.md`. Replace `<tag-pattern>` with the tag format of the repo. In `optimize` mode, keep a CI layout that the repo already uses for the same rule.

## GitLab

````markdown
- Make each check job extend `.branch-pipeline-only`:
  ```yaml
  .skip-tag-pipeline:
    rules:
      - if: $CI_COMMIT_TAG
        when: never
  .branch-pipeline-only:
    rules:
      - !reference [.skip-tag-pipeline, rules]
      - when: on_success
  ```
- A job's own `rules` replace the inherited `rules`. Start such a job's `rules` with `- !reference [.skip-tag-pipeline, rules]`. Never reference `.branch-pipeline-only` there: its last rule matches before the job's own rules.
- Run release jobs only with `if: $CI_COMMIT_TAG =~ <tag-pattern>`.
- Set `GIT_DEPTH: "0"` in release jobs. A tag pipeline fetches only the tag, so fetch `$CI_DEFAULT_BRANCH` before the ancestry check.
- Protect the release tag pattern. Protected variables reach only protected refs.
````

## GitHub

````markdown
- Run the checks in a workflow on `pull_request` and on `push` to branches.
- Run the release in a separate workflow on `push` of tags that match `<tag-pattern>`. GitHub tag filters are globs, such as `[0-9]+.[0-9]+.[0-9]+` and `[0-9]+.[0-9]+.[0-9]+-*`.
- Check out release jobs with `fetch-depth: 0`, so that the ancestry check sees the default branch.
- Keep release secrets in an environment that allows only the release tags. Protect the tags with a tag ruleset.
````
