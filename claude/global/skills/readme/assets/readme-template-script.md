# [project-name]

[Contact block: see the nearest CLAUDE.md]

## Overview

[What the tool does, and for whom. Keep it short.]

Key features:

- [Feature, one line]

Processing overview:

1. [What happens first: the tool and its purpose]

2. [What happens next]

## Installation

### Setup mamba

```bash
curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
bash Miniforge3-$(uname)-$(uname -m).sh
```

[Other prerequisites, if any]

### Create the environment

```bash
mamba env create -f [env-dir]/[project-name].yml
mamba activate [project-name]
```

## Usage

[Where the inputs live, as a compact list]

Main parameters:

- `--[flag]` - [Default, if any, and one short phrase.]

Steps:

1. [User action]

2. [User action, ending with the copy-paste command]

Minimal example:

```bash
[run-command] [Shortest valid command: required arguments only]
```

Explicit form (same defaults as above, all paths and tunables shown):

```bash
[run-command] [Same command with every option that takes a value spelled out]
```

`[run-command]` is the command that starts the script, for example `python src/[project_name].py` or `Rscript src/[project_name].R`.

## Results

[Where the output files live, which ones matter for the next step, and which are diagnostic or scratch]

## Detailed Usage

[Flag-by-flag explanations, per-stage behavior, and exit codes. Use one subheading per program or stage.]

## Testing

[Keep this section only if the user asked for tests. Otherwise delete it.]

## Repo structure

```text
[project-name]/
|-- README.md
|-- .gitignore
|-- [env-dir]/
|   `-- [project-name].yml
`-- [code folder from the language skill, with the main file]
```

[One line on the purpose of each folder and main file. Add folders to the tree when they are created.]
