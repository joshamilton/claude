################################################################################
### make_public_mirror.py
### Copyright (c) 2026, Joshua J. Hamilton
### Email: <joshamilton@gmail.com>
### URL: <https://www.linkedin.com/in/joshamilton/>
### URL: <https://github.com/joshamilton/claude>
### All rights reserved.
### Build a filtered copy of this repo in ../claude-public, ready to publish.
### 
### How the script works:
### 
### 1. It clones the commit history into ../claude-public.
### 
### 2. It runs git-filter-repo so that only the allowed paths (config/github-allowlist.yml) remain in every commit. Commits keep their message, date and author.
### 
### 3. It scans the commit history of the copy for the names in config/github-blocklist.yml, ignoring case. The blocklist is committed in this repo, but it is not on the allowlist, so it is never part of the copy.
### 
### 4. If a name is found, the copy is deleted and the script stops. The first five matches are shown for review, each with its commit, its file, and the matching line. If a match is an ordinary word (for example, the name "foo" matches the word "foobar"), add that word to "exceptions" in the blocklist.
### 
### 5. It sets the remote "origin" to git@joshamilton-github.com:joshamilton/claude.git, but does not push.
################################################################################

################################################################################
### Import packages
################################################################################

# Standard library imports
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional

# Third-party imports
import yaml

################################################################################
### Constants and configuration
################################################################################

OUT = Path("../claude-public")
ALLOWLIST = Path("config/github-allowlist.yml")
BLOCKLIST = Path("config/github-blocklist.yml")
REMOTE = "git@joshamilton-github.com:joshamilton/claude.git"

################################################################################
### Scan for blocklist names
################################################################################

def find_hits(log_text: str, location: Optional[str], names: list[str], exceptions: list[str]) -> list[tuple[str, str, str]]:
    """Find the lines of a git log output that hold a blocklist name.

    The text comes from git log with the format "commit <short hash>", so each
    commit starts with a line "commit <hash>". With "-p", the file of each patch
    line comes from the line "diff --git a/<file> b/<file>".

    Args:
        log_text: The output of git log
        location: What the lines are (for example "a commit message"), or None for patch output, where the location is the file name
        names: Blocklist names, in lower case
        exceptions: Ordinary words that contain a name, in lower case

    Returns:
        A list of (commit, location, original line), in the order of the log
    """
    hits = []
    commit = "unknown"
    current_file = None
    for line in log_text.splitlines():
        # A line that starts with "commit " marks the next commit. Lines of a patch start with a space, "+", "-", "@" or "diff", so they cannot be mistaken for it.
        if line.startswith("commit "):
            commit = line.split(" ", 1)[1]
            current_file = None
            continue
        if line.startswith("diff --git "):
            current_file = line.rsplit(" b/", 1)[-1]
            continue

        # Lower-case the line, so capitals do not matter. Replace each exception word with a space, so ordinary words that contain a name do not match.
        text = line.lower()
        for word in exceptions:
            text = text.replace(word, " ")
        if any(name in text for name in names):
            hits.append((commit, location or current_file or "a file header", line))
    return hits


################################################################################
### Main function
################################################################################

def main() -> None:
    """Build the filtered copy, scan it, and set the remote."""
    # Read the two lists. Names and exception words are lower-cased, because the text is searched in lower case.
    allowed = yaml.safe_load(ALLOWLIST.read_text())["paths"]
    blocklist = yaml.safe_load(BLOCKLIST.read_text())
    names = [name.lower() for name in blocklist["names"]]
    exceptions = [word.lower() for word in blocklist["exceptions"]]

    # Delete any older copy so each run starts fresh. Then clone only the main branch.
    # "--no-local" makes a real clone with its own history, and "--no-tags" leaves out tags.
    shutil.rmtree(OUT, ignore_errors=True)
    subprocess.run(["git", "clone", "-q", "--no-local", "--no-tags", "--single-branch", "--branch", "main", ".", str(OUT)], check=True)

    # Rewrite the history of the copy so that only the allowed paths remain, in every commit.
    # "cwd=OUT" runs the command inside the copy, so it cannot touch this repo.
    path_args = [item for path in allowed for item in ("--path", path)]
    subprocess.run(["git", "filter-repo", "--quiet", *path_args], cwd=OUT, check=True)

    # Gather the text to search, in three parts. Each commit starts with a line "commit <short hash>", so a match can be traced to its commit.
    file_names = subprocess.run(["git", "log", "--all", "--name-only", "--format=commit %h"], cwd=OUT, check=True, capture_output=True, text=True)
    authors_and_messages = subprocess.run(["git", "log", "--all", "--format=commit %h%n%an %ae %cn %ce%n%B"], cwd=OUT, check=True, capture_output=True, text=True)
    file_contents = subprocess.run(["git", "log", "--all", "-p", "--format=commit %h"], cwd=OUT, check=True, capture_output=True, text=True)

    # Any line that holds a name is a hit. Show up to five (each cut to 120 characters), then delete the copy and stop.
    hits = find_hits(file_names.stdout, "file name", names, exceptions)
    hits += find_hits(authors_and_messages.stdout, "author or commit message", names, exceptions)
    hits += find_hits(file_contents.stdout, None, names, exceptions)
    if hits:
        print("Blocklist word found in the history. The copy was deleted.")
        print("If a match is an ordinary word, add it to 'exceptions' in config/github-blocklist.yml.")
        print(f"{len(hits)} matching lines. The first {min(len(hits), 5)} are shown, as: commit, file, line.")
        for commit, location, line in hits[:5]:
            print(f"{commit}  {location}: {line[:120]}")
        shutil.rmtree(OUT)
        sys.exit(1)

    # The scan is clean. Point the copy at GitHub (the filter removed the old remote). Nothing is pushed.
    subprocess.run(["git", "remote", "add", "origin", REMOTE], cwd=OUT, check=True)

    print(f"Filtered repo created successfully.")
    print("Review, then push:")
    print(f"  cd {OUT}")
    print("  git log")
    print("  git push origin main")


if __name__ == "__main__":
    main()
