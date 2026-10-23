# Badges

Reference for the README badge row in [`SKILL.md`](SKILL.md).

## Which badges

One row under the description, in this order. Each fact gets its badge once its subject exists, and the row holds only these:

1. **CI**: one badge for the workflow or pipeline that builds and tests the default branch, with the workflow's `name` as alt text.
2. **Version**, from where users get the project: the registry's shields.io badge (`npm/v/<package>`, `pypi/v/<package>`, `crates/v/<crate>`) linking to the package page; else the host's latest release when it has published releases (bare tags do not count); else none.
3. **Runtime**: exactly one, what the project runs on or in (Node.js, Python, Deno, a browser, an OS), linking to the homepage its own repository lists. When several qualify, take the one every install needs.
4. **Framework**: the base, other than the runtime, that the README description or the manifest names and whose replacement means a rewrite (Next.js, Django, Rails), linking to its site or else its repository. None when nothing is named. Languages, supporting libraries, plugins and package managers (TypeScript, Tailwind, npm) stay in the manifest.

## Host formats

Prefer the host's native badge; fall back to shields.io where it has none.

| Badge | Host | Image | Link |
| --- | --- | --- | --- |
| CI | GitHub | `https://github.com/<owner>/<repo>/actions/workflows/<file>/badge.svg?branch=<branch>` | `https://github.com/<owner>/<repo>/actions/workflows/<file>` |
| CI | GitLab | `https://<host>/<namespace>/<project>/badges/<branch>/pipeline.svg` | `https://<host>/<namespace>/<project>/-/pipelines?ref=<branch>` |
| Release | GitHub | `https://img.shields.io/github/v/release/<owner>/<repo>` | `https://github.com/<owner>/<repo>/releases/latest` |
| Release | GitLab | `https://<host>/<namespace>/<project>/-/badges/release.svg` | `https://<host>/<namespace>/<project>/-/releases` |
| Manifest raw file | GitHub | `https://raw.githubusercontent.com/<owner>/<repo>/<branch>/<path>` | |
| Manifest raw file | GitLab | `https://<host>/<namespace>/<project>/-/raw/<branch>/<path>` | |

## Versions and style

- Read runtime and framework versions from the manifest (`engines.node`, `project.requires-python`, the framework's dependency entry) through a shields.io dynamic badge (`dynamic/json`, `dynamic/toml`, `dynamic/yaml`) whose URL-encoded `url` is the manifest raw file.
- Without a manifest version, use a static badge with the minimum version the docs or the host's repository description state, else the name alone. Use the name alone too when shields.io cannot fetch the manifest (private repo, internal host). The message is a version only, never an architecture.
- Static badges: `https://img.shields.io/badge/<label>-<message>-<color>`, or `<label>-<color>` for a name alone. In each part write `_` for a space, `__` for an underscore, `--` for a dash and `%2B` for `+`.
- Runtime and framework badges carry the brand's simple-icons logo and main color, with `logoColor=white`: the logo sits on the dark gray label, while shields.io picks the message text color itself. `https://img.shields.io/badge/Node.js-20%2B-5FA04E?logo=nodedotjs&logoColor=white`. A brand without a simple-icons logo gets no logo and `blue`.

## Verify

Fetch every badge image with `curl -sL`. A badge passes on HTTP 200 with an SVG showing a real value. shields.io answers 200 even on failure, so fail its badge when the `<title>` reads `not found`, `invalid` or `inaccessible`; fail a GitLab badge reading `unknown`. Fix and refetch failures. On a private repo, or one not yet pushed, report badges that cannot be fetched as unverified.
