# Shared Nextflow coding guidelines

Conventions shared by every Nextflow pipeline. A client's own `<client>-nextflow` skill, if it has one, holds only facts that belong to that client alone.

## nextflow.config section order

Every pipeline's `nextflow.config` follows this section order:

manifest --> plugins --> params --> validation --> includeConfig --> profiles --> container registry (`docker.registry`) --> env --> process.shell --> nextflow settings --> timeline/report/trace/dag

## Samplesheet parameter

Name the samplesheet parameter `input` (`params.input`, `--input` on the command line), as nf-core pipelines do.

## Container registry

Set only `docker.registry = 'quay.io'`. Do not set registries for other container technologies unless a pipeline actually uses them.

## conf/base.config resource conventions

nf-core writes `conf/base.config` with the resource labels pipelines use (`process_single`, `process_low`, `process_medium`, `process_high`, `process_long`, `process_high_memory`, `error_ignore`, `error_retry`). Keep those labels, and make these changes at the top of the `process` block:

- Delete the default `cpus`, `memory`, and `time`. The top level holds only error handling, and resources come from the labels.

- Set `maxRetries = 3` (not 1).

- Set `errorStrategy = { task.exitStatus in ((130..145) + 104) ? 'retry' : 'finish' }`, without the `175..177` exit codes that nf-core adds.

- Delete the `process_gpu` label. nf-core writes it even when `gpu` is skipped.

Use `withName` overrides for a process's individual resource requirements or cloud queue assignment: the queue settings and an example are in "Pipeline settings" in `aws.md`.

## nextflow.config

Start from `assets/nextflow.config` (see step 4 of the procedure in `SKILL.md`). Add each new pipeline-specific param to both `params` and `validation.defaultIgnoreParams`, unless it should appear in `nextflow_schema.json`.

Profiles: use `local`, the cloud profile (`batch` on AWS, `googlebatch` on GCP), `test` if the pipeline has the development tooling, and `seqera` if it runs on Seqera Platform. Do not add generic container or environment profiles (conda, mamba, docker, singularity, podman, shifter, charliecloud, apptainer, wave, gitpod, debug, arm) unless the user asks. Paste the cloud profile and params from "Pipeline settings" in `aws.md` or `gcp.md`, and the container wiring from `containers.md`.

## conf/modules.config publishDir pattern

Number `publishDir` paths to match pipeline steps (`01_`, `02_`, ..., `99_MULTIQC/`). Use `saveAs` when published filenames must differ from module defaults. Use `withName` sections for per-process `publishDir`, `ext.args`, and container assignment:

- the container strategy is chosen per pipeline (pinned images in a containers config, or custom images in `params.containers`): see `containers.md` in this folder

A pipeline that runs MultiQC has this block:

```groovy
    withName: 'MULTIQC' {
        ext.args   = { params.multiqc_title ? "--title \"$params.multiqc_title\"" : '' }
        publishDir = [
            path: { "${params.outdir}/99_MULTIQC/" },
            mode: params.publish_dir_mode,
            saveAs: { filename -> filename.equals('versions.yml') ? null : filename },
        ]
    }
```

### Renaming published files

Use `saveAs` to give published files names that are meaningful to the user. nf-core modules name paired FastQC outputs `_1_fastqc` and `_2_fastqc`. This example, for the initial FastQC step, renames them to `{sample}_R1_fastqc` and `{sample}_R2_fastqc`. A pipeline can build the new name from another value, for example the original FASTQ file name (`meta.fastq_pe1.replaceAll(/\.fastq\.gz$/, '_fastqc.html')` for `_1_fastqc.html`):

