---
name: nextflow
description: Use when initializing, writing, or extending any Nextflow pipeline. Covers the conventions shared by every Nextflow pipeline, which are initialized from the nf-core template. This skill covers nf-core template integration, how to remove nf-core branding, the nextflow.config template, resource and publishDir conventions in conf/, container strategies, AWS and GCP settings, and the development tooling (lint, nf-test, pre-commit hook).
---

# Shared Nextflow conventions

Follow these steps in order. Skip a step that does not apply.

## Procedure

1. Read the client's `<client>-nextflow` skill, if it has one. It holds only facts that belong to that client alone. Where it differs from this skill, follow the client skill.

2. Decide the task. For a new pipeline, continue with step 3. For an existing pipeline, go to step 9.

3. Initialize the pipeline. Read `references/setup.md` and follow its nf-core template integration workflow.

4. Write `nextflow.config` from `assets/nextflow.config`. Fill in the placeholders listed in "Placeholders for Nextflow files" in `references/setup.md`.

5. Add the cloud settings. Read `references/aws.md` or `references/gcp.md`. Paste the blocks under "Pipeline settings" into `nextflow.config` and `conf/base.config`. Fill the placeholders from the cloud table in the client `CLAUDE.md`.

6. Add the container configuration. Read `references/containers.md` and set up the pipeline's strategy. The strategy is chosen per pipeline, not per client, so ask the user if the pipeline does not already show it. For custom images, copy `assets/build.sh` to `docker/build.sh`.

7. Decide with the user whether this pipeline has the development tooling. Whether it does is chosen per pipeline, not per client. An existing pipeline has it if `scripts/lint.sh` exists. If it has it, follow "Development tooling" in `references/setup.md`. It copies the files in `assets/dev-tooling/` and `assets/starter/` into the pipeline.

8. Create the README with the `readme` skill and its Nextflow template. The template takes its cloud and container sections from the files in steps 5 and 6.

9. Write or extend pipeline code. Read `references/coding.md` and follow the `conf/base.config` conventions and the `conf/modules.config` pattern. When adding a module, follow "Adding a module" in that file.

10. Run the lint and test checks that the pipeline has (`scripts/lint.sh` and `scripts/test.sh` when the development tooling is in place, otherwise the manual test in "Testing without the development tooling" in `references/coding.md`). Fix what they report before you report the work as done.

## Reference files

- `references/setup.md` — nf-core template integration, branding removal, `pipeline.yml`, the placeholders for Nextflow files, the environment yml, directory structure, development tooling.

- `references/coding.md` — `nextflow.config` section order, container registry setting, `conf/base.config` resources, `conf/modules.config` pattern, adding a module.

- `references/aws.md` — pipelines on AWS Batch.

- `references/gcp.md` — pipelines on Google Batch.

- `references/containers.md` — the two container strategies and their config templates.

## Asset files

- `assets/nextflow.config` — the `nextflow.config` template.

- `assets/build.sh` — the `docker/build.sh` template for custom images, for AWS and GCP.

- `assets/dev-tooling/` — the lint and test scripts, the pre-commit hook, `nf-test.config`, the `tests/` files, and `.nf-core.yml`.

- `assets/starter/` — `schema_input.json` (every pipeline), and the test samplesheets, `multiqc_config.yml`, and `conf/test.config` (development tooling).

- `assets/gcp-integration-test.yml` — the GitHub Actions workflow for a pipeline on GCP.
