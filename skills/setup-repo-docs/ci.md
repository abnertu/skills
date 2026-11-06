# CI conventions

Add the shared naming rules and the repo's host block to `## CI` in `AGENTS.md`.
Replace `<tag-pattern>` with the repo's tag format.
In `optimize` mode, keep an existing CI layout that implements the same rule.

## Shared naming rules

```markdown
- Name CI files in kebab-case by purpose, such as `deploy-production.yml`.
- Keep reserved host filenames, including `.gitlab-ci.yml`.
- Name workflows in Title Case, such as `Deploy Production`.
- Keep the repository name out of workflow names.
- Name job IDs in snake_case, such as `build_image`.
- Start each GitHub step name with a verb, such as `Install Dependencies` or `Run Tests`.
- Preserve proper nouns and code identifiers when applying case.
- Prefer a specific purpose, such as `deploy-production.yml`, over a vague name, such as `production.yml`.
- Omit redundant host or artifact words, as in `github-action-build.yml` and `build-workflow.yml`.
- Name each workflow, job and step by its target and action.
- Keep job display names unique within the repository.
- Update dispatch references, dependencies, release gates, required check contexts and badges together when renaming CI artifacts.
```

## GitLab

````markdown
- Keep the dot prefix on hidden job IDs, and use snake_case after it.
- Apply step-name rules only where the CI host exposes named steps.
- Make each check job extend `.branch_pipeline_only`:
  ```yaml
  .skip_tag_pipeline:
    rules:
      - if: $CI_COMMIT_TAG
        when: never
  .branch_pipeline_only:
    rules:
      - !reference [.skip_tag_pipeline, rules]
      - when: on_success
  ```
- A job's own `rules` replace the inherited `rules`. Start such a job's `rules` with `- !reference [.skip_tag_pipeline, rules]`. Never reference `.branch_pipeline_only` there: its last rule matches before the job's own rules.
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
