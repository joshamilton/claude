# Shared Nextflow project setup

Conventions shared by every Nextflow pipeline. Each client's own `<client>-nextflow` skill's `references/setup.md` builds on this: it adds client-specific setup steps, and states only what's actually different about that client.

## nf-core template integration workflow

The general shape every pipeline's init follows, in order:

1. Determine placeholders from the project folder (project name, and its underscored form for workflow files).
2. Create the environment yml and `.gitignore` (see the `project-setup` skill for the shared parts, and this client's own `<client>-nextflow` skill for the Nextflow-specific additions).
3. Create `pipeline.yml` for `nf-core pipelines create` (see "pipeline.yml skip_features" below).
4. Create the conda environment and generate the nf-core template:
   ```bash
   mamba env create -f conf/[project-name].yml
   mamba activate [project-name]
   nf-core pipelines create --template-yaml pipeline.yml
   ```
5. Integrate the generated `nf-[project-name]/` directory into the project root:
   - Move all contents to the repo root.
   - Preserve `conf/[project-name].yml` if nf-core overwrote it.
   - Delete the empty `nf-[project-name]/` directory and the temporary `pipeline.yml`.
   - Delete `assets/nf-core-[project-name]_logo_light.png` and the `docs/` folder.
6. Fix Nextflow workflow file naming: Nextflow does not allow hyphens in workflow names or in file paths used in `include` statements:
   - Rename `workflows/[project-name].nf` to `workflows/[project_name].nf`.
   - Update `main.nf`'s `include` statement to `from './workflows/[project_name]'`.
   - Use underscores in the workflow constant name and drop the `NFCORE_` prefix (for example `NF_MY_PIPELINE`, not `NFCORE_MY-PIPELINE`).
7. Remove nf-core branding (see "Removing nf-core references" below).
8. Configure pipeline logic, `nextflow.config`, modules, and workflow wiring: see this shared skill's `references/coding.md` and the client's own `<client>-nextflow` skill's `references/coding.md`.

Each client's own `references/setup.md` inserts its remaining steps around this skeleton (dev tooling, README, CI/WIF setup, asset templates) and says exactly where they fit relative to the steps above.

Create the README with the `readme` skill, using its Nextflow template, the cloud file for the client's cloud (`aws.md` or `gcp.md`), and `containers.md`. The cloud file and `containers.md` are in this folder.

## Removing nf-core references

After integrating the nf-core template, replace nf-core branding with the client's own identity. Keep functional dependencies on nf-core modules and subworkflows.

Files to update:

1. `main.nf` — header, GitHub URL, workflow name (drop `NFCORE_` prefix), `include` path with underscores.
2. `nextflow.config` — header, `manifest.name`, `homePage`, help examples use `nextflow run main.nf`.
3. `nextflow_schema.json` — `$id` and `title` (no `nf-core/` prefix).
4. `modules.json` — `name` and `homePage` (keep `nf-core` namespace entries under `modules`).
5. `assets/schema_input.json` — `$id` and `title`.
6. `conf/base.config` — header; change `// TODO nf-core:` to `// TODO:`.
7. `subworkflows/local/utils_nfcore_[project-name]_pipeline/main.nf` — comments only; keep `../../nf-core/` imports.

Files to delete:

- `assets/nf-core-[project-name]_logo_light.png`
- `docs/` (nf-core template docs folder)

Files to keep as-is (functional dependencies on nf-core, not branding):

- `modules/nf-core/` — vendored nf-core modules
- `subworkflows/nf-core/` — vendored nf-core subworkflows
- The `nf-core` package pin in the environment yml
- Module and subworkflow imports from nf-core paths in workflow files

Search and replace patterns:

- `nf-core/[project name]` → `[project name]`
- `NFCORE_[PROJECT-NAME]` → `[PROJECT_NAME]` (workflow names)
- `// TODO nf-core:` → `// TODO:`
- `https://github.com/nf-core/[project name]` → the client's own GitHub URL

Verify after making changes:

- All pipeline branding references use `[project name]` instead of `nf-core/[project name]`.
- All GitHub URLs point to the correct repository.
- Workflow names are consistent throughout the codebase.
- Functional dependencies on nf-core modules/subworkflows are preserved.
- The pipeline can still be executed successfully.

## pipeline.yml skip_features

Every client's `pipeline.yml` uses this exact `skip_features` list; only `name`, `description`, and `author` vary per client (see the client's own `references/setup.md` for those values):

```yaml
name: [project name]
description: [Pipeline description]
author: [client-specific: see this client's references/setup.md]
force: true
outdir: .
version: 0.0.1
skip_features:
  - github
  - github_badges
  - changelog
  - license
  - ci
  - test_config
  - nf-test
  - igenomes
  - multiqc
  - fastqc
  - nf_core_configs
  - is_nfcore
  - seqera_platform
  - gpu
  - codespaces
  - vscode
  - code_linters
  - citations
  - documentation
  - rocrate
  - email
  - adaptivecard
  - slackreport
  - gitpod
```

Temporary file; delete after `nf-core pipelines create` runs.

## Directory structure

Every pipeline organizes modules and subworkflows the same way:

```
modules/
├── local/       # Custom modules specific to this pipeline
└── nf-core/     # Vendored nf-core modules
subworkflows/
├── local/       # Pipeline-specific subworkflows
└── nf-core/     # Vendored nf-core subworkflows
```

## Installing nf-core modules and subworkflows

From the project's conda environment:

```bash
mamba activate [project-name]
nf-core modules install <module>
nf-core subworkflows install <subworkflow>
```

Modules install under `modules/nf-core/`; subworkflows under `subworkflows/nf-core/`. Nested modules (for example `kraken2/kraken2`) are valid.
