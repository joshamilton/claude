---
name: music-tagger-setup
description: Use when a task needs the music-tagger command-line tool, its repo, or its `music-tagger` conda environment. Checks that the repo and the environment exist, clones the repo and creates the environment when missing, gives the command that runs Python in the environment, and holds the rules shared by the music task skills.
---

# music-tagger setup

This skill is personal work only. It checks the `music-tagger` repo and its conda environment. The task skills `organize-artist-popular` and `retag-artist-popular` require this skill to be run first.

## Hard limits

- Never edit, pull, reset, or commit in an existing music-tagger repo. Only clone it when it is missing.

- Never remove or rebuild an existing `music-tagger` environment. Add to it with `mamba env update`.

## Facts

1. Local repo: `/Users/joshamilton/Documents/repos/music-tagger`. Always use this absolute path.

2. Remote repo: `git@joshamilton-github.com:joshamilton/music-tagger.git`.

3. Environment name: `music-tagger`. Its definition is `config/music-tagger.yml` in the repo.

4. Run Python in the environment with `conda run -n music-tagger python <script>`. Add `--no-capture-output` to `conda run` when a command prints progress or prompts.

5. The tool itself runs as `conda run -n music-tagger python <tagger> <command> ...`. In the task skills, `<tagger>` is `/Users/joshamilton/Documents/repos/music-tagger/src/tagger.py`.

6. The environment's `bin` folder is `/Users/joshamilton/miniforge3/envs/music-tagger/bin`. It holds the command-line tools `metaflac`, `flac`, `sox`, `ffprobe`, `pdftoppm`, `pdfinfo`, `magick`, `montage`, and `sqlite3`.

7. A `tagger.py` command with `--output-dir` stops with "Invalid --output-dir: not an existing folder" unless the folder exists. Create it with `mkdir -p` first.

## Rules for the task skills

These rules hold for `organize-artist-popular` and `retag-artist-popular`. Each task skill supplements the music-tagger tool, and this skill holds the repo, the environment, and the command that runs it.

1. Classical music follows a different set of rules entirely. The task skills do not apply to it. If the artist folder is classical, stop and tell the user.

2. The artist folder comes from the user's request, for example `/path/to/artist/`. If the user did not give one, ask for it before doing anything else.

## Steps

1. Check the repo:

    ```bash
    test -d /Users/joshamilton/Documents/repos/music-tagger/.git && echo present || echo missing
    ```

    If it is missing, clone it:

    ```bash
    git clone git@joshamilton-github.com:joshamilton/music-tagger.git /Users/joshamilton/Documents/repos/music-tagger
    ```

2. Check the environment:

    ```bash
    conda env list | grep -w music-tagger
    ```

    If it is missing, create it from the repo:

    ```bash
    mamba env create -f /Users/joshamilton/Documents/repos/music-tagger/config/music-tagger.yml
    ```

3. Check the tools in fact 6:

    ```bash
    for t in metaflac flac sox ffprobe pdftoppm pdfinfo magick montage sqlite3; do test -x /Users/joshamilton/miniforge3/envs/music-tagger/bin/$t || echo "missing $t"; done
    ```

    If any is missing, add it to the existing environment (do not rebuild it):

    ```bash
    mamba env update -n music-tagger -f /Users/joshamilton/Documents/repos/music-tagger/config/music-tagger.yml
    ```

4. Tell the user only what you had to fix (cloned, created, or updated). If everything was present, say nothing about setup and go on with the task.
