---
name: setup-agent-prefs
description: Apply abnertu's personal preferences to Claude Code and Codex. Sets the status lines, permissions, attribution, theme, marketplaces and plugins, and sets up codex-plugin-cc.
disable-model-invocation: true
---

Apply the same personal preferences to Claude Code and Codex, from either runtime. The files next to this `SKILL.md` hold the wanted values:

| File | Target |
| --- | --- |
| [`claude-settings.json`](claude-settings.json) | Keys in `~/.claude/settings.json` |
| [`statusline.sh`](statusline.sh) | `~/.claude/statusline.sh`, which the `statusLine` key runs |
| [`codex-config.toml`](codex-config.toml) | Keys in `~/.codex/config.toml` |

Change only the keys in these files. Keep each other key, because both tools and the user write to the same files. Never print a secret or read an auth file. Show only the keys that this skill changes, because the settings files can hold tokens.

## 1. Check the prerequisites

Run `command -v claude codex node jq`. The status line needs `jq`, and codex-plugin-cc needs `node`. List each missing command for the user and ask how to install it. Install nothing without approval.

## 2. Plan the changes

Compare each wanted value with the current state:

- **Claude settings**: merge the objects of `claude-settings.json` into `~/.claude/settings.json`. A nested object, such as `attribution`, merges key by key.
- **Status line**: compare `statusline.sh` with `~/.claude/statusline.sh`.
- **Codex config**: compare each key of `codex-config.toml` with `~/.codex/config.toml`. Put a top-level key before the first table header. TOML assigns a key below a header to that table.
- **Marketplaces and plugins**: compare this table with `claude plugin marketplace list`, `claude plugin list`, `codex plugin marketplace list` and `codex plugin list`.

| Tool | Marketplace | Plugins |
| --- | --- | --- |
| Claude Code | `anthropics/claude-plugins-official` | |
| Claude Code | `abnertu/skills` | `abnertu-skills@abnertu` |
| Claude Code | `openai/codex-plugin-cc` | `codex@openai-codex` |
| Codex | `abnertu/skills` | `abnertu-skills@abnertu` |

Add a missing marketplace with `<tool> plugin marketplace add <repo>`. Install a missing plugin with `claude plugin install` or `codex plugin add`. Refresh the present ones with `claude plugin marketplace update`, `claude plugin update <plugin>` and `codex plugin marketplace upgrade`.

This step is done when each difference has a planned edit or command.

## 3. Apply after approval

Show the user each changed key with its old and new value, and each command. Apply the changes after the user approves.

Edit the files in place. Keep the formatting and the comments of `~/.codex/config.toml`. Copy `statusline.sh` to `~/.claude/statusline.sh` and make it executable.

## 4. Set up codex-plugin-cc

Run the setup of the installed plugin:

```sh
node "$(ls -d ~/.claude/plugins/cache/openai-codex/codex/*/ | sort -V | tail -n 1)scripts/codex-companion.mjs" setup --json
```

If Codex is not logged in, ask the user to run `codex login`. In Claude Code, the user types `! codex login`.

## 5. Verify

- Parse both config files. Use `jq empty ~/.claude/settings.json` and `python3 -c 'import tomllib, sys; tomllib.load(open(sys.argv[1], "rb"))' ~/.codex/config.toml`.
- Run `~/.claude/statusline.sh` with a sample JSON input. It must print one line.
- List the plugins of both tools again. Each row of the table must be present.
- The codex-plugin-cc setup must report that Codex is ready.

Report each change, each command result and each step that the user must do. A plugin update applies to new sessions. Tell the user to restart the open sessions.
