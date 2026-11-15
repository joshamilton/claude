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
### 4. If a name is found, the copy is deleted and the script stops. The matching lines are shown for review. If a match is an ordinary word (for example, the name "foo" matches the word "foobar"), add that word to "exceptions" in the blocklist.
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

    # Gather the text to search: file names, author names and emails, commit messages, and every line of every file in all commits.
    names_and_messages = subprocess.run(["git", "log", "--all", "--name-only", "--format=%an %ae %cn %ce%n%B"], cwd=OUT, check=True, capture_output=True, text=True)
    file_contents = subprocess.run(["git", "log", "--all", "-p", "--format="], cwd=OUT, check=True, capture_output=True, text=True)

    # Lower-case it all, so capitals do not matter. Then replace each exception word with a space, so ordinary words that contain a name do not match.
    text = (names_and_messages.stdout + file_contents.stdout).lower()
    for word in exceptions:
        text = text.replace(word, " ")

    # Any line that holds a name is a hit. Show up to five (each cut to 120 characters), then delete the copy and stop.
    hits = [line for line in text.splitlines() if any(name in line for name in names)]
    if hits:
        print("Blocklist word found in the history. The copy was deleted.")
        print("If a match is an ordinary word, add it to 'exceptions' in config/github-blocklist.yml.")
        for line in hits[:5]:
            print(line[:120])
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
