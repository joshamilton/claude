---
name: readme
description: Use when writing, editing, or reviewing the README.md of a script project (Python or R) or a Nextflow pipeline, including the first README of a new project, or when a change to command-line options, defaults, outputs, or directory layout makes a README out of date. Writes READMEs in a fixed section order, and provides a template for each project type.
---

# README files

One reference file and two templates:

- `references/structure.md` — read this whenever drafting or revising a README. It covers:
    - the fixed section order
    - what goes in the Overview
    - how short Usage must stay
    - how to show commands
    - the Results and Detailed command-line usage sections
    - the list pattern for command-line options
    - the sections unique to pipelines

- `assets/readme-template-script.md` — the starting point for the README of a script project (Python or R).

- `assets/readme-template-nextflow.md` — the starting point for the README of a Nextflow pipeline. The text that depends on the cloud or on the container strategy comes from `aws.md`, `gcp.md`, and `containers.md` in the `references/` folder of the `nextflow` skill.

In both templates, copy the file to the project root, replace the `[placeholders]`, and delete what does not apply. `[env-dir]` is the folder that holds the environment yml: `config` in a Python script project, `conf` in a Nextflow pipeline.

For a new project, the `project-setup` skill runs first and calls this skill to create the README. The language or pipeline skill sets `[env-dir]` and the code folder.

## Creating a first README

1. Copy the template for the project type to `README.md` at the project root:
    - `assets/readme-template-script.md` for a script project
    - `assets/readme-template-nextflow.md` for a Nextflow pipeline

2. Keep the title as `[project-name]`, replaced with the project folder basename.

3. Replace the `[Contact block: ...]` line with the contact block. Find it with the rule under "Placeholders" in the `project-setup` skill, and fill in `[YEAR]` and `[project-name]` inside it. If no block is found, ask the user.

4. Write the Overview from what the user has said: what the tool does and for whom, the key features, and the processing overview. If that is not enough, ask instead of guessing.

5. In Installation, replace `[env-dir]` with the folder that holds the environment yml.

6. For a pipeline, find the client's cloud (AWS or GCP) in the cloud table of the client `CLAUDE.md`, and the pipeline's container strategy in its `nextflow.config`. If either is not recorded, ask the user. Read the cloud file and `containers.md` in the `references/` folder of the `nextflow` skill, and paste their sections into the bracketed template lines that begin with "Cloud:" or that point to `containers.md`. Fill in the cloud placeholders from the cloud table in the client `CLAUDE.md`. Add the sections and rows that the client skill asks for.

7. In Repo structure, list the files and folders that exist now. Add to the tree as more are created.

8. Leave Usage, Results, and Detailed command-line usage as their bracketed placeholders. They cannot be written before the code exists. For a pipeline, also leave Deployment, Development Guidelines, and Testing as their placeholders. For a script project, delete Testing unless the user asked for tests.

9. Tell the user which placeholders remain.

## Keeping the README current

Keep the README in step with the code. When a change alters command-line behavior, defaults, outputs, or directory layout, update the README in the same change set:

- Overview, if the scope of the tool changes.
- Usage, if the default path or the minimal command changes.
- Results, if outputs move.
- Detailed command-line usage, if there are new or updated command-line options, flags, or exit codes.

This skill assumes the global standing instructions (`~/.claude/CLAUDE.md`) are already in effect, in particular "Voice and Style" and "Document Format".
