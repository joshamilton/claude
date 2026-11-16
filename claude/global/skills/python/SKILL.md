---
name: python
description: Use when starting a new Python script project, adding a script to one, or writing, editing, or reviewing Python code, for personal or client work. Covers the Python values for a new project (version, packages, run command, script template) and the required code patterns (argparse, logging, progress bars, error handling, type hints, docstrings, import order, plotting with seaborn, data handling with pandas).
---

# Python

This skill covers Python script projects (not package or notebook projects). The layout, naming, initialization steps, README content, and rules that every script follows are in the `scripting` skill. This skill gives only what is specific to Python. It has two reference files:

- `references/setup.md` — read this when scaffolding a brand-new project, or adding a new script to an existing one. It covers:
    - the Python values for the `scripting` setup (version, extra package, run command)
    - the config/*.yml and src/*.py templates
    - the .gitignore entries

- `references/coding.md` — read this when writing, editing, or reviewing any Python code. It covers:
    - logging
    - argparse
    - error handling and exit codes
    - type hints
    - docstrings
    - import organization
    - plotting and data handling

Run Python and every command-line tool the project needs inside the project's environment, using `mamba run -n [project-name] <command>`. Activation does not last between shell commands in Claude Code. Check that `mamba run` works on the user's install before the first use. Version pinning rules are in `project-setup` ("Environment yml").

Both files assume the global standing instructions (`~/.claude/CLAUDE.md`) are already in effect: interaction style and documentation/writing standards live there.
