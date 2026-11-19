#!/usr/bin/env python
################################################################################
### title_fixes.py
### Copyright (c) 2026, Joshua J. Hamilton
### Email: <joshamilton@gmail.com>
### URL: <https://www.linkedin.com/in/joshamilton/>
### URL: <https://github.com/joshamilton/claude>
### All rights reserved.
###
### Two steps for cleaning the TITLE tag of the FLAC files in one artist folder:
###   scan:  find the parenthetical text in every title, propose the clear fixes,
###          and mark the rest for review, in a CSV.
###   write: write the new titles of a reviewed CSV with metaflac, and check them.
### Run it with the Python of the music-tagger environment. The patterns it uses
### are in title_keywords.yml, next to this script.
################################################################################

################################################################################
### Import packages
################################################################################

# Standard library imports (alphabetical order within group)
import argparse
import csv
import logging
import re
import subprocess
import sys
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Optional

# Third-party imports (alphabetical order within group)
import yaml
from mutagen.flac import FLAC
from rapidfuzz.distance import Levenshtein
from tqdm import tqdm

################################################################################
### Constants
################################################################################

LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

CSV_COLUMNS = ["path", "old_title", "new_title", "change_kind", "parenthetical_text"]

OPENERS = {"(": ")", "[": "]"}
CLOSERS = {")", "]"}

logger = logging.getLogger(__name__)

################################################################################
### Command-line arguments
################################################################################

