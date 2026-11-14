---
name: nextflow
description: Use when initializing, writing, or extending any Nextflow pipeline. Covers the conventions shared across every Nextflow pipeline, which are initialized from nf-core. This skill covers nf-core template integration, how to remove nf-core branding, the pipeline.yml skip_features list, nextflow.config section order, conf/base.config resource conventions, and the conf/modules.config publishDir pattern.
---

# Shared Nextflow conventions

Follow these steps in order. Skip a step that does not apply.

## Procedure

1. Read the client's `<client>-nextflow` skill. It states the client's cloud (AWS or GCP) and container strategy. If it does not, ask the user. Where it differs from this skill, follow the client skill.

2. Decide the task. For a new pipeline, continue with step 3. For an existing pipeline, go to step 7.

3. Initialize the pipeline. Read `references/setup.md` and follow its nf-core template integration workflow.

4. Add the cloud settings. Read `references/aws.md` or `references/gcp.md`. Paste the blocks under "Pipeline settings" into `nextflow.config` and `conf/base.config`. Fill the placeholders from the identity table in the client `CLAUDE.md`.

5. Add the container configuration. Read `references/containers.md` and set up the client's strategy. For custom images, copy `assets/build.sh` to `docker/build.sh`.

6. Create the README with the `readme` skill and its Nextflow template. The template takes its cloud and container sections from the files in steps 4 and 5.

7. Write or extend pipeline code. Read `references/coding.md` and follow the `nextflow.config` section order, the `conf/base.config` conventions, and the `conf/modules.config` pattern. When adding a module, follow "Adding a module" in that file.

8. Run the lint and test checks that the client skill names. Fix what they report before you report the work as done.

## Reference files

- `references/setup.md` — nf-core template integration, branding removal, `pipeline.yml`, directory structure.

- `references/coding.md` — `nextflow.config` section order, container registry setting, `conf/base.config` resources, `conf/modules.config` pattern, adding a module.

- `references/aws.md` — pipelines on AWS Batch.

- `references/gcp.md` — pipelines on Google Batch.

- `references/containers.md` — the two container strategies and their config templates.

- `assets/build.sh` — the `docker/build.sh` template for custom images, for AWS and GCP.
