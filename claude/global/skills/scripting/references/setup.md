# Script project setup

This file holds the setup that is the same for every script project, whatever the language. The language skill gives language-specific values, including:

    - the version of the language to use

    - its extension (`.py`, `.R`, etc)

    - additional packages to use

    - how to run the script

    - required `.gitignore` entries

    - a script template

Read `references/coding.md` in this skill for the rules every script follows. Read "Voice and Style" and "Document Format" in the global `CLAUDE.md` for the writing standards.

## Project Type

The structure is for command-line utilities and executable scripts. Each project has a `[project-name]` that corresponds to the project folder: /path/to/[project-name].

### Naming: project folder vs script files

- The project folder basename may use hyphens, underscores, or a mix (for example `my-analysis`, `my_analysis`).

- Script file names under `src/` always use snake_case: lowercase words separated only by underscores. Never use hyphens in script file names.

- `[project_name]` and `[project-name]` are defined under "Placeholders" in the `project-setup` skill. Use `[project_name]` in script file names, and `[project-name]` in prose and in the environment `name:`.

## Project Structure

Create the following required files:

- `README.md`

- `config/[project-name].yml`

- `src/[project_name].<ext>`, where `<ext>` is the extension the language skill names

Optional folders (`assets`, `data`, `results`, etc) follow "Folders" in the `project-setup` skill. Document output file formats in `README.md`.

Keep source code (`src`), configuration (`config`), and assets in separate folders. When you change outputs, flags, or layout, update `README.md` in the same change set (see "Document Content" in the global `CLAUDE.md`).

### The src folder

`src/` holds the executable scripts. The main script is `[project_name].<ext>`. Further scripts use the same naming rule, for example `[project_name]_helper.<ext>` for supporting functions. Add more scripts when the main one gets too large. If the script has several operating modes, each mode may have its own script, with another script for the functions they share. A function that two or more scripts need lives in one shared script (for example `[project_name]_helper.<ext>`), and the scripts import it from there. Do not copy the same logic into several scripts. When you move a function into the shared script, update every import that used the old copy. If the scripts run sequentially (e.g., to carry out an extended analysis), the scripts should be numbered sequentially with a descriptive name: `01_<description>.<ext>`, `02_<description>.<ext>`, etc.

## Project Initialization Workflow

Follow these steps in order:

1. Follow the "Setup procedure" in the `project-setup` skill, with these values:

    - `[env-dir]` is `config`.

    - The primary tool, its version, and the extra packages (from the language skill).

    - Folders created: `config/` and `src/`.

    - Extra starting file: `src/[project_name].<ext>`, with the structure in "Script structure" below.

    - `.gitignore` entries: from the language skill.

2. Make the script follow the rules in `references/coding.md`:

    - flags, with `--log-level` and `--log-file`

    - logging, with a fresh log file for each run

    - the standard exit codes

    - progress for loops over records or files

    - the documentation and library-loading rules of the language skill

3. Validate. Run every command in the project's environment, with `mamba run -n [project-name]`:

    - the YAML file and the script parse without errors

    - the script runs with `--help`

    - the script exits with status 3 when the input file is missing

    - all placeholders are replaced, and `[project-name]` and `[project_name]` are used consistently

    - the project name, URLs, and contact information agree across all files

    - the file structure matches this specification

4. Review the complete structure before completion.

## README content

The `project-setup` procedure creates the README from `assets/readme-template-script.md` in the `readme` skill, including the contact block. The content that follows from the layout:

- Installation uses `config/[project-name].yml`.

- Usage runs the main script, with the run command from the language skill.

- Repo structure lists `config/`, `src/`, and any of `assets/`, `data/`, `results/` that exist.

## Environment yml

Create `config/[project-name].yml` following "Environment yml" in the `project-setup` skill. Pin only the primary tool when the file is created. Include the extra packages from the language skill, and leave them unpinned until the environment resolves. Then pin everything.

## Script structure

The main script has these sections, in this order. Each section starts with a full-width comment banner. The language skill gives the code.

1. Header: the script name, the contact block, and a one-line description. In a language with a shebang line, the shebang comes first.

2. Libraries or imports, grouped and in alphabetical order. Load only what the script uses.

3. Constants and configuration.

4. Command-line arguments.

5. Logging configuration.

6. Functions, in logical groups, each with its documentation.

7. The main function:

    - parse the arguments

    - set up logging

    - check the inputs

    - do the work inside error handling

    - exit with the standard codes.
The main function runs only when the file is run as a script, not when another file loads it.
