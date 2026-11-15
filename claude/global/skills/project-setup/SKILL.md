---
name: project-setup
description: Use whenever the user starts a new project, or asks for a README, an environment yml, or a .gitignore file. Creates the starting files and folders, and works with the readme skill and the language skills. Also defines the project naming convention, the environment yml rules, the default .gitignore, and the folder conventions (assets/, data/, results/, numbered output folders).
---

# Project setup conventions

These conventions apply to every new project, whatever the language. Follow the setup procedure first, then use the sections below as reference.

## Setup procedure

1. Confirm `[project-name]` with the user if the folder name is unclear. Compute `[project_name]` and `[YEAR]` (see "Placeholders").

2. Read the language or pipeline skills that apply (`python`, `nextflow`, etc), and the client-specific language skill. They give:
    - `[env-dir]`
    - the primary tool and its version
    - the extra dependencies
    - the folders and files to create
    - the `.gitignore` entries to append

3. Find the contact block (see "Placeholders").

4. Create the folders in which setup also creates a file: `[env-dir]/` and any code folder the language skills name (for example `src/`). Other folders are created when they are first needed (see "Folders").

5. Copy `assets/environment.yml` to `[env-dir]/[project-name].yml`. Fill in the name, the primary tool with its version, and the dependencies the language skills name. Pin only the primary tool (see "Environment yml").

6. Copy `assets/gitignore` to `.gitignore` at the project root and append the entries from the language skills.

7. Create `README.md` by following "Creating a first README" in the `readme` skill.

8. Create the other starting files that the language skills name.

9. Create the environment with `mamba env create -f [env-dir]/[project-name].yml`. Do not activate it. Once it resolves, pin the versions (see "Environment yml"). If a language skill needs the environment earlier, create it at that point instead.

10. Tell the user what was created, which placeholders remain, and which version pins were written to the yml. Do not run `git init`.

## Placeholders

- `[project-name]` — the project folder basename. Hyphens are kept. Use it in prose, README titles, URLs, and the `name:` field of the environment yml.

- `[project_name]` — the same name with every hyphen replaced by an underscore. Use it only where a file name or an import needs it. If the folder name has no hyphens, the two are the same.

- `[YEAR]` — the current year, four digits.

- `[Contact block]` — the block at the top of the README, including the copyright line. Templates write it as `[Contact block: see this client's CLAUDE.md]`.

    - Take it from the `CLAUDE.md` closest to the project folder (the nearest one above it that has a "Contact block" section).
    - For client work, if no client `CLAUDE.md` has a block, use the Trophic Nexus block.
    - If no block is found, or it is unclear which one applies, ask the user which block to use. Never invent a block or reuse another client's block.
    - Replace `[YEAR]` and `[project-name]` inside the block before writing it to the README.

## Environment yml

Every project has an environment yml named after the project. The folder it lives in (`[env-dir]`) is determined by the language skills.

1. Pin the primary tool or language version when the yml is created (for example `python=3.11`, or `nextflow=25.10.4`).

2. Leave every other package unpinned when the yml is created. A complex environment may not resolve with versions chosen in advance.

3. After `mamba env create` succeeds, read the installed versions with `mamba list -n [project-name]` and write them into the yml as `package=version`. The lines of `mamba list` start with spaces, so match with `grep -E "^ *package "`, not `"^package "`.

4. When a new package is needed later, add it to the yml unpinned, run `mamba env update -f [env-dir]/[project-name].yml`, and pin its version once the update succeeds.

5. Prefer packages from conda-forge and bioconda. Use pip only for packages that conda does not have.

6. List dependencies in alphabetical order.

7. Include `pip` and a `pip:` subsection only if a pip-only package is needed.

8. Run code and tools in the project's environment. In Claude Code, activation does not last between commands, so use `mamba run -n [project-name] <command>`.

Start from `assets/environment.yml`.

## .gitignore

Every project needs a `.gitignore`. Copy `assets/gitignore` to `.gitignore` at the project root, then append the `.gitignore` entries from each language skill that applies to the project (for example the Python entries, the Nextflow entries, the R entries).

## Folders

Setup creates the folders listed in step 4 of the setup procedure. Create each folder below when the project first needs it.

- `assets/` — supporting files that are not code, config, or output: reference sequences, databases, samplesheets, schema files, small test files. Tracked by git.

- `data/` — local copies of large input files: fastq files, bam files, other large files. Ignored by git.

- `logs/` — log files. Ignored by git.

- `results/` — output files, organized by step. Ignored by git.

- `work/` — scratch space for workflow runs. Ignored by git.

Output folders:

- Multi-step outputs use numbered prefixes in execution order: `01_<step>/`, `02_<step>/`, and so on (for example `results/01_fastqc/`, or `${outdir}/01_FASTQC/` in a Nextflow `publishDir`).

- Single-step outputs use a descriptive, lowercase, underscore-separated name.
