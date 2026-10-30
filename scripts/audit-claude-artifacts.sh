#!/bin/bash
set -uo pipefail

REPO_DIR="/Users/joshamilton/Documents/repos/claude-v2"
ALLOWLIST_FILE="$REPO_DIR/config/project-allowlist.txt"
LOG_DIR="$REPO_DIR/logs"

RUN_NAS=false
if [ "${1:-}" = "--with-nas" ]; then
    RUN_NAS=true
fi

mkdir -p "$LOG_DIR"

TIMESTAMP="$(date +%Y%m%d-%H%M%S)"
REPORT_FILE="$LOG_DIR/claude-artifact-audit-${TIMESTAMP}.txt"

CLAUDE_DIRS_TMP="$(mktemp)"
MCP_JSON_TMP="$(mktemp)"
CLAUDE_MD_TMP="$(mktemp)"
CODEX_DIRS_TMP="$(mktemp)"
CURSOR_DIRS_TMP="$(mktemp)"
trap 'rm -f "$CLAUDE_DIRS_TMP" "$MCP_JSON_TMP" "$CLAUDE_MD_TMP" "$CODEX_DIRS_TMP" "$CURSOR_DIRS_TMP"' EXIT

# Local leg, group A (.claude, .mcp.json, CLAUDE.md): scan / with /Volumes,
# the allow-listed roots, the global ~/.claude folder, and known noise
# directories pruned.
group_a_prune=(-path /Volumes -o -path /System -o -path /private -o -path /dev -o -path /Library -o -path "$HOME/.claude" -o -name ".git" -o -name "node_modules")

while IFS= read -r pattern; do
    case "$pattern" in
        ""|\#*) continue ;;
    esac
    group_a_prune+=(-o -path "$pattern")
done < "$ALLOWLIST_FILE"

# Local leg, group B (.codex, .cursor): same noise exclusions as group A,
# but no allow-list carve-out, since every copy should be reported
# regardless of location.
group_b_prune=(-path /Volumes -o -path /System -o -path /private -o -path /dev -o -path /Library -o -name ".git" -o -name "node_modules")

echo "Scanning local disk..."
find / "(" "${group_a_prune[@]}" ")" -prune -o -type d -iname ".claude" -print 2>/dev/null | sed 's/^/[local] /' >> "$CLAUDE_DIRS_TMP" || true
find / "(" "${group_a_prune[@]}" ")" -prune -o -type f -iname ".mcp.json" -print 2>/dev/null | sed 's/^/[local] /' >> "$MCP_JSON_TMP" || true
find / "(" "${group_a_prune[@]}" ")" -prune -o -type f -iname "CLAUDE.md" -print 2>/dev/null | sed 's/^/[local] /' >> "$CLAUDE_MD_TMP" || true
find / "(" "${group_b_prune[@]}" ")" -prune -o -type d -iname ".codex" -print 2>/dev/null | sed 's/^/[local] /' >> "$CODEX_DIRS_TMP" || true
find / "(" "${group_b_prune[@]}" ")" -prune -o -type d -iname ".cursor" -print 2>/dev/null | sed 's/^/[local] /' >> "$CURSOR_DIRS_TMP" || true
echo "  done"

if [ "$RUN_NAS" = true ]; then
    # NAS leg: scan /volume1 directly on the Synology over SSH, pruning its
    # own internal @-prefixed system folders, the docker storage folder, and
    # the same noise directories as the local leg. One prune list applies to
    # all five item types here, since the allow list never applies to the
    # NAS's own filesystem. The synology-nas SSH connection execs commands
    # directly with no shell, so this must stay a plain argument list: no
    # quote characters, pipes, or redirection inside the remote command.
    # Redirecting 2>/dev/null applies to ssh's own local stderr. GNU find's
    # -printf tags each hit's category so this can run as one pass instead
    # of five.
    nas_prune=(-name "@*" -o -path "/volume1/docker" -o -name ".git" -o -name "node_modules")

    echo "Scanning NAS via SSH..."
    nas_results="$(ssh synology-nas find /volume1 "(" "${nas_prune[@]}" ")" -prune \
        -o -type d -iname ".claude" -printf "CLAUDE_DIR\t%p\n" \
        -o -type f -iname ".mcp.json" -printf "MCP_JSON\t%p\n" \
        -o -type f -iname "CLAUDE.md" -printf "CLAUDE_MD\t%p\n" \
        -o -type d -iname ".codex" -printf "CODEX_DIR\t%p\n" \
        -o -type d -iname ".cursor" -printf "CURSOR_DIR\t%p\n" \
        2>/dev/null)" || true

    while IFS=$'\t' read -r tag path; do
        [ -z "$tag" ] && continue
        case "$tag" in
            CLAUDE_DIR) echo "[nas] $path" >> "$CLAUDE_DIRS_TMP" ;;
            MCP_JSON) echo "[nas] $path" >> "$MCP_JSON_TMP" ;;
            CLAUDE_MD) echo "[nas] $path" >> "$CLAUDE_MD_TMP" ;;
            CODEX_DIR) echo "[nas] $path" >> "$CODEX_DIRS_TMP" ;;
            CURSOR_DIR) echo "[nas] $path" >> "$CURSOR_DIRS_TMP" ;;
        esac
    done <<< "$nas_results"
    echo "  done"
else
    echo "Skipping NAS leg (pass --with-nas to include it)."
fi

{
    echo "Claude artifact audit - $TIMESTAMP"
    echo
    echo "== .claude directories =="
    if [ -s "$CLAUDE_DIRS_TMP" ]; then cat "$CLAUDE_DIRS_TMP"; else echo "(none found)"; fi
    echo
    echo "== .mcp.json files =="
    if [ -s "$MCP_JSON_TMP" ]; then cat "$MCP_JSON_TMP"; else echo "(none found)"; fi
    echo
    echo "== CLAUDE.md files =="
    if [ -s "$CLAUDE_MD_TMP" ]; then cat "$CLAUDE_MD_TMP"; else echo "(none found)"; fi
    echo
    echo "== .codex directories =="
    if [ -s "$CODEX_DIRS_TMP" ]; then cat "$CODEX_DIRS_TMP"; else echo "(none found)"; fi
    echo
    echo "== .cursor directories =="
    if [ -s "$CURSOR_DIRS_TMP" ]; then cat "$CURSOR_DIRS_TMP"; else echo "(none found)"; fi
} > "$REPORT_FILE"

claude_dirs_count=$(wc -l < "$CLAUDE_DIRS_TMP" | tr -d ' ')
mcp_json_count=$(wc -l < "$MCP_JSON_TMP" | tr -d ' ')
claude_md_count=$(wc -l < "$CLAUDE_MD_TMP" | tr -d ' ')
codex_dirs_count=$(wc -l < "$CODEX_DIRS_TMP" | tr -d ' ')
cursor_dirs_count=$(wc -l < "$CURSOR_DIRS_TMP" | tr -d ' ')

echo
echo "Found $claude_dirs_count .claude folder(s), $mcp_json_count .mcp.json file(s), $claude_md_count CLAUDE.md file(s), $codex_dirs_count .codex folder(s), $cursor_dirs_count .cursor folder(s)."
echo "Full report: $REPORT_FILE"
