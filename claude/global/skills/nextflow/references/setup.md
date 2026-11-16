# Shared Nextflow project setup

Conventions shared by every Nextflow pipeline. A client's own `<client>-nextflow` skill, if it has one, holds only facts that belong to that client alone.

## nf-core template integration workflow

The general shape every pipeline's init follows, in order:

1. Determine placeholders from the project folder (project name, and its underscored form for workflow files), and from the Nextflow table in the client `CLAUDE.md` (see "Placeholders for Nextflow files" below).

2. Create the environment yml (see "Environment yml" below) and `.gitignore` (see the `project-setup` skill; Nextflow adds no `.gitignore` entries).

3. Create `pipeline.yml` for `nf-core pipelines create` (see "pipeline.yml skip_features" below).

4. Create the conda environment and generate the nf-core template:
   ```bash
   mamba env create -f conf/[project-name].yml
   mamba activate [project-name]
   nf-core pipelines create --template-yaml pipeline.yml
   ```

5. Integrate the generated `[org]-[project-name]/` folder into the project root. nf-core makes this folder a git repository of its own, and runs Nextflow in the current folder.
   - Delete `[org]-[project-name]/.git/` first, so it cannot replace the project's own repository.
   - Delete `[org]-[project-name]/README.md` and `[org]-[project-name]/.gitignore`. The project keeps its own `.gitignore`, and the README comes from the `readme` skill.
   - Move all remaining contents, including the hidden files, to the repo root.
   - Delete the empty `[org]-[project-name]/` folder, the temporary `pipeline.yml`, and the run files that nf-core leaves in the repo root: `null/`, `work/`, `.nextflow/`, and `.nextflow.log*`.

6. Fix Nextflow workflow file naming. The generated pipeline does not compile until this is done, because Nextflow does not allow hyphens in workflow names or in file paths used in `include` statements:
   - Rename `workflows/[project-name].nf` to `workflows/[project_name].nf`.
   - Update `main.nf`'s `include` statement to `from './workflows/[project_name]'`.
   - Use underscores in the workflow names, in `main.nf` and in the workflow file. nf-core writes `[PROJECT-NAME]` and `[ORG]_[PROJECT-NAME]`. Name the inner workflow `[PROJECT_NAME]` and the outer workflow in `main.nf` `NF_[PROJECT_NAME]`, for example `MY_PIPELINE` and `NF_MY_PIPELINE`, not `MY-PIPELINE` and `[CLIENT]_MY-PIPELINE`. The two names must differ: `main.nf` includes the inner workflow, and `nextflow lint` fails with "is already included" if the outer one has the same name.

7. Remove the remaining nf-core references (see "Removing nf-core references" below).

8. Configure pipeline logic, `nextflow.config`, modules, and workflow wiring: see this shared skill's `references/coding.md` (and the client's own `<client>-nextflow` skill, if it has one).

After the pipeline logic is configured, set up the development tooling if the pipeline has it (see "Development tooling" below), set up the GitHub Actions CI access for a pipeline on GCP (see "GitHub Actions CI access setup" in `gcp.md`), and create the README.

Create the README with the `readme` skill, using its Nextflow template, the cloud file for the client's cloud (`aws.md` or `gcp.md`), and `containers.md`. The cloud file and `containers.md` are in this folder.

## Removing nf-core references

Because `pipeline.yml` sets `org`, nf-core already writes the client's name in the headers, `manifest.name`, the schema `$id` and `title` fields, and `modules.json`. It writes no logo and no `docs/` folder. Three things remain.

GitHub URLs. nf-core writes `https://github.com/[org]/[project-name]`, which is wrong when the GitHub owner differs from `[org]`. Replace it with `[github-url]`, and `https://raw.githubusercontent.com/[org]/[project-name]` with `https://raw.githubusercontent.com/[github-owner]/[project-name]`, in:

- `main.nf` (header)
- `modules.json` (`homePage`)
- `nextflow_schema.json` (`$id`)

`nextflow.config` is replaced from `assets/nextflow.config` (step 4 of the procedure in `SKILL.md`), so it needs no changes here.

Samplesheet schema. Replace the generated `assets/schema_input.json` with `assets/starter/schema_input.json` from this skill, for every pipeline. The two files differ only in the `fastq_1` and `fastq_2` fields: this skill's file leaves out `"format": "file-path"` and `"exists": true`. With `format: file-path`, nf-schema turns a relative path into an absolute path under the launch folder, not under `projectDir`, and `exists: true` then fails unless the pipeline is launched from the repo root. Without them the paths stay text, and the workflow resolves relative paths against `projectDir` (see the client skill's samplesheet wiring). nf-schema skips the `exists` check for `s3://` and `gs://` paths in any case.

TODO comments. Change `// TODO nf-core:` to `// TODO:` in `conf/base.config` and in the other generated files.

Keep these, because they are functional dependencies on nf-core, not branding:

- `subworkflows/nf-core/` (vendored nf-core subworkflows) and `modules/nf-core/` (vendored modules, once installed)
- the `utils_nfcore_[project-name]_pipeline` subworkflow name and its `../../nf-core/` imports
- the `nf-core` package pin in the environment yml

