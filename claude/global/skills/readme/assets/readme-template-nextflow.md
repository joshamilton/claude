# [project-name]

[Contact block: see this client's CLAUDE.md]

[How to use this template: every line in square brackets is a placeholder. A bracketed line that begins with "Cloud:" names a section to copy from the cloud file for this project's cloud, `aws.md` or `gcp.md`, in `nextflow/references/`. Replace each placeholder, and delete this paragraph.]

## Overview

[What the pipeline does, and for whom. Keep it short.]

Key features:

- [Feature, one line]

Processing overview:

1. [Module name: what it does]
2. [Module name: what it does]

## Installation

### Setup mamba

```bash
curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
bash Miniforge3-$(uname)-$(uname -m).sh
```

[Other prerequisites, if any]

### Install the pipeline and create the environment

```bash
git clone [repository URL]
cd [project-name]
mamba env create -f conf/[project-name].yml
mamba activate [project-name]
./scripts/setup-githooks.sh
```

[Cloud: the "Installation" section of the cloud file (credentials, test assets, the cloud head node).]

## Usage

Inputs:

- [Samplesheet: path and one line on what it holds. The full column list is under Detailed command-line usage.]
- [Other inputs, as a compact list]

Main parameters:

- `--input` — [Path to the samplesheet CSV.]
- `--outdir` — [Output directory.]
- `--[flag]` — [Default, if any, and one short phrase.]

Steps:

1. [User action]
2. [User action, ending with the copy-paste command]

Minimal example (local run):

```bash
nextflow run main.nf \
    -profile local \
    --input assets/samplesheet.csv \
    --outdir results
```

Explicit form (same defaults as above, all paths and tunables shown):

```bash
nextflow run main.nf \
    -profile local \
    -work-dir /path/to/scratch \
    --input assets/samplesheet.csv \
    --outdir results \
    [every other option that takes a value]
```

[Cloud: the "Usage" section of the cloud file (the production run and the local run that reads cloud data).]

## Results

Pipeline outputs are organized in the following directory structure:

```text
outdir/
├── [NN_STEP_NAME]/           # [description]
├── [NN_STEP_NAME]/           # [description]
└── logs/<timestamp>/         # Run diagnostics (params, trace, timeline, software versions)
```

Key output files:

| Path | Description |
| ---- | ----------- |
| `[path/under/outdir]` | [what it contains] |

## Detailed Usage

### Inputs

The pipeline requires the following inputs:

1. Samplesheet: a CSV file with sample metadata and file paths. It has these columns:
   - `sample` (required): Unique sample identifier.
   - `fastq_1` (required): Path to forward (R1) reads in gzipped FASTQ format. A local path or a cloud path (for example `[cloud path to a FASTQ file]`).
   - `fastq_2` (optional): Path to reverse (R2) reads in gzipped FASTQ format. A local path or a cloud path.
   - [Any other columns: `column` ([required or optional]): description.]
2. [Reference files, databases, or other required inputs. Give the parameter name, the format, and the validation rules.]

At startup, the pipeline checks the inputs before any process runs:

- The header must include the required columns.
- Each row must have a value in every required column.
- `sample` identifiers must be unique across the file.
- [Any other rule.]

### Parameters

[Parameter-by-parameter explanations. Use the list pattern for command-line options.]

## Deployment

### Prerequisites

For deploying and running the pipeline, you need:

- Docker Desktop installed. See the [Docker installation guide](https://docs.docker.com/desktop/).
- GitHub access.
- [Cloud: the access prerequisite from the "Deployment" section of the cloud file.]

### Docker Containers

[The Docker Containers text for this project's container strategy, from the "README text" section of `nextflow/references/containers.md`.]

### Cloud resources

[Cloud: the cloud resources list from the "Deployment" section of the cloud file.]

### Pipeline assets and external resources

[Pipeline assets and external databases or reference files that must exist in cloud storage before a production run. Delete this subsection if there are none.]

## Development Guidelines

### nf-core lint disables

`.nf-core.yml` sets which [nf-core pipelines lint](https://nf-co.re/docs/nf-core-tools/cli/pipelines/lint) tests run. Disabled tests are listed below with the check they skip and the reason. Keep one row for every flag in the pipeline's `.nf-core.yml`, and delete the rows for flags the pipeline does not set.

| Flag | nf-core check | Why disabled |
| ---- | ------------- | ------------ |
| `actions_ci: false` | GitHub workflow for nf-core pipelines lint | Lint runs in pre-commit, not on GitHub CI |
| `actions_nf_test: false` | GitHub workflow for nf-test | nf-test runs in pre-commit, not on GitHub CI |
| `nf_test_content: false` | nf-core conventions | Custom layout: path-gated nf-core tests, explicit nf-test paths, no template testdata base paths |
| `readme: false` | README badges and Zenodo DOI placeholders | Custom README |
| `pipeline_name_conventions: false` | pipeline name follows nf-core naming rules | Client pipeline, not an nf-core community pipeline |
| `rocrate_readme_sync: false` | RO-Crate metadata | No RO-Crate metadata file |
| `files_exist: false` | required template files present | Minimal layout with many template paths intentionally omitted |
| `files_unchanged: false` | template files unmodified from `nf-core pipelines create` output | Workflows and assets deliberately customized |
| `schema_params: false` | every flat param from `nextflow config` appears in `nextflow_schema.json` | Params typed in workflow config; not all visible to `nextflow config` |
| `nextflow_config: false` | required config keys in `nextflow.config` only | No nf-core `custom_config_base` |
| `container_configs: false` | container config layout | Custom `conf/containers_*.config` layout |
| `multiqc_config.report_comment` | HTML links to nf-core GitHub and docs URLs | `report_comment` links to the pipeline's own GitHub repository |
| `multiqc_config.show_analysis_paths` | MultiQC config option | Disabled in report output by design |
| `multiqc_config.show_analysis_time` | MultiQC config option | Disabled in report output by design |
| `multiqc_config.report_section_order` | MultiQC config option | Custom section order in `assets/multiqc_config.yml` |

[Cloud: any lint rows from the "Development Guidelines" section of the cloud file.]

[Client: any rows and subsections that the client skill adds.]

## Testing

### Test layers

| Layer | What it tests | When it runs |
| ----- | ------------- | ------------ |
| nf-core components | nf-core module/subworkflow tests | Pre-commit when staged nf-core paths change; skipped otherwise |
| Local components | Local modules and subworkflows | Pre-commit always (`modules/local/`, `subworkflows/local/`; no-op when no tests exist) |
| Pipeline integration (local) | Production local run (see below) | Pre-commit always via `tests/default_local.nf.test` |

[Cloud: the cloud integration row from the "Testing" section of the cloud file, if there is one.]

### Pre-commit hook

Install hooks once with `./scripts/setup-githooks.sh`. Each commit runs, in order:

1. `scripts/lint.sh` — `nextflow lint` (allowlisted paths), `nf-core pipelines lint`, local module/subworkflow lint
2. `scripts/test.sh`:
   - nf-core component tests — only when staged files change under `modules/nf-core/` or `subworkflows/nf-core/` (scoped to changed components)
   - local module tests — `modules/local/`
   - local subworkflow tests — `subworkflows/local/`
   - pipeline integration — `tests/default_local.nf.test` with `--profile +local`

Run the same checks manually:

```bash
./scripts/lint.sh
./scripts/test.sh
```

### GitHub Actions CI

[Cloud: the "GitHub Actions CI" section of the cloud file. Delete this subsection if the cloud file has none.]

### Integration test commands

Integration tests mirror the production `nextflow run` commands. The local integration test uses a local `--outdir`.

1. Local pipeline integration (nf-test)

```bash
nextflow run main.nf \
    -profile local \
    --outdir <OUTDIR> \
    --input assets/samplesheet_test_local.csv \
    [additional required params]
```

`tests/default_local.nf.test` runs this command (`<OUTDIR>` is a temporary nf-test directory). Pre-commit runs `nf-test test tests/default_local.nf.test --profile +local -c nf-test.config`. The `+local` part turns on the `local` profile from `nextflow.config`, including Docker.

[Cloud: the cloud integration command from the "Testing" section of the cloud file, if there is one.]

## Repo structure

```text
[project-name]/
├── main.nf                       # Pipeline entry point
├── nextflow.config               # Core pipeline configuration
├── nextflow_schema.json          # Parameter validation schema
├── nf-test.config                # nf-test configuration
├── modules.json                  # nf-core modules tracking
├── .nf-core.yml                  # nf-core pipeline configuration
├── README.md                     # This file
├── .githooks/pre-commit          # Pre-commit hook
├── scripts/
│   ├── lint.sh                   # Lint checks
│   ├── test.sh                   # Test runner
│   └── setup-githooks.sh         # Installs the pre-commit hook
├── assets/                       # Test samplesheets and pipeline assets
│   └── samplesheet_test_local.csv
├── conf/                         # Configuration files
│   ├── base.config               # Base process resources
│   ├── modules.config            # Module-specific options and publish paths
│   ├── containers_*.config       # Pinned container images
│   ├── test.config               # Test profile
│   └── [project-name].yml        # Conda environment
├── docker/                       # Container build files (only with custom images)
├── modules/
│   ├── local/                    # Modules specific to this pipeline
│   └── nf-core/                  # Standard nf-core modules
├── subworkflows/
│   ├── local/                    # Pipeline-specific subworkflows
│   └── nf-core/                  # Standard nf-core subworkflows
├── tests/
│   ├── default_local.nf.test
│   ├── default_local.nf.test.snap
│   ├── nextflow.config
│   └── .nftignore
└── workflows/
    └── [project_name].nf         # Primary analysis workflow
```

[Cloud: any files the cloud file adds to the tree (for example a CI workflow or a cloud test samplesheet).]
