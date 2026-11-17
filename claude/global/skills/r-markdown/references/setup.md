# R Markdown report setup

This file holds what is specific to starting a new R Markdown report. The report rules are in `references/coding.md` in this skill. The rules for the R code in the chunks are in the `r` skill.

## Report values

1. File: `[project_name].Rmd`, in snake_case. Put it where the project keeps its reports. If the project does not show where, ask the user.

2. Packages for the environment yml: `r-rmarkdown`, `r-knitr`, and `r-ggplot2` for the plot in the template. Add any other package the report loads. Follow "Environment yml" in the `project-setup` skill: add them unpinned, and pin them once the environment resolves.

3. Render command: `Rscript -e 'rmarkdown::render("[project_name].Rmd", params = list(input_file = "data.csv"))'`, run in the project's environment.

## Starting a report

1. Copy `assets/report-template.Rmd` to the report's place and name it as in "Report values".

2. Replace the placeholders: the title (in the front matter and in `report_title`), `[project_name]`, the description, and the contact block. Find the contact block with the rule under "Placeholders" in the `project-setup` skill.

3. In a client project, read the client's own report skill (if it has one) for the author, logo, and css values, and put them in the `Report Metadata` and `Styling` params.

4. Keep the param groups in the order of "YAML front matter" in `references/coding.md`, and delete the groups and the sections the report does not need.

5. Render the report with the render command, using a small CSV file with the columns `sample` and `reads`, and open the HTML file. The report must render before the sections are changed.

## What the template contains

1. The front matter, with the param groups `Report Metadata`, `Styling`, `Input Files`, and `Section Control`.

2. The chunks `setup`, `load_libraries`, `helper_functions`, and `load_data`, which do not show in the report.

3. A header chunk that adds the style sheet, the logo, and the author when the params give them.

4. One example section with a table and a plot. Each section is switched on and off by a `show_*` param, runs only when the data loaded, and reports a failure in the text.

5. A chunk that tells the reader when the input table could not be read.
