# R project setup

This file holds what is specific to R script projects (not package or Shiny application projects). The layout, naming, initialization steps, README content, and script structure that every script project shares are in the `scripting` skill. Read `references/coding.md` in this skill for the R code rules.

## R values

Use these values in the `scripting` setup:

- File extension: `.R`. Script names are snake_case.

- Primary tool: `r-base=4.5`. Extra packages: `r-cli`, `r-logging` and `r-optparse`.

- `.gitignore` entries: the R entries below.

- Run command: `Rscript src/[project_name].R [arguments]`, in the project's environment (`mamba run -n [project-name] Rscript src/[project_name].R`).

- Parse check: `mamba run -n [project-name] Rscript -e 'invisible(parse("src/[project_name].R"))'`.

Make the script follow the R sections of `references/coding.md`:

- `optparse` with `--log-level` and `--log-file` ("Command-line Arguments")

- logging with `setup_logging()` ("Logging Configuration")

- `cli` progress bars for loops over records or files ("Progress bars")

- error handling with the standard exit codes ("Error Handling and Exit Codes")

- roxygen2 documentation on every function ("Function Documentation")

- libraries in base R, third-party, local order, with the packages in one `suppressPackageStartupMessages()` block ("Library Loading")

When you validate, also run the parse check.

## File Templates

### config/[project-name].yml Template

This file specifies the conda environment for the project. R-specific entries:

- Pin `r-base=4.5` when the yml is created.

- Include `r-cli`, `r-logging` and `r-optparse`. Every other R package has the conda name `r-<package>` in lowercase (for example `r-ggplot2`). Leave them unpinned until the environment resolves.

- Pin all other packages after the environment resolves (see "Environment yml" in the `project-setup` skill).

### src/[project_name].R Template Structure

The R template has two parts that the Python template does not. `format_log_line()` is there because the `logging` package has no line format that matches the Python one: it passes the time as text and leaves the name of the root logger empty. The "Errors" section with `stop_invalid_data()` is there because R has no built-in error type for bad input data, where Python raises `ValueError`.

This file is the main script for the project. It follows the section order in "Script structure" in the `scripting` skill, and the standards in `references/coding.md`:

```r
#!/usr/bin/env Rscript
################################################################################
### [project_name].R
### [Contact block: see the nearest CLAUDE.md]
### [Description]
################################################################################

################################################################################
### Load libraries
################################################################################

suppressPackageStartupMessages({
  # Base R packages that R does not attach by default (alphabetical order within group)
  # Add them here if needed (e.g., library(tools))

  # Third-party packages (alphabetical order within group)
  library(cli)
  library(logging)
  library(optparse)
  # Add other third-party packages here (e.g., dplyr, ggplot2, etc.)
})

# Local scripts (alphabetical order within group)
# Add supporting scripts here if any (e.g., source("src/[project_name]_helper.R"))

# Note: Only load what is actually used. Remove unused libraries.

################################################################################
### Constants
################################################################################

LOG_LEVELS <- c("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")

################################################################################
### Command-line arguments
################################################################################

#' Parse command-line arguments
#'
#' Exits with status 2 when the arguments are invalid.
#'
#' @return A named list of the argument values.
parse_arguments <- function() {
  option_list <- list(
    make_option("--input-file", dest = "input_file", type = "character",
                metavar = "FILE", help = "Path to input file"),
    make_option("--output-dir", dest = "output_dir", type = "character",
                default = "results", metavar = "DIR",
                help = "Output directory (default: results)"),
    make_option("--log-level", dest = "log_level", type = "character",
                default = "INFO", metavar = "LEVEL",
                help = "Logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL (default: INFO)"),
    make_option("--log-file", dest = "log_file", type = "character",
                default = file.path("logs", "[project_name].log"), metavar = "FILE",
                help = "Path to log file (default: logs/[project_name].log)")
  )
  parser <- OptionParser(
    option_list = option_list,
    description = "[Brief description of the utility]",
    epilog = "For more information, see README.md"
  )
  args <- tryCatch(parse_args(parser), error = function(e) {
    message("Invalid command-line arguments: ", conditionMessage(e))
    quit(status = 2)
  })
  if (!(args$log_level %in% LOG_LEVELS)) {
    message("Invalid --log-level: ", args$log_level)
    quit(status = 2)
  }
  if (is.null(args$input_file)) {
    message("Missing required argument: --input-file")
    quit(status = 2)
  }
  args
}

################################################################################
### Logging configuration
################################################################################

#' Format a log line
#'
#' Gives the same line format as the Python scripts: date and time, logger name,
#' level, and message, separated by " - ". The root logger has no name, so `main`
#' is written in its place (the Python scripts write `__main__`).
#'
#' @param record A log record from the logging package
#' @return The log line as text
format_log_line <- function(record) {
  logger_name <- if (nzchar(record$logger)) record$logger else "main"
  sprintf("%s - %s - %s - %s", substr(record$timestamp, 1, 19),
          logger_name, record$levelname, record$msg)
}

#' Configure logging
#'
#' Each run starts a new log file, so the log holds only the latest run. Log
#' lines go to the log file only.
#'
#' @param log_level One of DEBUG, INFO, WARNING, ERROR, CRITICAL
#' @param log_file Path to the log file
setup_logging <- function(log_level, log_file) {
  dir.create(dirname(log_file), showWarnings = FALSE, recursive = TRUE)
  if (file.exists(log_file)) {
    file.remove(log_file)
  }
  invisible(removeHandler("basic.stdout"))
  setLevel(log_level)
  addHandler(writeToFile, file = log_file, level = log_level,
             formatter = format_log_line)
}

################################################################################
### Errors
################################################################################

#' Stop with an error that marks the input data as invalid
#'
#' @param message Description of what is wrong with the data
stop_invalid_data <- function(message) {
  stop(structure(
    class = c("invalid_data", "error", "condition"),
    list(message = message, call = NULL)
  ))
}

################################################################################
### Processing functions
################################################################################

#' Process a vector of records, with a progress bar
#'
#' Replace the body with the script's own work. Add more functions, in logical
#' groups, each with roxygen2 documentation.
#'
#' @param records A character vector of records to process
#' @return The number of records processed
process_records <- function(records) {
  processed <- 0
  for (i in cli_progress_along(records, "Processing records")) {
    processed <- processed + 1
  }
  loginfo("Processed %d records", processed)
  processed
}

################################################################################
### Main function
################################################################################

main <- function() {
  args <- parse_arguments()
  setup_logging(args$log_level, args$log_file)

  tryCatch({
    if (!file.exists(args$input_file)) {
      logerror("Input file not found: %s", args$input_file)
      quit(status = 3)
    }
    loginfo("Processing started")
    records <- readLines(args$input_file)
    # Call stop_invalid_data("what is wrong") for a problem in the input data.
    process_records(records)
    loginfo("Processing completed successfully")
  }, invalid_data = function(e) {
    logerror("Invalid data: %s", conditionMessage(e))
    quit(status = 4)
  }, error = function(e) {
    logerror("Unexpected error: %s", conditionMessage(e))
    quit(status = 1)
  })
}

if (sys.nframe() == 0) {
  main()
}
```

The main script:

1. Starts with the shebang line `#!/usr/bin/env Rscript`.

2. Calls `main()` only when it is run as a script (`sys.nframe() == 0`), so that `source()` loads the functions without running the analysis.

3. Loads its supporting scripts, if it has any, with `source()`.

### .gitignore Template

Append these entries to the template `.gitignore`:

```
# R
.Rhistory
.Rapp.history
.RData
.Ruserdata
.Rproj.user/
```