Verify: search the repo for `github.com/[org]/` and `TODO nf-core`, and run `nextflow lint` on `main.nf` and `workflows/`.

## pipeline.yml skip_features

Every pipeline's `pipeline.yml` uses this exact `skip_features` list. Only `name`, `org`, `description`, and `author` vary: `org` and `author` are the `.nf-core.yml` `template.org` and `author` rows of the Nextflow table in the client `CLAUDE.md`. Setting `org` keeps the nf-core name out of the generated files.

```yaml
name: [project-name]
org: [org]
description: [pipeline-description]
author: [author]
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

## Placeholders for Nextflow files

The files in `assets/` use these placeholders, in addition to `[project-name]` and `[project_name]` (see `project-setup`). Fill them from the Nextflow table in the client `CLAUDE.md`. If a row says "not recorded", ask the user.

- `[manifest-name]` — the `manifest.name` row.

- `[org]` — the `.nf-core.yml` `template.org` row.

- `[author]` — the `author` row.

- `[github-url]` — the GitHub hosting row, with `[project-name]` filled in.

- `[github-owner]` — the owner part of `[github-url]` (for example `trophicnexus` in `https://github.com/trophicnexus/[project-name]`).

- `[pipeline-description]` — one sentence, from the user.

The cloud placeholders (`[gcp-...]`, `[aws-...]`) are defined in `gcp.md` and `aws.md`, and filled from the cloud table in the client `CLAUDE.md`.

## Environment yml

Create `conf/[project-name].yml` from `project-setup/assets/environment.yml`. Every Nextflow pipeline has these dependencies, in alphabetical order with the cloud tools and any extra tools:

- `nextflow=25.10.4`
- `nf-core=4.0.0`
- `python=3.12`

Add the cloud tools: `google-cloud-sdk` for GCP, `awscli` and `boto3` for AWS. Add `nf-test=0.9.5` when the pipeline has the development tooling. The `project-setup` rules apply: only the primary tool (`nextflow`) is pinned when the file is created, and the other versions listed here are written in once the environment resolves.

## Development tooling

A pipeline has this tooling when the user says so. This is chosen per pipeline, not per client. A pipeline is a clean single-pipeline repository: do not add stash logic, a `.lintignore`, or exclusion globs.

Copy the files, and replace `[project-name]` (the environment name in `scripts/`), `[org]`, and the other placeholders:

| Asset in this skill | Destination in the pipeline |
| ------------------- | --------------------------- |
| `assets/dev-tooling/scripts/` | `scripts/` |
| `assets/dev-tooling/githooks/pre-commit` | `.githooks/pre-commit` |
| `assets/dev-tooling/nf-test.config` | `nf-test.config` |
| `assets/dev-tooling/tests/` | `tests/` |
| `assets/dev-tooling/nf-core.yml` | `.nf-core.yml` (replaces the generated file) |
| `assets/starter/test.config` | `conf/test.config` |
| `assets/starter/samplesheet_test_local.csv` | `assets/samplesheet_test_local.csv` |
| `assets/starter/multiqc_config.yml` | `assets/multiqc_config.yml` |

Then:

1. Make the scripts and the hook executable, and run `./scripts/setup-githooks.sh`.

2. Edit `tests/default_local.nf.test` and `conf/test.config` so they mirror the production local `nextflow run` command: the params, the assertions, and the input paths. The test file ships with an example `reference_database` param that most pipelines replace.

3. Generate the first snapshot with `nf-test test tests/default_local.nf.test --profile +local -c nf-test.config --update-snapshot`.

4. Commit small test FASTQs under `assets/fastq/`, or write down in the README how developers get them. `assets/samplesheet_test_local.csv` paths are relative to `projectDir`.

5. Add pipeline-specific MultiQC sections to `report_section_order` in `assets/multiqc_config.yml` as modules are wired. Delete the file if the pipeline does not run MultiQC.

6. Pin the container digests in `conf/containers_*.config` when nf-core modules are installed (see `containers.md`).

7. Add one row to the lint table in the README for every flag in `.nf-core.yml` (see the `readme` skill).

For a pipeline on GCP, also follow "Development Guidelines" and "Testing" in `gcp.md`, which add the cloud workflow, the cloud samplesheet, and extra lint flags.

### A pipeline without the development tooling

Skip the copying above: do not copy `assets/dev-tooling/`, `conf/test.config`, or the test samplesheets, and do not create `.nf-core.yml` unless the user asks. Leave `nf-test` out of the environment yml, and delete the `test` profile from `nextflow.config`. Test the pipeline by hand (see "Testing without the development tooling" in `references/coding.md`). Change the README as follows:

- Delete the nf-core lint disables table from Development Guidelines, unless the pipeline has a `.nf-core.yml`.

- In Testing, delete the Test layers, Pre-commit hook, and GitHub Actions CI subsections, and replace the local integration command by the production cloud command with an `s3://` or `gs://` output directory.

- In Repo structure, delete `nf-test.config`, `.githooks/`, `scripts/`, `tests/`, and `conf/test.config`.
