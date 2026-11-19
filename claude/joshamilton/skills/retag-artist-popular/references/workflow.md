# Workflow

Environment, required reading, when to ask the user, writing and checking the tags, and the report. Steps 1, 2, 8, 10, and 12 of `SKILL.md`.

## 1. Working environment and background

The skill `music-tagger-setup` gives the repo path, the command that runs Python in the `music-tagger` environment, and the command-line tools the environment holds. Refer to the repo's files by their absolute paths.

Read these before starting:

- `/Users/joshamilton/Documents/repos/music-tagger/README.md`, sections "Tag Fields > Popular", "Multi-Valued tags", and "Standardize > Popular". These define the rules in `references/tag-rules.md`. Also read "Convert", "Cleanup", and "Standardize > Reviewing reports".

- `/Users/joshamilton/Documents/repos/music-tagger/config/library-schema.yml`, the `titlecase_exceptions` list. Names on that list are kept exactly as written. Also the `genres` list, for GENRE and the staging layout.

- The Lossless library catalog at `/Volumes/TheLibrary/Audio/Lossless/catalog-popular.db` (SQLite, table `tracks`, columns `artist`, `album_artist`, `album`, `date`, `path`). It lives on a slow NAS, so copy it to your scratchpad and query the copy. Use it to see how existing artists are spelled, and to reuse an existing spelling a tag is already in the library.

## 2. When to ask

Ask before writing, in one batch per album where you can, with your recommended answer first. Show the plan CSV paths, and wait for the user to approve the plan. Ask about:

- A year that is a range, a guess, or disputed between sources.

- Whether an album is contemporaneous or posthumous, when it is not obvious.

- A named bonus disc: move it to its own album (`references/standardize.md`, section 1).

- A credit you cannot settle from the rules in `references/tag-rules.md`.

- Anything where different reasonable readings would give different tags.

Do not ask about things the rules already decide.

## 3. Writing and checking

- Write with `metaflac --preserve-modtime`. Remove the old values first (`--remove-tag=ARTIST --remove-tag=ALBUMARTIST --remove-tag=DATE --remove-tag=ALBUM --remove-tag=GENRE --remove-tag=DISCNUMBER`), then set the new ones. On a single-artist album, remove ALBUMARTIST and do not set it. On a single-disc album, do not set DISCNUMBER. `cleanup` has already removed `ALBUM ARTIST` and `YEAR`.

- After writing, re-read every file and check:

    - Each tag matches the plan, and each appears exactly once.

    - DATE is four digits.

    - ALBUM and GENRE are the same on every track of an album.

    - DISCNUMBER is on every track of a multi-disc album, and on no track of a single-disc album.

    - The single-artist or multi-artist rule holds for the whole album.

    - No file holds a `PICTURE` block (embedded artwork).

- Print the pooled list of distinct ARTIST and ALBUMARTIST values across the whole artist folder with counts, so near-duplicate spellings stand out. Do the same for TITLE.

- TITLE fixes (`references/tag-rules.md`, section 9) come after the other tags are written, so you can confirm ARTIST holds every guest before the credit leaves the title.

    Use the script `assets/title_fixes.py` in the skill folder. `<skill>` stands for `/Users/joshamilton/Documents/repos/claude/claude/joshamilton/skills/retag-artist-popular`. It finds the parenthetical text in each title that may be removed. Its patterns are in `assets/title_keywords.yml`.

    1. Scan the folder. The CSV has one row per file, with `old_title`, `new_title`, `change_kind`, and the parenthetical text found:

        ```bash
        conda run -n music-tagger --no-capture-output python <skill>/assets/title_fixes.py --log-file "<scratch>/title_fixes.log" scan --dir "<artist folder>" --output "<scratch>/titles.csv"
        ```

    2. Read the CSV and the log. Rows of kind `credit`, `accessory`, and `part` already hold the proposed `new_title`. Every other kind is left unchanged, for you to decide with `references/tag-rules.md`, section 9:

        - `review`: parenthetical text the patterns do not know. Keep it if it is part of the song's name.

        - `separator`: a ` - ` or ` / ` outside any parentheses or brackets. It may be a medley or a credit.

        - `accent`: a word that usually has an accent or umlaut.

        - `spelling`: the log lists each set of spellings of one song, with counts.

        - `unbalanced`, `missing`, and `multiple`: a title whose parentheses or brackets do not pair up, a file with no TITLE, and a file with more than one TITLE.

        Edit `new_title` in the CSV. Show the changed rows in the plan you give the user in step 8.

    3. After the user approves, write. The script first checks that every file still holds its `old_title` and writes nothing if one does not. Then it writes with `metaflac --preserve-modtime`, re-reads each file (exactly one TITLE, equal to `new_title`), and runs `flac -t -s`. Use `--dry-run` first:

        ```bash
        conda run -n music-tagger --no-capture-output python <skill>/assets/title_fixes.py --log-file "<scratch>/title_fixes.log" write --file-list "<scratch>/titles.csv" --dry-run
        ```

    4. Scan again into a new CSV. It must propose no change, and every remaining `review`, `separator`, `accent`, or `spelling` row must be one you decided to keep.

    The script exits with 3 for a missing file, 4 for a CSV that does not match the files, and 1 for any other error. Read the log for the reason.

## 4. Report

End with a report the user can review, in plain language:

- Per album: number of tracks tagged, the main sources, the year range, whether it is single-artist or multi-artist, the ALBUM value, and any bonus disc moved to its own album.

- The pooled list of ARTIST values.

- Every judgment call: years that fell back to release year, credits taken from one source over another, answers the user gave you.

- Every problem you found but did not fix, with the evidence (track numbers, durations, checksums).

- The full paths of the plan CSVs, of the `convert`, `cleanup`, and `standardize` reports, and of the staged artist folder, and the files listed in `convert_warnings.csv`.

Then wait for the user's review. Do not call the task finished until the user confirms the tags and the `standardize` report look right.
