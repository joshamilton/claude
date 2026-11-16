---
name: scripting
description: Use when starting a new command-line script project in any language, adding a script to an existing project, or writing or reviewing such a script, for personal or client work. Covers the project layout and naming, the initialization steps, the README content, and the rules every script follows (command-line flags, logging, exit codes, results as files, comments, plotting, data handling).
---

# Scripting

This skill covers command-line script projects in any language (not packages, notebooks, or Shiny applications). The language skills (`python`, `r`) give the code. This skill gives everything that is the same in every language. It has two reference files:

- `references/setup.md` — read this when scaffolding a brand-new project, or adding a new script to an existing one. It covers:
    - the project type and structure
    - naming conventions
    - the initialization workflow and the checks at the end
    - the README content
    - the order of the sections in a script

- `references/coding.md` — read this when writing, editing, or reviewing any script. It covers the rules every script follows:
    - command-line flags
    - logging
    - exit codes
    - errors, progress, and results
    - documentation and comments
    - plotting
    - data handling

Run the script and every command-line tool the project needs inside the project's environment, using `mamba run -n [project-name] <command>`. Activation does not last between shell commands in Claude Code. Version pinning rules are in `project-setup` ("Environment yml").

Both files assume the global standing instructions (`~/.claude/CLAUDE.md`) are already in effect: interaction style and documentation standards live there.
