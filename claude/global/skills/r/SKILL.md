---
name: r
description: Use when starting a new R script project, adding a script to one, or writing, editing, or reviewing R code, in a script or in the chunks of an R Markdown report, for personal or client work. Gives the R values for a new project and the required code patterns.
---

# R

This skill covers R script projects (not package or Shiny application projects). The layout, naming, initialization steps, README content, and rules that every script follows are in the `scripting` skill. This skill gives only what is specific to R. It has two reference files:

- `references/setup.md` - read this when scaffolding a brand-new project, or adding a new script to an existing one. It covers:

    - the R values for the `scripting` setup (version, extra packages, run command)

    - the config/*.yml and src/*.R templates

    - the .gitignore entries

- `references/coding.md` - read this when writing, editing, or reviewing any R code. It covers:

    - command-line arguments

    - logging

    - error handling and exit codes

    - roxygen2 documentation

    - library loading

    - plotting and data handling

Run R and every command-line tool inside the project's environment. How to run a command there, and the version pinning rules, are in "Environment yml" in the `project-setup` skill.
