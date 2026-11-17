# R Markdown report conventions

The report structure of any R Markdown report, regardless of subject matter: YAML params, chunks, and markdown output. The R code in the chunks follows the `r` skill (library loading, code style, roxygen2 documentation, plotting, data handling). The sections of the `r` skill on command-line arguments, logging, and exit codes are for command-line scripts and do not apply to a report.

## YAML front matter

Group `params` under clear headings so the front matter stays readable as it grows. Follow these rules:

1. Use this order, with a comment above each group: Report Metadata, Styling, Input Files, Metadata Analysis, Section Control. Skip a group entirely if a report has nothing for it.

2. Add a new param under the appropriate existing group. Ask the user before adding a new group.

3. For a param whose value comes from outside the report (passed in by a calling pipeline rather than written in the file), default to `NULL` and add a comment saying where the value comes from, for example `# will get passed in by the calling pipeline`.

4. Use boolean `params$show_*` flags to switch optional sections on or off. Check both the flag and that the data loaded, in the `eval` condition of the chunk (see "Chunk conventions").

Example:

```yaml
params:
  # Report Metadata
  report_title: NULL
  report_author: NULL
  pipeline_name: NULL
  # Styling
  logo: NULL
  css: NULL
  # Input Files
  samplesheet: NULL
  # Section Control
  show_summary: true
  # ... etc.
```

The values of `report_author`, `logo`, and `css` (branding) come from the client's own report skill. The `Input Files`, `Metadata Analysis`, and `Section Control` params differ from report to report.

## Chunk conventions

Follow the `r` skill for the R code in a chunk, and these report details:

1. Use descriptive snake_case chunk names (for example `load_libraries`, `helper_functions`).

2. Use `include=FALSE` for setup, data-loading, and helper-function chunks.

3. Use `results='asis'` for chunks that write markdown with `cat()`.

4. Use `eval=params$show_* && ...` to run a section only when it is wanted. Check both the show flag and that the required data actually loaded (for example `eval=params$show_summary && !is.null(samplesheet_data)`).

5. Set `fig.height` and `fig.width` explicitly rather than relying on the defaults.

6. Start the `setup` chunk with a banner comment that holds a title line and the contact block, as the header of a script does. Find the block with the rule under "Placeholders" in the `project-setup` skill, fill in `[YEAR]` and `[project-name]`, and start each line of the block with `### `.

7. Place new helper functions in the `helper_functions` chunk, in logical order. Document each one with roxygen2, as "Function Documentation" in the `r` skill says.

## Error handling in a report

A report differs from a script (see "Error Handling and Exit Codes" in the `r` skill): after a failure it keeps rendering, and says what failed in the text. Follow these rules:

1. Use `tryCatch()` when loading external data or generating plots.

2. Report a failure with a user-facing `cat()` message, so that the report still renders.

Example:

```r
tryCatch({
  plot_thing(data)
}, error = function(e) {
  cat("Error generating thing:", e$message, "\n")
})
```

## Markdown and HTML conventions

Follow these rules for the text that a report writes:

1. Write dynamic headers and text with `cat()` under `results='asis'`: `cat("# Section Title\n\n")`.

2. Mark section boundaries with HTML comments: `<!-- Section Name -->`.

3. Use pandoc divs for styled blocks: `::: div-class`.

4. Use `## Section {.tabset}` for tabbed subsections, with `### Tab Title` for each tab.
