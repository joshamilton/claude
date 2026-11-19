# Bonus discs, staging, and standardize

Steps 9 and 11 of `SKILL.md`. Commands use `<scratch>` and `<tagger>` as in `references/convert-and-cleanup.md`.

## 1. Named bonus discs (step 9)

A bonus disc with its own name becomes its own album. Ask the user first, in the step 8 batch.

1. Create `<grouping folder>/[YYYY] <Title>` in the artist folder. Pick the grouping folder with the rules in `organize-artist-popular` (`Live` for a live session). YYYY is provisional; `standardize` sets it from DATE.

2. Move the disc's audio files, CUE sheet, log, and scans into it. Keep the file names.

3. If one disc folder is left in the old album, move its files up into the album folder and remove the empty `Disc N` folder. `standardize` blocks an album with a lone `Disc` folder.

4. List both albums' files and check that no file was lost: the count before equals the count after.

## 2. Staging layout (step 11)

`standardize` checks the artist and renames album folders only when the artist folder sits at `<root>/<Super-Genre>/<Genre>/<Artist>`. In any other place (for example `<folder>/<Artist>`) it flags every album as "not inside an artist folder" and changes nothing.

1. `<Genre>` is the artist's GENRE. `<Super-Genre>` is the key of the `genres` list in `config/library-schema.yml` that holds it.

2. `<root>` is the folder that holds the artist folder as the user gave it. For `/path/to/artist` it is `/path/to`. No folder above `<root>` may be named like a Super-Genre or Genre folder: `standardize` would take that one as the root. If one is, stop and ask the user for another `<root>`.

3. If the artist folder already sits at `<root>/<Super-Genre>/<Genre>/<Artist>`, do not move it.

4. Otherwise move it to `<root>/<Super-Genre>/<Genre>/<Artist>`. Create the two parent folders if missing. Leave the folder there when done.

## 3. Run standardize (step 11)

```bash
conda run -n music-tagger --no-capture-output python <tagger> standardize --library-type popular --library-format lossless --mode live --dir "<staged artist folder>" --output-dir "<scratch>/standardize"
```

The live pass pads and renumbers TRACKNUMBER, title-cases tags, renames track files, and renames album folders to `[earliest DATE] ALBUM`. Then run `--mode dry-run` into another report folder and confirm it plans nothing more that a live pass can fix; if it does, run `--mode live` again.

## 4. What the user gets

- `standardize.csv`: what is left for review.

- `standardize_genres.csv`, `standardize_artists.csv`, `standardize_albums.csv`, `standardize_titles.csv`: the distinct values of each tag, for bulk fixes.

Give their full paths, and the staged artist folder, in the report.
