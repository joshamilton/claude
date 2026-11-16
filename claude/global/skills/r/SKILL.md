---
name: r
description: Use when starting a new R script project, adding a script to one, or writing, editing, or reviewing R code, in a script or in the chunks of an R Markdown report, for personal or client work. Covers the R values for a new project (version, packages, run command, script template) and the required code patterns (command-line arguments, logging, exit codes, roxygen2 documentation, library loading, plotting, data handling).
---

# R

This skill covers R script projects (not package or Shiny application projects). The layout, naming, initialization steps, README content, and rules that every script follows are in the `scripting` skill. This skill gives only what is specific to R. It has two reference files:

- `references/setup.md` — read this when scaffolding a brand-new project, or adding a new script to an existing one. It covers:
    - the R values for the `scripting` setup (version, extra packages, run command)
    - the config/*.yml and src/*.R templates
    - the .gitignore entries

- `references/coding.md` — read this when writing, editing, or reviewing any R code. It covers:
    - command-line arguments
    - logging
    - error handling and exit codes
    - roxygen2 documentation
    - library loading
    - plotting and data handling

Run R and every command-line tool the project needs inside the project's environment, using `mamba run -n [project-name] Rscript src/[project_name].R`. Activation does not last between shell commands in Claude Code. Version pinning rules are in `project-setup` ("Environment yml").

Both files assume the global standing instructions (`~/.claude/CLAUDE.md`) are already in effect: interaction style and documentation/writing standards live there.
