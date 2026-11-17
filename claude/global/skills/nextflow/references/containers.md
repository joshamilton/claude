# Container strategies for Nextflow pipelines

A pipeline uses one of two strategies, or combines them. Any client can use any strategy. The pipeline's own `nextflow.config` shows which one it uses. For a new pipeline, ask the user.

- Strategy A: community or Wave images, pinned per process in `conf/containers_*.config`.

- Strategy B: custom images in a cloud registry, named in `params.containers` in `conf/modules.config`.

Use A for tools that nf-core modules already provide an image for. Use B when the pipeline needs an image that no module provides. A pipeline can use A for most processes and B for the few that need a custom image.

The registry address for custom images depends on the cloud:

- AWS (ECR): `[aws-registry-path]` (see `aws.md` in this folder).

- GCP (Artifact Registry): `[gcp-registry-path]` (see `gcp.md` in this folder).

## Strategy A: pinned images

Pin the container of every process in a containers config file when you install the module. Take the full digest from the module's `meta.yml` or from `nf-core modules info`. Change `conf/modules.config` and the workflow in the same change.

Files:

- `conf/containers_docker_amd64.config` - cloud runs and local x86_64 runs.

- `conf/containers_docker_arm64.config` - local runs on Apple Silicon. Use arm64-native digests where they exist.

- `conf/containers_wave_arch_arm64.config` - included from the `local` profile on arm64 only. It sets `arch = 'arm64'` for processes that use native arm64 images. Other processes default to amd64 emulation.

Wiring in the `local` profile of `nextflow.config`. With strategy B only, the `local` profile has no `includeConfig` statements for container files, and `process.arch` is not set:

```groovy
        includeConfig (System.getProperty('os.arch') in ['aarch64', 'arm64'])
            ? 'conf/containers_docker_arm64.config'
            : 'conf/containers_docker_amd64.config'
        includeConfig (System.getProperty('os.arch') in ['aarch64', 'arm64'])
            ? 'conf/containers_wave_arch_arm64.config'
            : '/dev/null'
```

The cloud batch profile always includes `conf/containers_docker_amd64.config`. Add this line as the first line of the profile in `nextflow.config`: the `batch` profile on AWS, or the `googlebatch` profile on GCP.

```groovy
        includeConfig 'conf/containers_docker_amd64.config'
```

A custom image in this strategy is named by its full registry address in the containers config file.

### Templates

Add one `withName` line per process when modules are installed. The digests below are examples.

`conf/containers_docker_amd64.config`:

```groovy
/*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Docker containers for amd64 (cloud and local x86_64)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
*/

process { withName: 'FASTQC_INIT' { container = 'community.wave.seqera.io/library/fastqc:0.12.1--5cb1a2fa2f18c7c2' } }
process { withName: 'MULTIQC'     { container = 'community.wave.seqera.io/library/multiqc:1.34--db7c73dae76bc9e6' } }
```

`conf/containers_docker_arm64.config`:

```groovy
/*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Docker containers for arm64 (Apple Silicon local)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
*/

process { withName: 'FASTQC_INIT' { container = 'community.wave.seqera.io/library/fastqc:0.12.1--e455e32f745abe68' } }
process { withName: 'MULTIQC'     { container = 'community.wave.seqera.io/library/multiqc:1.34--d167b8012595a136' } }
```

`conf/containers_wave_arch_arm64.config`:

```groovy
/*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Native arm64 CPU arch for nf-core modules with Wave containers (Apple Silicon local)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
*/

process {
    withName: 'FASTQC_INIT' {
        arch = 'arm64'
    }
    withName: 'MULTIQC' {
        arch = 'arm64'
    }
}
```

## Strategy B: custom images in a registry

Define the registry path and the image names once, in `params` in `conf/modules.config`. Then point each process at its image.

```groovy
/*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Config file for defining DSL2 per module options and publishing paths
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
*/

params {
    registry_path = "[registry-path]"
    containers {
        custom_process = "${registry_path}/pipeline-name/container-name:1.0.0"
        another_process = "${registry_path}/pipeline-name/another-container:1.0.0"
    }
}

process {
    withName: 'CUSTOM_PROCESS' {
        container = params.containers.custom_process
    }
}
```

In the config, `[registry-path]` is built from the same parameters as the placeholders in `aws.md` and `gcp.md`:

- AWS: `${params.aws_account_id}.dkr.ecr.${params.aws_region}.amazonaws.com/[aws-repository]` (`[aws-registry-path]`)

- GCP: `${params.gcp_location}-docker.pkg.dev/${params.gcp_project}/[gcp-repository]` (`[gcp-registry-path]`)

Build and push the images with `docker/build.sh`. Copy it from `assets/build.sh` in the `nextflow` skill, replace `[project-name]`, and make it executable. The same script serves both clouds. Add one `build_and_push` line per image at the end. The script:

- logs in to the registry

- builds the image, and pushes it to `<registry>/<repo>/<image>:<tag>`

- builds for the platforms in `--platform` when it is given (for example `linux/amd64,linux/arm64` for local runs on Apple Silicon), using `docker buildx`

Give the script the registry values as command-line options, never as fixed text in the file:

- `--cloud aws` or `--cloud gcp`, always required.

- AWS: `--aws-profile`, `--aws-account-id`, and `--aws-region`. The script logs in with `aws ecr get-login-password`.

- GCP: `--gcp-project` and `--gcp-region`. The script logs in with `gcloud auth configure-docker [gcp-region]-docker.pkg.dev`.

- Both: `--repo` (the repository name, default `[project-name]`) and `--platform` (optional).

## README text

For the Docker Containers subsection of Deployment. Use the version for the pipeline's strategy. If the pipeline combines both, use both paragraphs.

Strategy A:

```text
The pipeline uses community and Wave Docker images for the nf-core tools, pinned in `conf/containers_*.config`.

Optional custom images: build multi-platform (`linux/amd64`, `linux/arm64`) images with `docker/build.sh` and push them to [registry name]. Refer to a custom image in `conf/containers_*.config` by its full registry address.
```

```bash
git clone [repository URL]
cd [project-name]
chmod +x docker/build.sh
# ./docker/build.sh --cloud [aws|gcp] [cloud flags] --platform linux/amd64,linux/arm64
```

Strategy B:

```text
The pipeline uses Docker images stored in [registry name]. To build and deploy the images:
```

On AWS (ECR):

```bash
# Clone the repo
git clone [repository URL]
cd [project-name]

# Make the build script executable
chmod +x docker/build.sh

# Build and push the images
./docker/build.sh \
    --cloud aws \
    --aws-profile [aws-profile] \
    --aws-account-id [aws-account-id] \
    --aws-region [aws-region] \
    --repo [aws-repository]
```

On GCP (Artifact Registry):

```bash
# Clone the repo
git clone [repository URL]
cd [project-name]

# Make the build script executable
chmod +x docker/build.sh

# Build and push the images
./docker/build.sh \
    --cloud gcp \
    --gcp-project [gcp-project] \
    --gcp-region [gcp-region] \
    --repo [gcp-repository]
```
