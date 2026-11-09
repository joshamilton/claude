#!/bin/bash
#
# cleanup-claude-projects.sh
#
# Removes Claude projects that are not on the allowlist, plus the session files
# that belong to them and the project's own .claude folder. Also empties the
# plans, ide, sessions and shell-snapshots folders in ~/.claude.
#
# What is allowed is decided by comparing names as text. The disk is never read
# to make that decision. Each allowlist line is turned into a project-name
# pattern with the same rule Claude uses for folder names: every character that
# is not a letter or a digit becomes "-". The glob characters [ ] * ? are kept.
# A project is allowed when its name equals a pattern, or starts with a pattern
# followed by "-".
#
# Environment variables (for testing against a scratch copy):
#   CLAUDE_DIR      Claude data folder (default: $HOME/.claude)
#   ALLOWLIST_FILE  Allowlist file (default: $HOME/.local/share/claude-cleanup/project-allowlist.txt)
#
# Exit status: 0 when everything worked, 1 when the allowlist is missing or empty
# (nothing is deleted) or when something could not be removed.

set -uo pipefail
export LC_ALL=C

CLAUDE_DIR="${CLAUDE_DIR:-$HOME/.claude}"
ALLOWLIST_FILE="${ALLOWLIST_FILE:-$HOME/.local/share/claude-cleanup/project-allowlist.txt}"

name_patterns=()
error_count=0

# Read the allowlist and fill name_patterns. Returns 1 if the file cannot be read
# or contains no patterns.
load_allowlist() {
    local line
    name_patterns=()

    if [ ! -r "$ALLOWLIST_FILE" ]; then
        echo "Error: cannot read the allowlist file: $ALLOWLIST_FILE" >&2
        return 1
    fi

    while IFS= read -r line || [ -n "$line" ]; do
        case "$line" in
            ""|\#*) continue ;;
        esac
        line="${line%"${line##*[![:space:]]}"}"
        while [ "${line%/}" != "$line" ]; do
            line="${line%/}"
        done
        [ -n "$line" ] || continue
        name_patterns+=("${line//[^][A-Za-z0-9*?-]/-}")
    done < "$ALLOWLIST_FILE"

    if [ "${#name_patterns[@]}" -eq 0 ]; then
        echo "Error: the allowlist has no entries: $ALLOWLIST_FILE" >&2
        return 1
    fi
    return 0
}

# Succeeds when the project name matches an allowlist pattern.
is_allowed() {
    local name="$1" pat
    for pat in "${name_patterns[@]}"; do
        # shellcheck disable=SC2053
        if [[ "$name" == $pat ]] || [[ "$name" == $pat-* ]]; then
            return 0
        fi
    done
    return 1
}

# Remove a path. On failure, print one error line and count it.
remove_path() {
    local target="$1" msg
    if msg="$(rm -rf "$target" 2>&1)"; then
        return 0
    fi
    echo "Error: could not remove $target: $msg" >&2
    error_count=$((error_count + 1))
    return 1
}

# Empty a folder but keep the folder itself.
clear_dir_contents() {
    local dir="$1" msg
    [ -d "$dir" ] || return 0
    if ! msg="$(find "$dir" -mindepth 1 -maxdepth 1 -exec rm -rf {} + 2>&1)"; then
        echo "Error: could not empty $dir: $msg" >&2
        error_count=$((error_count + 1))
    fi
    return 0
}

# Print the working folder recorded in a session file.
session_cwd() {
    python3 -I -c "
import json, sys

with open(sys.argv[1]) as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            d = json.loads(line)
        except json.JSONDecodeError:
            continue
        if 'cwd' in d:
            print(d['cwd'])
            break
" "$1"
}

main() {
    local removed_count=0
    local removed_onsite_claude_count=0
    local project_dir name jsonl uuid todo cwd already_seen seen onsite_claude_dir
    local cwd_list

    if ! load_allowlist; then
        exit 1
    fi

    for project_dir in "$CLAUDE_DIR/projects"/*/; do
        [ -d "$project_dir" ] || continue
        name="$(basename "$project_dir")"

        if is_allowed "$name"; then
            continue
        fi

        cwd_list=()

        for jsonl in "$project_dir"*.jsonl; do
            [ -f "$jsonl" ] || continue
            uuid="$(basename "$jsonl" .jsonl)"
            if [ -n "$uuid" ]; then
                remove_path "$CLAUDE_DIR/session-env/$uuid" || true
                remove_path "$CLAUDE_DIR/file-history/$uuid" || true
                remove_path "$CLAUDE_DIR/debug/$uuid.txt" || true
                for todo in "$CLAUDE_DIR/todos/${uuid}"*.json; do
                    [ -f "$todo" ] || continue
                    remove_path "$todo" || true
                done
            fi

            cwd="$(session_cwd "$jsonl" || true)"
            if [ -n "$cwd" ]; then
                already_seen=false
                for seen in "${cwd_list[@]:-}"; do
                    if [ "$seen" = "$cwd" ]; then
                        already_seen=true
                        break
                    fi
                done
                [ "$already_seen" = true ] || cwd_list+=("$cwd")
            fi
        done

        for cwd in "${cwd_list[@]:-}"; do
            [ -n "$cwd" ] || continue
            onsite_claude_dir="$cwd/.claude"
            if [ "$onsite_claude_dir" = "$CLAUDE_DIR" ] || [ "$onsite_claude_dir" = "$HOME/.claude" ]; then
                echo "Skipped $onsite_claude_dir: it is the Claude data folder itself."
                continue
            fi
            if [ -d "$onsite_claude_dir" ]; then
                if remove_path "$onsite_claude_dir"; then
                    removed_onsite_claude_count=$((removed_onsite_claude_count + 1))
                fi
            fi
        done

        if remove_path "$project_dir"; then
            removed_count=$((removed_count + 1))
        fi
    done

    clear_dir_contents "$CLAUDE_DIR/plans"
    clear_dir_contents "$CLAUDE_DIR/ide"
    clear_dir_contents "$CLAUDE_DIR/sessions"
    clear_dir_contents "$CLAUDE_DIR/shell-snapshots"

    echo "Removed $removed_count project(s) outside the allowlist and $removed_onsite_claude_count on-disk .claude folder(s)."

    if [ "$error_count" -ne 0 ]; then
        echo "Error: $error_count item(s) could not be removed. See the error output." >&2
        exit 1
    fi
}

# Run main only when the file is executed, not when it is sourced for testing.
if [ "${BASH_SOURCE[0]}" = "$0" ]; then
    main
fi
