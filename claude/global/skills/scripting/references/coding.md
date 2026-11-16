# Script coding rules

These rules hold for every script that is run from the command line, in any language. The language skill gives the language-specific code for the scripts. See `references/setup.md` in this skill for the project layout and the order of the sections in a script.

## Command-line flags

- Name flags in long form with hyphens (`--input-file`). Use short options sparingly, and only for common flags (such as `-h`).
- Give every flag help text, and give every optional flag a default. State the default in the help text.
- Name the type and a short placeholder for each value (for example `FILE` or `DIR`) in the help output.
- Use a plain on/off flag for a switch that takes no value.
- `--help` prints the help text and exits with status 0.
- Every script has `--log-level` (DEBUG, INFO, WARNING, ERROR, CRITICAL; default INFO) and `--log-file` (default `logs/<script>.log`: the script name with a `.log` suffix, under `logs/`).

## Logging

- Use the log for errors, warnings, and important status messages. Do not print messages the user needs.
- Create the log folder if it does not exist.
- Each log line has the date and time (`YYYY-MM-DD HH:MM:SS`), the logger name, the level, and the message, separated by ` - `. For example: `2026-11-16 11:12:05 - __main__ - INFO - Processing started`.
- Each run starts its log file fresh. Open the log file for writing, which empties it, never for appending. This holds for the default path and for a path given with `--log-file`.
- If the logs of earlier runs must be kept, give each run its own file name (for example a timestamp in the name). Do not append to one shared file.

## Exit codes

Every script exits with one of these codes:

- 0: success
- 1: unexpected error
- 2: invalid command-line arguments
- 3: file not found, or a file read or write error
- 4: invalid input data

Check the inputs early, give a clear error message in the log, and then exit with the matching code. Catch specific errors, and exit with a code that matches the error.

## Results, progress, and output

- Write results to files (CSV, not the terminal). Use the terminal for important progress updates, and use the log for messages.
- Show progress when looping over records, files, or other collections. Draw the progress bar on the standard error, so that it never mixes with results written to the standard output.
- Report counts and warnings with the log, not with the progress bar, so that they reach the log file.
- Write numbers in CSV files with the rules of the `csv-files` skill.

## Documentation

Every function has documentation in the format of the language. The text follows "Voice and Style" and "Document Content" in the global `CLAUDE.md`, and so does the `--help` text.

## Comments

For functions with non-trivial logic (multiple steps, loops, branching, or domain-specific behavior), add inline comments that explain how the function works, not just what each line does. A reader should be able to follow the logic without re-deriving it. A client's own skill may point to a specific function in existing code as the model to follow.

## Plotting

The language skill gives the code.

- Use a plain white background with light grid lines, not a grey default theme.
- Use the viridis color scale for categorical fills and colors. It is colorblind-safe and the same in every project.
- Format large counts on an axis with a thousands separator (1,200,000, not 1.2e+06).

## Data handling

The language skill gives the code.

- Read identifier columns (sample names, accessions) as text. A reader that guesses the type drops leading zeros (007 becomes 7), and the text NA in an identifier column can be read as a missing value.
- Keep column names exactly as they are in the file. Do not let the reader rewrite them.
- Write CSV files as the `csv-files` skill says.
