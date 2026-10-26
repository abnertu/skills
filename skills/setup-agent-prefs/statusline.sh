#!/usr/bin/env bash
# Claude Code status line: directory · branch · model · context · 5-hour and 7-day limits.
input=$(cat)
field() { jq -r "$1 // empty" <<<"$input"; }

dir=$(field '.workspace.current_dir // .cwd')
branch=$(git -C "$dir" --no-optional-locks branch --show-current 2>/dev/null)
sep=$(printf ' \033[2m·\033[0m ')

# Print the time until a Unix timestamp, or nothing when it has passed.
remaining() {
  local s=$(( $1 - $(date +%s) ))
  (( s <= 0 )) && return
  if (( s >= 86400 )); then
    printf ' (%dd%dh)' $((s / 86400)) $((s % 86400 / 3600))
  else
    printf ' (%dh%dm)' $((s / 3600)) $((s % 3600 / 60))
  fi
}

# Print a dim usage segment with the time until its reset.
limit() {
  local used=$1 reset=$2 label=$3
  [[ -n $used ]] || return
  printf '%s\033[2m%s %.0f%%%s\033[0m' "$sep" "$label" "$used" "$([[ -n $reset ]] && remaining "$reset")"
}

out=$(printf '\033[36m%s\033[0m' "${dir##*/}")
[[ -n $branch ]] && out+="$sep$(printf '\033[32m%s\033[0m' "$branch")"
out+="$sep$(printf '\033[2m%s\033[0m' "$(field '.model.display_name')")"
used=$(field '.context_window.used_percentage')
[[ -n $used ]] && out+="$sep$(printf '\033[2mctx %.0f%%\033[0m' "$used")"
out+=$(limit "$(field '.rate_limits.five_hour.used_percentage')" "$(field '.rate_limits.five_hour.resets_at')" 5h)
out+=$(limit "$(field '.rate_limits.seven_day.used_percentage')" "$(field '.rate_limits.seven_day.resets_at')" 7d)
echo "$out"