```groovy
/*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Config file for defining DSL2 per module options and publishing paths
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
*/

process {

    //
    // STEP 1: Initial FastQC on raw reads
    // Published names: {sample}_R1_fastqc.{html,zip}, {sample}_R2_fastqc.{html,zip}
    //
    withName: 'FASTQC_INIT' {
        ext.args   = '--quiet'
        ext.prefix = { "${meta.id}" }
        publishDir = [
            [
                path: { "${params.outdir}/01_FASTQC/" },
                pattern: '*.html',
                saveAs: { filename ->
                    if (filename.endsWith('_1_fastqc.html')) {
                        return "${meta.id}_R1_fastqc.html"
                    }
                    if (filename.endsWith('_2_fastqc.html')) {
                        return "${meta.id}_R2_fastqc.html"
                    }
                    return filename
                },
                mode: params.publish_dir_mode,
            ],
            [
                path: { "${params.outdir}/01_FASTQC/" },
                pattern: '*.zip',
                saveAs: { filename ->
                    if (filename.endsWith('_1_fastqc.zip')) {
                        return "${meta.id}_R1_fastqc.zip"
                    }
                    if (filename.endsWith('_2_fastqc.zip')) {
                        return "${meta.id}_R2_fastqc.zip"
                    }
                    return filename
                },
                mode: params.publish_dir_mode,
            ],
        ]
    }

}
```

## Workflow wiring

Workflow and DSL2 names: uppercase `[project_name]` (for example folder `nf-my-pipeline` gives the workflow `MY_PIPELINE`, and the outer workflow `NF_MY_PIPELINE`).

### `workflows/[project_name].nf`

- File name uses underscores (`[project_name]`).

- Workflow name uses underscores (e.g. `NF_MY_PIPELINE`).

- Alias modules when the same tool runs more than once.

- Collect MultiQC inputs in `ch_multiqc_files` as modules are added.

- Default MultiQC config: `file("${projectDir}/assets/multiqc_config.yml", checkIfExists: true)`.

- Write software versions to `${outdir}/logs/${params.trace_report_suffix}/`.

```groovy
include { FASTQC as FASTQC_INIT  } from '../modules/nf-core/fastqc/main'
include { MULTIQC                } from '../modules/nf-core/multiqc/main'
include { softwareVersionsToYAML } from '../subworkflows/nf-core/utils_nfcore_pipeline'

workflow NF_MY_PIPELINE {

    take:
    ch_samplesheet
    multiqc_config
    multiqc_logo
    outdir

    main:

    def ch_versions = channel.empty()
    def ch_multiqc_files = channel.empty()

    FASTQC_INIT(ch_samplesheet)
    ch_multiqc_files = ch_multiqc_files.mix(FASTQC_INIT.out.zip.map { _meta, zip -> zip })

    // Collate versions (topic-based pattern from nf-core template)
    def topic_versions = channel.topic("versions")
        .distinct()
        .branch { entry ->
            versions_file: entry instanceof Path
            versions_tuple: true
        }

    def topic_versions_string = topic_versions.versions_tuple
        .map { process, tool, version ->
            [ process[process.lastIndexOf(':')+1..-1], "  ${tool}: ${version}" ]
        }
        .groupTuple(by:0)
        .map { process, tool_versions ->
            tool_versions.unique().sort()
            "${process}:\n${tool_versions.join('\n')}"
        }

    def ch_collated_versions = softwareVersionsToYAML(ch_versions.mix(topic_versions.versions_file))
        .mix(topic_versions_string)
        .collectFile(
            storeDir: "${outdir}/logs/${params.trace_report_suffix}",
            name:  '[project-name]_software_mqc_versions.yml',
            sort: true,
            newLine: true
        )

    ch_multiqc_files = ch_multiqc_files.mix(ch_collated_versions)
    MULTIQC(
        ch_multiqc_files.flatten().collect().map { files ->
            [
                [id: '[project-name]'],
                files,
                multiqc_config
                    ? file(multiqc_config, checkIfExists: true)
                    : file("${projectDir}/assets/multiqc_config.yml", checkIfExists: true),
                multiqc_logo ? file(multiqc_logo, checkIfExists: true) : [],
                [],
                [],
            ]
        }
    )

    emit:
    multiqc_report = MULTIQC.out.report.map { _meta, report -> [report] }.toList()
    versions       = ch_versions
}
```

### `main.nf`

- Name the outer workflow `NF_[PROJECT_NAME]` (see step 6 of the integration workflow in `setup.md`).

- `include` workflow from `./workflows/[project_name]` (underscores).

