---
name: retag-artist-popular
description: Use when the user asks to retag, clean up, or fix the tags of a new artist folder of popular music. Do not use for classical music. Converts high-resolution files, strips disallowed tags, researches and writes ARTIST, ALBUMARTIST, DATE, ALBUM, GENRE, DISCNUMBER, and TITLE to the library standards, and runs the music-tagger `standardize` command.
---

# Retag artist

Set ARTIST, ALBUMARTIST, DATE, ALBUM, GENRE, and DISCNUMBER on every FLAC file, and clean TITLE (see `references/tag-rules.md`). Then run `standardize` to fix TRACKNUMBER, the file names, and the folder names. Then hand its report to the user. The user reviews the result and fixes what is left.

Follow the section "Rules for the task skills" in the skill `music-tagger-setup`: it covers classical music and the artist folder.

The genre tag comes from the user's request, for example `Rock`. If the user did not give one, ask for it before doing anything else.

## Hard limits

- Do not edit any code in the music-tagger repo (`/Users/joshamilton/Documents/repos/music-tagger`). You may edit FLAC tags directly with `metaflac`.

- Write no ARTIST, ALBUMARTIST, DATE, ALBUM, GENRE, DISCNUMBER, or TITLE value until the user has approved the plan (step 8).

- Work through every album in the artist folder. Write the tags, verify them, then hand over a report.

- Never rename, move, or delete an album folder or an audio file yourself, with two exceptions, both in `references/standardize.md`: moving a named bonus disc to its own album after the user agrees, and moving the artist folder to the staging layout. Otherwise only `convert`, `cleanup`, and `standardize` change files.

- Always pass `--output-dir` (an existing folder in your scratchpad) to `convert`, `cleanup`, and `standardize`. Outside the library their reports would otherwise land in the artist folder.

## Steps

1. Check the music-tagger repo and environment with the skill `music-tagger-setup`.

2. Read `references/workflow.md` (environment and required reading) and `references/tag-rules.md`.

3. Convert high-resolution FLAC files to 16-bit 44 kHz with `convert` (`references/convert-and-cleanup.md`, section 1).

4. Inventory the artist folder and dump every current tag, before `cleanup` removes any tag (`references/research.md`). `convert` keeps every tag. `cleanup` removes tags that help the research (catalog numbers, ISRC, etc).

5. Strip disallowed tags and files with `cleanup` (`references/convert-and-cleanup.md`, section 2).

6. Research credits and recording years album by album (`references/research.md`).

7. Build a per-track plan CSV for each album (`references/research.md`).

8. Ask the user about anything uncertain, in one batch per album, and wait for the user to approve the plan (`references/workflow.md`).

9. Move each named bonus disc the user agreed to into its own album (`references/standardize.md`, section 1).

10. Write the tags with `metaflac` and verify them, then make the TITLE fixes and verify those (`references/workflow.md`).

11. Move the artist folder to the staging layout and run `standardize --mode live` (`references/standardize.md`, sections 2 and 3).

12. Hand over the report (`references/workflow.md`).

## Reference files

- `references/tag-rules.md`: read this before deciding any tag value. Covers the album terms, ALBUMARTIST (single-artist or multi-artist album), ARTIST (whose recording it is, and name style), DATE, ALBUM, GENRE, DISCNUMBER, TITLE, and punctuation.

- `references/research.md`: read this when inventorying the rip and looking up credits and recording years. Covers the inventory, rip logs, mislabeled discs, liner-note scans (`Scans.pdf`), the Discogs API and other web sources, and the per-track plan CSV.

- `references/workflow.md`: read this before starting and again before writing. Covers the working environment and required reading, when to ask the user, writing and checking the tags, and the final report.

- `references/convert-and-cleanup.md`: read this before steps 3 and 5. Covers `convert` and `cleanup` and their reports.

- `references/standardize.md`: read this before steps 9 and 11. Covers bonus discs, the staging layout, `standardize`, and the reports handed to the user.

- `assets/title_fixes.py`: read this at step 10. It is the script for the TITLE fixes. `references/workflow.md`, section 3, gives its two commands (`scan` and `write`).

- `assets/title_keywords.yml`: read this when the script misses a title note. It holds the patterns that script uses to tell credits, accessory notes, and part numbers apart. Edit this file, not the script, to change what it proposes.
