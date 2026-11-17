---
name: r-markdown
description: Use when writing, editing, or reviewing any R Markdown (.Rmd) report, for personal or client work. Covers the report structure: YAML params and their groups, chunk naming and options, helper functions, error handling in a report, conditional sections, and markdown and HTML output. The R code inside the chunks follows the `r` skill.
---

# R Markdown

This skill covers the structure of an R Markdown report, whatever its subject. The rules for the R code inside the chunks are in the `r` skill. This skill gives only what is specific to a report. Content that belongs to one client, such as branding, is in that client's own report skill. It has two reference files and one template:

- `references/setup.md` - read this when starting a new report. It covers:

    - the file name, the packages, and the render command

    - the steps to start a report from the template

    - what the template contains

- `references/coding.md` - read this when writing, editing, or reviewing any R Markdown report. It covers:

    - YAML front matter and params

    - chunk conventions, including helper functions

    - error handling in a report

    - markdown and HTML conventions

- `assets/report-template.Rmd` - the starting point for a new report. Copy it, and replace the placeholders.
