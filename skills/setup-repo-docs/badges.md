# Badges

Reference for the README badge row in [`SKILL.md`](SKILL.md).

## Which badges

Put one row under the description, in this order. Add each badge when its subject exists. The row holds only these badges:

1. **CI**: one badge for the workflow or pipeline that builds and tests the default branch. Use the workflow's `name` as alt text.
2. **Version**: show the version from the place where users get the project.
   - Use the registry's shields.io badge, such as `npm/v/<package>`, `pypi/v/<package>` or `crates/v/<crate>`. Link it to the package page.
   - If there is no registry, use the host's latest release. Bare tags are not releases.
   - If there is no published release, add no version badge.
3. **Runtime**: exactly one, the platform that the project runs on or in. Examples: Node.js, Python, Deno, a browser, an OS. Link it to the homepage that the runtime's own repo lists. If several runtimes qualify, take the one that each install needs.
4. **Framework**: the base, other than the runtime, that the README description or the manifest names. Replacing it means a rewrite. Examples: Next.js, Django, Rails. Link it to its site, or else to its repo. Add none when nothing is named. Languages, supporting libraries, plugins and package managers are not frameworks. Examples: TypeScript, Tailwind, npm.

## Host formats

Prefer the host's native badge. Use shields.io where the host has none.

| Badge | Host | Image | Link |
| --- | --- | --- | --- |
| CI | GitHub | `https://github.com/<owner>/<repo>/actions/workflows/<file>/badge.svg?branch=<branch>` | `https://github.com/<owner>/<repo>/actions/workflows/<file>` |
| CI | GitLab | `https://<host>/<namespace>/<project>/badges/<branch>/pipeline.svg` | `https://<host>/<namespace>/<project>/-/pipelines?ref=<branch>` |
| Release | GitHub | `https://img.shields.io/github/v/release/<owner>/<repo>` | `https://github.com/<owner>/<repo>/releases/latest` |
| Release | GitLab | `https://<host>/<namespace>/<project>/-/badges/release.svg` | `https://<host>/<namespace>/<project>/-/releases` |
| Manifest raw file | GitHub | `https://raw.githubusercontent.com/<owner>/<repo>/<branch>/<path>` | |
| Manifest raw file | GitLab | `https://<host>/<namespace>/<project>/-/raw/<branch>/<path>` | |

## Versions and style

- Read the runtime and framework versions from the manifest, such as `engines.node`, `project.requires-python` or the framework's dependency entry. Show them with a shields.io dynamic badge: `dynamic/json`, `dynamic/toml` or `dynamic/yaml`. Its `url` parameter is the URL-encoded manifest raw file.
- If the manifest has no version, use a static badge. Show the minimum version that the docs or the host's repo description state. If they state none, show the name alone.
- If shields.io cannot fetch the manifest, show the name alone. Examples: a private repo or an internal host.
- The message shows a version only, never an architecture.
- Static badges: `https://img.shields.io/badge/<label>-<message>-<color>`, or `<label>-<color>` for a name alone. In each part, write `_` for a space, `__` for an underscore, `--` for a dash and `%2B` for `+`.
- Runtime and framework badges carry the brand's simple-icons logo and main color, with `logoColor=white`. Example: `https://img.shields.io/badge/Node.js-20%2B-5FA04E?logo=nodedotjs&logoColor=white`. The logo is on the dark gray label, and shields.io selects the message text color itself.
- If simple-icons has no logo for the brand, use no logo and the color `blue`.

## Verify

Fetch each badge image with `curl -sL`. A badge passes when it returns HTTP 200 and an SVG that shows a real value.

- shields.io returns 200 also on failure. Fail its badge when the `<title>` contains `not found`, `invalid` or `inaccessible`.
- Fail a GitLab badge that shows `unknown`.
- Fix each failure and fetch the badge again.
- On a private repo, or a repo that is not pushed yet, some badges cannot be fetched. Report them as unverified.
