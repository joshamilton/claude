# README structure

These rules define how to draft and revise `README.md`: the section order, what belongs in each section, and how to show commands. Start the README of a new script project from `assets/readme-template-script.md`, and the README of a Nextflow pipeline from `assets/readme-template-nextflow.md`.

Script projects and pipelines share one structure. Pipelines also have the sections marked "Nextflow" below.

## 1. Fixed section order

Unless the user explicitly directs otherwise, use this order in `README.md`:

1. Title and contact block
2. Overview (see section 2)
3. Installation (see section 3)
4. Usage (see section 4)
5. Results (see section 5)
6. Detailed Usage (see section 6)
7. Deployment (see section 9; Nextflow only)
8. Development Guidelines (see section 9; Nextflow only)
9. Testing (see section 9; optional for a script project, mandatory for a pipeline)
10. Repo structure (see section 10)

Add other sections only where they fit without displacing this spine.

## 2. Overview content

The Overview must stay short and readable. Include:

- What the pipeline or tool does.
- Key features: a short bulleted list, one line per bullet.
- Processing overview: a numbered list in execution order. Each item is one to three lines. Use prose. Name the tool and its purpose. Do not list command-line flags; defer details to the "Detailed Usage" section. Avoid labels like "step 00" and numeric directory names. For a pipeline, use the list of modules.

## 3. Installation

Installation includes the prerequisites.

- The first subsection is the mamba setup and any other prerequisite.
- Then come the commands that clone the repository and create the environment from `[env-dir]/[project-name].yml`.
- For a pipeline, the cloud setup text (credentials, the head node) comes from `aws.md` or `gcp.md` in the `nextflow` skill's `references/` folder.

## 4. Usage

The Usage section is for getting someone up and running. Include only:

- Activating the environment.
- Where inputs live, in a compact list.
- A concise list of the main CLI parameters: flag, default if any, and one short phrase for each (use the list pattern in section 9).
- A numbered list of user actions ending with copy-paste commands.
- Two command examples for the same logical operation: one minimal and one fully explicit (see below).

### 4a. Minimal example

Show the shortest command that is valid for typical use (required arguments only). Omit arguments that match the program defaults.

Example:

```bash
mamba activate pipeline
python src/pipeline.py --samplesheet assets/samplesheet.csv --resume
```

### 4b. Fully explicit examples

Show the same command with every option spelled out on the command line, so a reader can see values without opening `--help`. Use project-realistic values.

- List every optional argument that takes a value (`--log-file`, `--results-dir`, thread counts, etc).
- For `argparse` `store_true` flags, include the flag.
- Introduce the block with one line of intent, for example: "Explicit form (same defaults as above, all paths and tunables shown):".
- Write flags and paths in inline code.
- Use em dashes in parameter lists with many options.

Example:

```bash
python src/pipeline.py \
  --log-file logs/pipeline.log \
  --log-level INFO \
  --samplesheet assets/samplesheet.csv \
  --results-dir results \
```

Adapt the same pattern for other scripts or pipelines (`setup.py`, `download_data.py`, and so on).

## 5. Results section

Summarize:

- where results live (using a directory tree or table)
- which files matter for the next step
- what is diagnostic or scratch

## 6. Detailed Usage

Include:

- flag-by-flag explanations
- per-stage outputs
- checksum and resume rules
- tool log behavior
- exit codes
- for a pipeline, an "Inputs" subsection with the input specification: samplesheet columns, validation rules, and reference files

Use subheadings per program or per stage so readers can jump in. Follow the list pattern in section 9.

## 8. Lists for CLI options

List CLI options in a README or long help text this way:

- a labeled block title, then a blank line
- one hyphen bullet per option
- the flag (or path) in inline code, then an em dash (U+2014), then the description

For example:

Required arguments:

- `--sample-name` — Sample name; config is loaded from `config/<sample_name>/<sample_name>.yml`.
- `--output-dir` — Base output directory; results go to `<output-dir>/<sample_name>/`.

Optional arguments:

- `--log-file` — Log file path (default: `logs/screen.log`).
- `--log-level` — Logging verbosity (default: `INFO`).

Adapt the labels to the program at hand.

## 9. Nextflow-only sections

A pipeline README has these sections after Detailed Usage.

- Deployment:
    - Prerequisites: Docker Desktop, GitHub access, and the cloud access text from the cloud file (`aws.md` or `gcp.md` in the `nextflow` skill's `references/` folder).
    - Docker Containers: from `containers.md` in the `nextflow` skill's `references/` folder.
    - Cloud resources: from the cloud file (`aws.md` or `gcp.md` in the `nextflow` skill's `references/` folder).
    - Pipeline assets and external resources that must exist before a production run.
- Development Guidelines:
    - A table of the nf-core lint tests the pipeline disables.
    - One row for every flag in the pipeline's `.nf-core.yml`, with the nf-core check it skips and the reason.
    - Any subsections a client skill adds, after the table.
- Testing:
    - The test layers table.
    - The pre-commit hook.
    - GitHub Actions CI, when the cloud has a CI workflow.
    - The integration test commands, which mirror the production `nextflow run` commands.

## 10. Repo structure

Show a tree of the files and folders that exist now, with one line on the purpose of each folder and main file. Add to the tree when a folder or main file is created.