- Pass `params` through to init subworkflow and main workflow.

```groovy
include { NF_MY_PIPELINE } from './workflows/[project_name]'
include { PIPELINE_INITIALISATION } from './subworkflows/local/utils_nfcore_[project-name]_pipeline'

workflow {
    PIPELINE_INITIALISATION(
        params.version,
        params.validate_params,
        params.monochrome_logs,
        workflow.commandLine,
        params.outdir,
        params.input,
        // add pipeline-specific params here
        params.help,
        params.help_full,
        params.show_hidden,
    )

    NF_MY_PIPELINE(
        PIPELINE_INITIALISATION.out.samplesheet,
        params.multiqc_config,
        params.multiqc_logo,
        params.outdir,
    )
}
```

### `subworkflows/local/utils_nfcore_[project-name]_pipeline/main.nf`

Extend the nf-core init subworkflow:

1. Add pipeline-specific params to `PIPELINE_INITIALISATION` `take:` block.

2. Call validation functions after `UTILS_NFCORE_PIPELINE`.

3. Use `resolveInputPath()` for relative FASTQ paths in samplesheet channel construction.

4. Add `validateInputSamplesheet()` and any database validators.

`resolveInputPath()` (required for nf-test local runs):

```groovy
def resolveInputPath(path) {
    def normalized = normalizePathString(path)
    if (!normalized) {
        return normalized
    }
    if (normalized.startsWith('gs://') || normalized.startsWith('s3://') || normalized.startsWith('/')) {
        return normalized
    }
    if (normalized ==~ /^[A-Za-z]:[\\\/].*/) {
        return normalized
    }
    return "${projectDir}/${normalized}"
}
```

Samplesheet channel pattern (paired-end). `normalizePathString()` and `validateGroupedSamplesheet()` are helpers that each pipeline writes for itself. Keep the `fastq_2` check only if the pipeline needs paired-end reads, because the samplesheet schema does not require `fastq_2`:

```groovy
channel
    .fromList(samplesheetToList(input, "${projectDir}/assets/schema_input.json"))
    .map { meta, fastq_1, fastq_2 ->
        if (!fastq_2) {
            error("Samplesheet row for sample '${meta.id}' is missing fastq_2 (paired-end reads required)")
        }
        def fq1 = resolveInputPath(fastq_1)
        def fq2 = resolveInputPath(fastq_2)
        return [
            meta.id,
            meta + [ single_end: false, fastq_1: fq1, fastq_2: fq2 ],
            [ file(fq1), file(fq2) ],
        ]
    }
    .groupTuple()
    .map { samplesheet -> validateGroupedSamplesheet(samplesheet) }
    .map { meta, fastqs -> [ meta, fastqs.flatten() ] }
    .set { ch_samplesheet }
```

## Adding a module

Combine these in one change when adding a module:

- Install it: `nf-core modules install <module>` (or add `modules/local/` for a custom one).

- Wire it into the workflow file: import, alias if the same tool runs more than once, connect channels, add its outputs to `ch_multiqc_files` if it reports to MultiQC.

- Configure it in `conf/modules.config`: `publishDir`, `ext.args`, container assignment.

- Configure resources in `conf/base.config` if the defaults are insufficient.

- Add any new required params to `nextflow.config` and its `validation.defaultIgnoreParams` if appropriate.

- Test it: for a pipeline with the development tooling, also pin its container in `conf/containers_*.config` (strategy A), add its params to `conf/test.config` and to the cloud workflow, add a section to `assets/multiqc_config.yml` if it reports to MultiQC, and update the assertions and the snapshot in `tests/default_local.nf.test`. For a pipeline without it, test as described in "Testing without the development tooling" below.

## Testing without the development tooling

A pipeline without the development tooling has no nf-test and no pre-commit hooks. Test it by hand, end to end, after each new module:

- Test the entire pipeline with all required parameters, not individual modules, after each module is implemented (including its publishing configuration).

- Use a cloud output directory only (`s3://` or `gs://`). Do not test with local directories.

- Use the exact test command from the README's Testing section. Do not invent custom test commands.
