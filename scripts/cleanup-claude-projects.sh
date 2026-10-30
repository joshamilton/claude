#!/bin/bash
set -euo pipefail

CLAUDE_DIR="$HOME/.claude"
ALLOWLIST_FILE="/Users/joshamilton/Documents/repos/claude-v2/config/project-allowlist.txt"

allowed_prefixes=()
while IFS= read -r pattern; do
    case "$pattern" in
        ""|\#*) continue ;;
    esac
    for dir in $pattern; do
        [ -d "$dir" ] || continue
        allowed_prefixes+=("${dir//\//-}")
    done
done < "$ALLOWLIST_FILE"

is_allowed() {
    local name="$1" prefix
    for prefix in "${allowed_prefixes[@]}"; do
        if [ "$name" = "$prefix" ] || [[ "$name" == "$prefix"-* ]]; then
            return 0
        fi
    done
    return 1
}

clear_dir_contents() {
    local dir="$1"
    [ -d "$dir" ] || return 0
    find "$dir" -mindepth 1 -maxdepth 1 -exec rm -rf {} +
}

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

removed_count=0
removed_onsite_claude_count=0

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
        rm -rf "$CLAUDE_DIR/session-env/$uuid"
        rm -rf "$CLAUDE_DIR/file-history/$uuid"
        rm -f "$CLAUDE_DIR/debug/$uuid.txt"
        for todo in "$CLAUDE_DIR/todos/${uuid}"*.json; do
            [ -f "$todo" ] || continue
            rm -f "$todo"
        done

        cwd="$(session_cwd "$jsonl")"
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
        if [ -d "$onsite_claude_dir" ]; then
            rm -rf "$onsite_claude_dir"
            removed_onsite_claude_count=$((removed_onsite_claude_count + 1))
        fi
    done

    rm -rf "$project_dir"
    removed_count=$((removed_count + 1))
done

clear_dir_contents "$CLAUDE_DIR/plans"
clear_dir_contents "$CLAUDE_DIR/ide"
clear_dir_contents "$CLAUDE_DIR/sessions"
clear_dir_contents "$CLAUDE_DIR/shell-snapshots"

echo "Removed $removed_count project(s) outside the allowlist and $removed_onsite_claude_count on-disk .claude folder(s)."
