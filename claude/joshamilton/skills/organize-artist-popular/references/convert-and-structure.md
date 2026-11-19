# Split single-file rips and run structure

Steps 6 and 7 of `SKILL.md`. Run them after the albums are in their folders (step 5), on the albums that stay. Do not run on the Delete folder. The `music-tagger` environment must pass the checks in the skill `music-tagger-setup`.

## 1. Split single-file rips into tracks

A single-file rip is an album folder (or disc folder) with one audio file (`.flac` or `.ape`) plus one `.cue` sheet, and no per-track audio files. If the CUE sheet has more than one `FILE` line, it is not a single-file rip.

1. If the `FILE` line of the CUE sheet does not name the real audio file next to it, fix that line. The tool finds the audio file through that line.

2. Check that the folder holds no per-track files (`NN - Title.flac`). The tool fails to write, or overwrites, when it does.

3. Split, with an absolute output path (a relative path such as `.` writes nothing):

    ```bash
    conda run -n music-tagger --no-capture-output ffcuesplitter -i "<album>/<name>.cue" -f flac -o "<absolute path of album>" -p standard
    ```

    Do not use `-del`: it also deletes the CUE sheet. Do not use `-ow never`: it writes nothing.

4. Check the result before deleting anything:

    - The number of new `.flac` tracks equals the number of `TRACK` lines in the CUE sheet.

    - The track lengths add up to the length of the single file, within 1 second. The lead-in before track 1 (up to about 0.5 s) is not kept; gaps between tracks (`INDEX 00`) are kept. Read lengths with `conda run -n music-tagger ffprobe -v error -show_entries format=duration -of csv=p=0 <file>`.

5. When the check passes: delete the single audio file and the `<name>.ffcuesplitter.log` file the tool writes. Keep the CUE sheet and the rip log.

6. When the check fails, or the tool fails: keep everything, report the album, and tell the user to split it by hand.

7. A single-file 2-on-1 (two albums on one disc): after the check passes, divide the tracks among the albums as the plan says (`references/folder-layout.md`). Every album folder gets a copy of the original CUE sheet and rip log, unchanged.

8. Renumber every album of any split 2-on-1 (single-file, or ripped track by track) that does not start at track 1. For each track of such an album, number the tracks `1..N` in their order, then set the tag and rename the file to match:

    ```bash
    metaflac --remove-tag=TRACKNUMBER --set-tag=TRACKNUMBER=<k> "<album>/<NN> - <Title>.flac"
    mv "<album>/<NN> - <Title>.flac" "<album>/<kk> - <Title>.flac"
    ```

    `<kk>` is `k` zero-padded to the width of the album's highest track number. Then list `TRACKNUMBER` and the file name of every track of the album, and check that they run `1..N` and agree.

## 2. Run `structure --mode all`

`--dir` is a grouping folder (`Studio`, `Live`, `Compilation`, or `Box Set`). The command treats every subfolder of `--dir` as an album folder, and works inside each album folder, including its disc subfolders. Do not run it on the artist folder: it would treat `Studio` and the other grouping folders as albums. Run it once for each grouping folder that exists:

```bash
conda run -n music-tagger --no-capture-output python <tagger> structure --library-type popular --dir "<grouping folder>" --mode all --output-csv "/tmp/structure-<grouping folder name>.csv"
```

`<tagger>` is defined in the skill `music-tagger-setup`.
