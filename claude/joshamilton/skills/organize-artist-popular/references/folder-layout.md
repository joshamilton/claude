# Folder layout and names

Step 3 of `SKILL.md`: where each album goes and what its folder is called.

## 1. Folder layout and names

- Inside the artist folder: `Studio`, `Live`, `Compilation`, `Box Set`. Create only the folders that contain albums. These four are the only allowed names (`groupings` in `config/library-schema.yml` of music-tagger).

- Soundtrack albums are not kept. Move them to the Delete folder and list them under "flagged for manual review" in the plan.

- `Box Set` holds sets sold as boxes. It takes precedence over `Studio`, `Live`, and `Compilation`. There is one exception: a box of complete albums is still split under the rule below. A 2-disc album (a double live album, or an edition with a bonus disc) is not a box set: it goes in `Studio`, `Live`, or `Compilation`.

- An album with editions with different numbers of discs (`references/what-to-keep.md`) gets one folder per edition, named `[YYYY] Album (1-Disc Edition)`, `[YYYY] Album (2-Disc Edition)`, and so on.

- A set that holds separate albums (a box of complete LPs) is split: each album becomes its own `[YYYY] Album` folder in the right subfolder. The empty set folder goes to Delete.

- Archival live concerts go in `Live`, one folder per release.

- Expanded or complete editions of live albums go in `Live` under their own folder year (year of first release), next to the original album they repeat.

- Album folder name: `[YYYY] Album`.

    - YYYY is the year of first release, for every album: studio, live, compilation, and box set.

    - Album is the title of the original release. When sources disagree on the title (Discogs, Wikipedia, etc.), ask the user.

    - Write "&" as "and" in folder names.

    - A `/` or `:` in a title becomes ` - `. Accented letters stay.

- Leave disc subfolders as they are: `structure` renames them to `Disc N` (step 7). Name any disc subfolder you create `Disc 1`, `Disc 2`.

- A 2-on-1 CD (two albums on one disc) that is the only source on disk for at least one of its albums is split into its albums. It then supplies all of them.

    - Any separate rip of the other album goes to Delete.

    - To split it: rename the folder for one album, create a folder for the other, move the other album's tracks into it, and copy the whole-disc log, CUE, and cover into it.

    - The 2-on-1 wins over separate rips even when they are verified copies and the 2-on-1 drops a track.

    - A single-file 2-on-1 (one audio file plus a CUE sheet) is first split into tracks in step 6 (`references/convert-and-structure.md`). Then its tracks are divided among the albums as described here.

    - When every album on the disc is also on disk separately, the 2-on-1 goes to Delete whole, under the repackaged-albums rule in `references/what-to-keep.md`.

