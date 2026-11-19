# Convert and clean up

Steps 3 and 5 of `SKILL.md`, on the whole artist folder.

- `convert` (step 3) runs before the tag dump (step 4) and keeps every tag.

- `cleanup` (step 5) runs after the dump, because it removes tags.

In the commands:

- `<scratch>` is a folder in your scratchpad.

- `<tagger>` is defined in the skill `music-tagger-setup`.

Run `tagger.py` with `conda run -n music-tagger --no-capture-output python <tagger> ...`. Create each report folder (`mkdir -p`) before the first run.

## 1. Convert high-resolution files

1. Convert in place. The tool skips files that are already 16-bit 44 kHz:

    ```bash
    conda run -n music-tagger --no-capture-output python <tagger> convert --library-type popular --dir "<artist folder>" --output-dir "<scratch>/convert" --overwrite
    ```

2. Read the reports in `<scratch>/convert`. If `convert_failures.csv` (unreadable files) or `convert_errors.csv` (failed conversions) has rows, stop and report the files. List the files in `convert_warnings.csv` (sox reports clipped samples there) in the final report.

## 2. Strip disallowed tags and files

1. Run it:

    ```bash
    conda run -n music-tagger --no-capture-output python <tagger> cleanup --library-type popular --library-format lossless --dir "<artist folder>" --output-dir "<scratch>/cleanup"
    ```

2. Read the reports in `<scratch>/cleanup`. If `cleanup_busy.txt` lists files, stop and report them. In the final report, list the files in `cleanup_delete.txt` that are not `.DS_Store` or similar system files. `cleanup` removes embedded artwork and lists it in `cleanup_tags.csv` with `tag_type` `Picture`.

3. Check that no FLAC still holds embedded artwork (a `PICTURE` block). The count must be 0:

    ```bash
    find "<artist folder>" -name '*.flac' -exec /Users/joshamilton/miniforge3/envs/music-tagger/bin/metaflac --list --block-type=PICTURE {} + | grep -c 'type: 6'
    ```

    If it is not 0, list the files that hold a picture and remove it from each with `metaflac --preserve-modtime --remove --block-type=PICTURE "<file>"`. Then run the check again.