def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments.

    argparse exits with status 2 when the arguments are invalid.

    Returns:
        Parsed arguments namespace.
    """
    parser = argparse.ArgumentParser(
        description=(
            "Clean the TITLE tag of FLAC files. 'scan' writes a CSV of proposed new titles. "
            "'write' writes the titles of a reviewed CSV to the files."
        ),
        epilog=(
            "Change kinds in the CSV: credit, accessory, part (proposed, new_title is filled); "
            "review, separator, accent, spelling, unbalanced, missing, multiple (flagged, "
            "new_title is unchanged until you edit it)."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--log-level",
        type=str,
        choices=LOG_LEVELS,
        default="INFO",
        metavar="LEVEL",
        help="Logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL (default: INFO)"
    )
    parser.add_argument(
        "--log-file",
        type=Path,
        default=Path("logs") / f"{Path(__file__).stem}.log",
        metavar="FILE",
        help="Path to log file (default: logs/title_fixes.log)"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    scan = subparsers.add_parser("scan", help="Write a CSV of proposed title changes")
    scan.add_argument(
        "--dir",
        type=Path,
        required=True,
        metavar="DIR",
        help="Artist folder; every FLAC file below it is read"
    )
    scan.add_argument(
        "--output",
        type=Path,
        required=True,
        metavar="FILE",
        help="CSV file to write"
    )
    scan.add_argument(
        "--keywords",
        type=Path,
        default=Path(__file__).with_name("title_keywords.yml"),
        metavar="FILE",
        help="Pattern file (default: title_keywords.yml next to this script)"
    )

    write = subparsers.add_parser("write", help="Write the titles of a reviewed CSV to the files")
    write.add_argument(
        "--file-list",
        type=Path,
        required=True,
        metavar="FILE",
        help="Reviewed CSV from 'scan'; rows whose new_title differs from old_title are written"
    )
    write.add_argument(
        "--dry-run",
        action="store_true",
        help="Check every row and list the changes, but write nothing"
    )
    return parser.parse_args()

################################################################################
### Logging configuration
################################################################################

def setup_logging(log_level: str = "INFO", log_file: Optional[Path] = None) -> None:
    """Configure logging for the script.

    Each run starts a new log file, so the log holds only the latest run.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to the log file, or None for logging to stderr only
    """
    handlers: list[logging.Handler] = []
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        handlers.append(logging.FileHandler(log_file, mode="w"))
    handlers.append(logging.StreamHandler(sys.stderr))

    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=handlers
    )

################################################################################
### Title functions
################################################################################

def find_parenthetical_text(title: str) -> Optional[list[tuple[int, int]]]:
    """Find the parenthetical text of a title.

    Parenthetical text is text inside a pair of parentheses ( ) or square brackets [ ],
    with the marks themselves. Counts ( and [ as openers and ) and ] as closers, so
    parenthetical text that holds more of it, such as "[with <name> (<band>)]",
    is one piece: only the outermost pieces are found.

    Args:
        title: The title text.

    Returns:
        A list of (start, end) positions, where title[start:end] is one piece of
        parenthetical text with its marks, or None when the marks do not pair up.
    """
    spans: list[tuple[int, int]] = []
    stack: list[str] = []
    start = 0
    for position, character in enumerate(title):
        if character in OPENERS:
            if not stack:
                start = position
            stack.append(OPENERS[character])
        elif character in CLOSERS:
            # A closer must match the most recent opener.
            if not stack or stack.pop() != character:
                return None
            if not stack:
                spans.append((start, position + 1))
    if stack:
        return None
    return spans


def classify_parenthetical_text(inner: str, patterns: dict) -> tuple[str, Optional[str]]:
    """Decide what to do with the text inside one piece of parenthetical text.

    Args:
        inner: The text inside the parentheses or brackets, without them.
        patterns: The compiled patterns from load_patterns().

    Returns:
        (kind, replacement). kind is 'credit', 'accessory', 'part', or 'review'.
        replacement is the text that replaces the whole piece, marks included: '' to
        remove it, ', Part N' for a part, or None to keep it.
    """
    text = inner.strip()
    if any(pattern.search(text) for pattern in patterns["credit"]):
        return "credit", ""
    if any(pattern.search(text) for pattern in patterns["accessory"]):
        return "accessory", ""
    part = patterns["part"].search(text)
    if part:
        return "part", f", Part {part.group(1)}"
    return "review", None


def propose_title(title: str, patterns: dict) -> tuple[str, set[str], list[str]]:
    """Propose a new title for one old title.

    Args:
        title: The old title.
        patterns: The compiled patterns from load_patterns().

    Returns:
        (new_title, kinds, parenthetical). kinds is the set of change kinds found.
        parenthetical is the list of pieces of parenthetical text, as written.
    """
    spans = find_parenthetical_text(title)
    if spans is None:
        return title, {"unbalanced"}, []

    kinds: set[str] = set()
    pieces: list[str] = []
    cursor = 0
    outside = ""  # the text outside all parentheses and brackets, used to look for a separator
    for start, end in spans:
        before = title[cursor:start]
        pieces.append(before)
        outside += before
        kind, replacement = classify_parenthetical_text(title[start + 1:end - 1], patterns)
        kinds.add(kind)
        if replacement is None:
            pieces.append(title[start:end])
        elif replacement:
            # ", Part 1" attaches to the word before it, with no space.
            pieces[-1] = pieces[-1].rstrip()
            pieces.append(replacement)
        cursor = end
    tail = title[cursor:]
    pieces.append(tail)
    outside += tail

    if " - " in outside or " / " in outside:
        kinds.add("separator")
    new_title = re.sub(r"\s+", " ", "".join(pieces)).strip()
    return new_title, kinds, [title[start:end] for start, end in spans]


def spelling_key(title: str) -> str:
    """Reduce a title to letters and digits, without case or accents.

    Args:
        title: The title text.

    Returns:
        The reduced text.
    """
    decomposed = unicodedata.normalize("NFKD", title)
    letters = "".join(c for c in decomposed if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]", "", letters.casefold())


def find_spelling_variants(titles: list[str], max_distance: int, min_length: int) -> list[set[str]]:
    """Find titles that are probably the same song written two ways.

    A difference in capital letters alone does not count: `standardize` fixes it.
    Accents, punctuation, and up to max_distance different letters do count.

    Args:
        titles: The new titles of every file in the folder.
        max_distance: The largest number of different letters that still counts.
        min_length: Reduced titles shorter than this must match exactly.

    Returns:
        A list of clusters. Each cluster is the set of spellings of one song.
    """
    by_key: dict[str, set[str]] = {}
    for title in titles:
        by_key.setdefault(spelling_key(title), set()).add(title)

    # Join the keys that are close to each other, so a cluster can hold more than two.
    parent = {key: key for key in by_key}

    def find_root(key: str) -> str:
        while parent[key] != key:
            parent[key] = parent[parent[key]]
            key = parent[key]
        return key

    keys = sorted(key for key in by_key if len(key) >= min_length)
    for index, key in enumerate(keys):
        for other in keys[index + 1:]:
            if abs(len(key) - len(other)) > max_distance:
                continue
            if Levenshtein.distance(key, other) <= max_distance:
                parent[find_root(other)] = find_root(key)

    members: dict[str, set[str]] = {}
    for key in by_key:
        members.setdefault(find_root(key), set()).update(by_key[key])
    # A cluster of one key is a variant only when its spellings differ by more than case.
    return [spellings for spellings in members.values()
            if len({spelling.casefold() for spelling in spellings}) > 1]


def load_patterns(keywords_file: Path) -> dict:
    """Read the pattern file and compile its patterns.

    Args:
        keywords_file: Path to title_keywords.yml.

    Returns:
        A dict with the compiled 'credit', 'accessory', and 'part' patterns, the
        'accent_words', and the two spelling settings.

    Raises:
        FileNotFoundError: If the pattern file does not exist.
        ValueError: If the file lacks a setting or holds an invalid pattern.
    """
    with open(keywords_file, encoding="utf-8") as handle:
        settings = yaml.safe_load(handle) or {}
    required = ["credit_patterns", "accessory_patterns", "part_pattern", "accent_words",
                "spelling_max_distance", "spelling_min_length"]
    missing = [name for name in required if name not in settings]
    if missing:
        raise ValueError(f"{keywords_file} has no setting for: {', '.join(missing)}")
    try:
        return {
            "credit": [re.compile(p, re.IGNORECASE) for p in settings["credit_patterns"]],
            "accessory": [re.compile(p, re.IGNORECASE) for p in settings["accessory_patterns"]],
            "part": re.compile(settings["part_pattern"], re.IGNORECASE),
            "accent_words": {word.casefold() for word in settings["accent_words"]},
            "spelling_max_distance": int(settings["spelling_max_distance"]),
            "spelling_min_length": int(settings["spelling_min_length"]),
        }
    except re.error as error:
        raise ValueError(f"Invalid pattern in {keywords_file}: {error}") from error

################################################################################
### Scan
################################################################################

def read_titles(path: Path) -> list[str]:
    """Read the TITLE values of one FLAC file, whatever the case of the field name.

    Args:
        path: The FLAC file.

    Returns:
        The list of TITLE values (empty when the file has none).
    """
    tags = FLAC(path).tags
    return list(tags.get("title", [])) if tags else []


def run_scan(args: argparse.Namespace) -> int:
    """Write the CSV of proposed title changes.

    Args:
        args: Parsed arguments (dir, output, keywords).

    Returns:
        The number of files read.

    Raises:
        FileNotFoundError: If the folder or the pattern file does not exist.
    """
    if not args.dir.is_dir():
        raise FileNotFoundError(f"Not a folder: {args.dir}")
    patterns = load_patterns(args.keywords)
    paths = sorted(p for p in args.dir.rglob("*") if p.suffix.lower() == ".flac")
    logger.info(f"Reading {len(paths)} FLAC files below {args.dir}")

    rows: list[dict[str, str]] = []
    kinds_by_row: list[set[str]] = []
    for path in tqdm(paths, desc="Reading titles"):
        titles = read_titles(path)
        if len(titles) != 1:
            kind = "missing" if not titles else "multiple"
            old_title = titles[0] if titles else ""
            rows.append({"path": str(path), "old_title": old_title, "new_title": old_title,
                         "change_kind": kind, "parenthetical_text": ""})
            kinds_by_row.append({kind})
            continue
        new_title, kinds, parenthetical = propose_title(titles[0], patterns)
        rows.append({"path": str(path), "old_title": titles[0], "new_title": new_title,
                     "change_kind": "", "parenthetical_text": " | ".join(parenthetical)})
        kinds_by_row.append(kinds)

    # Checks that need the whole folder or the new title.
    new_titles = [row["new_title"] for row in rows if row["new_title"]]
    clusters = find_spelling_variants(
        new_titles, patterns["spelling_max_distance"], patterns["spelling_min_length"]
    )
    counts = Counter(new_titles)
    for cluster in sorted(clusters, key=lambda spellings: sorted(spellings)[0]):
        listing = "; ".join(f"{title!r} x{counts[title]}" for title in sorted(cluster))
        logger.info(f"Spelling variants: {listing}")
    variants = {title for cluster in clusters for title in cluster}
    for row, kinds in zip(rows, kinds_by_row):
        if row["new_title"] in variants:
            kinds.add("spelling")
        if set(re.findall(r"[a-z]+", row["new_title"].casefold())) & patterns["accent_words"]:
            kinds.add("accent")
        if not row["change_kind"]:
            row["change_kind"] = "; ".join(sorted(kinds))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)

    changed = sum(1 for row in rows if row["new_title"] != row["old_title"])
    flagged = sum(1 for row in rows if row["change_kind"] and
                  set(row["change_kind"].split("; ")) - {"credit", "accessory", "part"})
    logger.info(f"Wrote {args.output}: {changed} proposed change(s), {flagged} row(s) to review")
    return len(paths)

################################################################################
### Write
################################################################################

def run_command(command: list[str]) -> subprocess.CompletedProcess:
    """Run one command and capture its output.

    Args:
        command: The command and its arguments.

    Returns:
        The finished process.
    """
    return subprocess.run(command, capture_output=True, text=True)


def run_write(args: argparse.Namespace) -> int:
    """Write the new titles of a reviewed CSV, and check each file.

    All rows are checked before any file is written: if one file no longer holds the
    old title, nothing is written.

    Args:
        args: Parsed arguments (file_list, dry_run).

    Returns:
        The number of files changed (or that would change, with --dry-run).

    Raises:
        FileNotFoundError: If the CSV or a listed file does not exist.
        ValueError: If a row is invalid, or a file no longer holds the old title.
    """
    with open(args.file_list, newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    missing_columns = [c for c in CSV_COLUMNS[:3] if not rows or c not in rows[0]]
    if missing_columns:
        raise ValueError(f"{args.file_list} has no column: {', '.join(missing_columns)}")
    changes = [row for row in rows if row["new_title"] != row["old_title"]]
    logger.info(f"{len(changes)} of {len(rows)} row(s) change a title")

    # Check every row first.
    problems: list[str] = []
    for row in changes:
        path = Path(row["path"])
        if not path.is_file():
            raise FileNotFoundError(f"File not found: {path}")
        if not row["new_title"].strip():
            problems.append(f"{path}: new_title is empty")
        current = read_titles(path)
        if current != [row["old_title"]]:
            problems.append(f"{path}: TITLE is {current!r}, expected {row['old_title']!r}")
    if problems:
        for problem in problems:
            logger.error(problem)
        raise ValueError(f"{len(problems)} row(s) do not match the files; nothing was written")

    if args.dry_run:
        for row in changes:
            logger.info(f"Would change: {row['old_title']!r} -> {row['new_title']!r}")
        return len(changes)

    failures: list[str] = []
    for row in tqdm(changes, desc="Writing titles"):
        path = Path(row["path"])
        result = run_command(["metaflac", "--preserve-modtime", "--remove-tag=TITLE",
                              f"--set-tag=TITLE={row['new_title']}", str(path)])
        if result.returncode != 0:
            failures.append(f"{path}: metaflac failed: {result.stderr.strip()}")
            continue
        if read_titles(path) != [row["new_title"]]:
            failures.append(f"{path}: TITLE is not exactly the new title after writing")
            continue
        result = run_command(["flac", "-t", "-s", str(path)])
        if result.returncode != 0:
            failures.append(f"{path}: flac -t failed: {result.stderr.strip()}")
    for failure in failures:
        logger.error(failure)
    if failures:
        raise ValueError(f"{len(failures)} file(s) failed the write or the check")
    logger.info(f"Wrote and checked {len(changes)} title(s)")
    return len(changes)

################################################################################
### Main function
################################################################################

def main() -> None:
    """Run the script: parse arguments, set up logging, and run the chosen command."""
    args = parse_arguments()
    setup_logging(args.log_level, args.log_file)

    try:
        logger.info(f"Command {args.command} started")
        if args.command == "scan":
            run_scan(args)
        else:
            run_write(args)
        logger.info("Completed successfully")
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        sys.exit(3)
    except PermissionError as e:
        logger.error(f"Permission denied: {e}")
        sys.exit(3)
    except (ValueError, TypeError) as e:
        logger.error(f"Invalid data: {e}")
        sys.exit(4)
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
