# Shared Nextflow coding guidelines

Conventions shared by every Nextflow pipeline. Each client's own `<client>-nextflow` skill's `references/coding.md` builds on this: it gives the concrete `nextflow.config` (profiles, cloud params), the container strategy, and the testing approach, while following the shared structure below.

## nextflow.config section order

Every pipeline's `nextflow.config` follows this section order:

manifest --> plugins --> params --> validation --> includeConfig --> profiles --> container registry (`docker.registry`) --> env --> process.shell --> nextflow settings --> timeline/report/trace/dag

## Samplesheet parameter

Name the samplesheet parameter `input` (`params.input`, `--input` on the command line), as nf-core pipelines do.

## Container registry

Set only `docker.registry = 'quay.io'`. Do not set registries for other container technologies unless a pipeline actually uses them.

## conf/base.config resource conventions

Do not define default `cpus`, `memory`, or `time` at the top process level: only error handling. Use label-based blocks for resources, and `maxRetries = 3` (not 1) at the top level:

```groovy
process {
    errorStrategy = { task.exitStatus in ((130..145) + 104) ? 'retry' : 'finish' }
    maxRetries    = 3
    maxErrors     = '-1'

    withLabel:process_single {
        cpus   = { 1                   }
        memory = { 6.GB * task.attempt }
        time   = { 4.h  * task.attempt }
    }
    withLabel:process_low {
        cpus   = { 2     * task.attempt }
        memory = { 12.GB * task.attempt }
        time   = { 4.h   * task.attempt }
    }
    withLabel:process_medium {
        cpus   = { 6     * task.attempt }
        memory = { 36.GB * task.attempt }
        time   = { 8.h   * task.attempt }
    }

    // Process-specific overrides
    // withName: 'HEAVY_PROCESS' {
    //     cpus = { 32 * task.attempt }
    //     maxRetries = 1
    // }
}
```

Add `process_high`, `process_long`, `process_high_memory`, `error_ignore`, and `error_retry` label blocks as pipelines need them, following the same `task.attempt`-scaled pattern. Use `withName` overrides for a process's individual resource requirements or cloud queue assignment: see the client's own `references/coding.md` for cloud-specific queue params.

## conf/modules.config publishDir pattern

Number `publishDir` paths to match pipeline steps (`01_`, `02_`, ..., `99_MULTIQC/`). Use `saveAs` when published filenames must differ from module defaults. Use `withName` sections for per-process `publishDir`, `ext.args`, and container assignment:

- see `containers.md` in this folder for the two container strategies (Wave-pinned config vs. ECR `params.containers`)
- see the client's own `references/coding.md` for which strategy that client uses

## Adding a module

Combine these in one change when adding a module:

- Install it: `nf-core modules install <module>` (or add `modules/local/` for a custom one).
- Wire it into the workflow file: import, alias if the same tool runs more than once, connect channels, add its outputs to `ch_multiqc_files` if it reports to MultiQC.
- Configure it in `conf/modules.config`: `publishDir`, `ext.args`, container assignment.
- Configure resources in `conf/base.config` if the defaults are insufficient.
- Add any new required params to `nextflow.config` and its `validation.defaultIgnoreParams` if appropriate.
- Test it: see the client's own `references/coding.md` for that client's testing approach.
