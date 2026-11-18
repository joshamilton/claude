---
name: organize-artist-popular
description: Use when the user asks to organize, sort, or clean up a new artist folder of popular music in the library. Do not use for classical music. Sorts albums into a defined structure, keeps one copy per album, splits single-file rips into tracks, and cleans album folders with the music-tagger `structure` command.
---

# Organize artist

Sort one artist folder into a clean layout: one copy of each album the artist, in `Studio`, `Live`, `Compilation`, and `Box Set` subfolders, with every rejected folder moved to a Delete folder for the user to review. Nothing moves until the user approves a written plan.

Classical music follows a different set of rules entirely. This skill does not apply to it. If the artist folder is classical, stop and tell the user.

The artist folder comes from the user's request, for example `/path/to/artist/`. If the user did not give one, ask for it before doing anything else.

This skill supplements the music-tagger tool. The skill `music-tagger-setup` holds the repo, the environment, and the command that runs it.

## Hard limits

- Never delete album folders. Rejected albums, and parent folders left empty after a move, go into the Delete folder. The user deletes them.

- Move nothing until the user has approved the plan.

- Never rename, move between albums, edit, or re-encode an audio file. The only audio files you may split are single-file rips and 2-on-1 CDs, in step 6. The only audio files you may move between albums or rename are the tracks of a split 2-on-1, which are renumbered in step 6 (see `references/convert-and-structure.md` and `references/folder-layout.md`).

- Never delete a single audio file before its split has passed the checks in `references/convert-and-structure.md`. Never delete a CUE sheet or a rip log.

- Never edit a CUE sheet. One exception: the `FILE` line of a CUE sheet that does not name the real audio file next to it may be fixed, before the split (see `references/convert-and-structure.md`).

- Never create an empty subfolder. A Live folder exists only if at least one live album goes into it.

- Never write or change tags yourself. The only tags written are the ones the splitter writes from the CUE sheet, and the `TRACKNUMBER` of the albums of a split 2-on-1 (see `references/convert-and-structure.md`). Retagging is a separate task (`retag-artist-popular`).

## Steps

1. Check the music-tagger repo and environment with the skill `music-tagger-setup`.

2. Inventory the artist folder and compare it with a discography. Read `references/inventory.md`.

3. Decide each folder's fate with the rules in `references/folder-layout.md` (where it goes and what it is called), and `references/what-to-keep.md` (which copy stays, and what goes to Delete). Allowed fates are:

    - keep (with its new name and subfolder)

    - split

    - move to Delete

4. Write the plan with your questions at the end, and stop. Read `references/plan.md`. Wait for the user's answers and approval.

5. When the user approves, make the moves exactly as approved, then list the final tree so the user can check it. Wait for the user's approval.

6. When the user approves, split every single-file rip (one APE or FLAC file plus a CUE sheet) into FLAC tracks. Fix a wrong `FILE` line in the CUE sheet first. Check the result, then delete the single audio file and keep the CUE sheet and the rip log. If the split or the checks fail, leave the album as it is and report it. For a single-file 2-on-1, divide the tracks among its albums and renumber them. Read `references/convert-and-structure.md`, section 1.

7. Organize and clean up each album folder with `structure --mode all`. Read `references/convert-and-structure.md`, section 2.

8. Tell the user you are done with the folder.

## Reference files

- `references/inventory.md`: the inventory and the discography check.

- `references/folder-layout.md`: the folders, the album folder names, volumes, 2-on-1 discs, and box sets.

- `references/what-to-keep.md`: one copy per album, what is kept, and the Delete folder.

- `references/plan.md`: what the plan holds.

- `references/convert-and-structure.md`: splitting single-file rips and running `structure`.
