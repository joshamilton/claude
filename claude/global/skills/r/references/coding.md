# R coding conventions

Conventions for any R code, whether it is in a script, a package, or the chunks of an R Markdown report. The sections "Command-line Arguments", "Logging Configuration", and "Error Handling and Exit Codes" apply to command-line scripts only. See `references/setup.md` in this skill for the R values and the script template, and the `scripting` skill for the rules every command-line script follows.

## Quick Reference: Required Standards for Scripts

When creating or modifying an R script, meet all of the following. Together they make every script run and fail in the same way, so that a reader who knows one script can read the others:

- Arguments: `optparse`.

- Logging: the `logging` package, with `setup_logging(log_level, log_file)`.

- Progress: `cli`.

- Errors: `quit(status = n)`.

- Documentation: roxygen2 on every function.

- Libraries: `library()` calls in groups.

- Main: `if (sys.nframe() == 0)`.

## Command-line Arguments

Use the `optparse` package. Follow "Command-line flags" in the `scripting` skill, and these R details:

1. Use `OptionParser` with a `description` and an `epilog`.

2. Set `type` and `metavar` on every option, and set `dest` to the underscore form (`dest = "input_file"`), so the value is read as `args$input_file`.

3. Give every optional option a `default`.

4. Use `action = "store_true"` with `default = FALSE` for an on/off flag.

5. The default for `--log-file` is `file.path("logs", "<script>.log")`, with the script name written into the default.

6. Call `parse_args()` inside `tryCatch()` and exit with status 2 on an error: `optparse` exits with status 1 by itself, which is not the standard code. `optparse` has no list of allowed values, so check `--log-level` against the allowed values after parsing, and also exit with status 2.

See `parse_arguments()` in the script template in `references/setup.md`.

## Logging Configuration

Use the `logging` package. Follow "Logging" in the `scripting` skill, and these R details:

1. Log with `loginfo()`, `logwarn()`, `logerror()`, and `logdebug()`.

2. The package starts with a console handler named `basic.stdout`. Remove it with `removeHandler("basic.stdout")`, so that log lines go to the log file only.

3. The package appends to an existing file, so remove the old file before adding the file handler.

4. Create the log folder with `dir.create(dirname(log_file), showWarnings = FALSE, recursive = TRUE)`.

5. Set the line format with a `formatter` function given to `addHandler()`. The package passes the time as text, so take its first 19 characters (`substr(record$timestamp, 1, 19)`). The root logger has no name, so write `main` in its place. Python writes `__main__` there, so this is the one place where the log lines of the two languages differ.

See `setup_logging()` and `format_log_line()` in the script template in `references/setup.md`.

## Progress bars

Use the `cli` package. It plays the role that `tqdm` plays in Python, and the tidyverse already depends on it.

1. Wrap the thing you loop over: `for (i in cli_progress_along(items, "Processing")) { ... }`.

2. For a loop where the number of steps is not the length of a vector, use `cli_progress_bar("Processing", total = n)`, call `cli_progress_update()` once per step, and call `cli_progress_done()` at the end.

3. `cli` draws nothing for a loop that finishes in about two seconds. Use `clear = FALSE` in `cli_progress_bar()` to keep the finished bar on the screen.

4. Do not report with `cli_alert_*()` or `cli_text()`: use the log.

See `process_records()` in the script template in `references/setup.md`.

## Error Handling and Exit Codes

Follow "Exit codes" in the `scripting` skill, and these R details:

1. Set the exit code with `quit(status = n)`, and never let an error end the script without a status.

2. Wrap the main logic in `tryCatch()`:

   - a condition of class `invalid_data` -> log the error, exit with code 4

   - any other `error` -> log the message, exit with code 1

3. Signal bad input data with `stop_invalid_data("message")`, which raises an error of class `invalid_data`.

See `main()` and `stop_invalid_data()` in the script template in `references/setup.md`.

## Function Documentation

Follow "Documentation" in the `scripting` skill, and these R details:

1. Document every function with roxygen2: a one-line summary, an optional longer description, `@param` for each parameter, and `@return`.

See any function in the script template in `references/setup.md`.

## Library Loading

Load libraries in this order, with the packages of each group in alphabetical order:

1. Base R packages that R does not attach by default (for example `tools`, `parallel`). R attaches `stats`, `graphics`, `grDevices`, `utils`, `datasets`, and `methods` on its own, so do not load those.

2. Third-party packages.

3. Local scripts, loaded with `source()`.

Put the `library()` calls of groups 1 and 2 inside one `suppressPackageStartupMessages({ ... })` block. See "Load libraries" in the script template in `references/setup.md`.

## R Code Style

1. Use `<-` for assignment, and snake_case for function and variable names, and UPPER_CASE for constants.

2. Use two spaces for indentation.

## Plotting

Follow "Plotting" in the `scripting` skill, with these ggplot2 details:

1. Use `theme_bw()` + `theme()`, rather than the default gray theme.

2. Use `scale_fill_viridis_d()` and `scale_color_viridis_d()` with `option = "viridis"` and `na.value = "grey90"`, so that missing values are light gray.

3. Format large counts on an axis with `scale_y_continuous(labels = function(x) format(x, big.mark = ",", scientific = FALSE))`.

Example:

```r
ggplot(df, aes(x = sample, y = reads, fill = group)) +
  geom_col(position = "dodge") +
  scale_fill_viridis_d(option = "viridis", na.value = "grey90") +
  scale_y_continuous(labels = function(x) format(x, big.mark = ",", scientific = FALSE)) +
  theme_bw()
ggsave(file.path(output_dir, "reads_by_sample.png"), width = 6, height = 4)
```

## Data handling

Follow "Data handling" in the `scripting` skill, with these R details:

1. Name the identifier columns as text with `colClasses`, and keep the column names with `check.names = FALSE`, because `read.csv()` otherwise rewrites them (`a b` becomes `a.b`): `read.csv(path, colClasses = c(sample = "character"), check.names = FALSE)`.

2. With `readr`, name the identifier columns with `col_types`: `read_csv(path, col_types = cols(sample = col_character()))`. It keeps the column names as they are.
