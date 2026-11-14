# Nextflow pipelines on GCP (Google Batch)

Use this file for a pipeline that runs on Google Cloud: production runs go through Google Batch with data in Google Cloud Storage, and development runs use local Docker. Every pipeline on GCP uses the same settings and README text. Only the placeholder values differ from client to client.

Two parts follow the placeholder table:

- "Pipeline settings" holds the GCP parts of `nextflow.config`.
- "README text" holds the sections that fill the bracketed lines that begin with "Cloud:" in the Nextflow README template of the `readme` skill.

## Placeholders

The values are identifiers, not credentials. They come from the identity table in the client `CLAUDE.md`. Never put a credential, key, or token in a skill or in a repository file.

Cloud values are of two kinds:

- Values that identify an account or a user (for example project, account, region, profile, queue, service account, network) default to `null` in `params`. Pass them on the command line with the parameter name.
- Pipeline-specific settings (for example machine type, disk size, spot use, retries) keep a shared default in `params`.

GCP has no job queue to choose, because Google Batch schedules the jobs, so it has no queue values. `docker/build.sh` takes `--cloud gcp`, the project, the region, and the repository as flags (see `containers.md` in this folder).

| Placeholder | Meaning |
| ----------- | ------- |
| `[gcp-project]` | GCP project ID |
| `[gcp-region]` | Region where Google Batch runs |
| `[gcp-zone]` | Zone for the head-node VM |
| `[gcp-allowed-locations]` | Allowed Batch locations, comma separated (for example `regions/<region>,zones/<region>-b`) |
| `[gcp-batch-service-account]` | Service account that runs the Batch task VMs |
| `[gcp-network]` | VPC network for the Batch task VMs (for example `global/networks/default`) |
| `[gcp-subnetwork]` | Subnetwork for the Batch task VMs (for example `regions/<region>/subnetworks/default`) |
| `[gcp-orchestrator-service-account]` | Service account attached to the head-node VM |
| `[gcp-scratch-bucket]` | Scratch bucket for work directories and test outputs, with the `gs://` prefix |
| `[gcp-output-bucket]` | Bucket for pipeline outputs, with the `gs://` prefix |
| `[gcp-reference-bucket]` | Bucket with reference data, with the `gs://` prefix |
| `[gcp-test-bucket]` | Bucket with test fixtures, with the `gs://` prefix |
| `[gcp-ci-service-account]` | Service account that GitHub Actions impersonates |
| `[gcp-wif-provider]` | Resource name of the workload identity provider |
| `[gcp-repository]` | Artifact Registry repository for custom container images (the `--repo` value of `docker/build.sh`; the project name by default) |
| `[gcp-registry-path]` | Artifact Registry address for custom container images: `[gcp-region]-docker.pkg.dev/[gcp-project]/[gcp-repository]` |

## Pipeline settings

These pieces go into `nextflow.config`. The rest of the file follows the client's template. Identity values are `null`, so no client value is written into the file.

Parameters, in the `params` block:

```groovy
    // GCP options (read by -profile googlebatch)
    gcp_project             = null
    gcp_location            = null
    gcp_service_account     = null
    gcp_network             = null
    gcp_subnetwork          = null
    gcp_use_private_address = true
    gcp_spot                = true
    gcp_boot_disk_size      = '50 GB'
    gcp_max_spot_attempts   = 3
    gcp_machine_type        = 'c2-*,c3-*,e2-*,n2-*'
    gcp_allowed_locations   = null
    gcp_batch_queue_size    = 32
```

Entries in `validation.defaultIgnoreParams`:

```groovy
        'gcp_project',
        'gcp_location',
        'gcp_service_account',
        'gcp_network',
        'gcp_subnetwork',
        'gcp_use_private_address',
        'gcp_spot',
        'gcp_boot_disk_size',
        'gcp_max_spot_attempts',
        'gcp_machine_type',
        'gcp_allowed_locations',
        'gcp_batch_queue_size',
```

The `googlebatch` profile, in the `profiles` block:

```groovy
    googlebatch {
        docker {
            enabled = true
        }
        executor {
            queueSize = params.gcp_batch_queue_size
        }
        process {
            executor       = 'google-batch'
            machineType    = params.gcp_machine_type
            resourceLabels = [
                pipeline: '[project-name]',
            ]
        }
        google {
            project            = params.gcp_project
            location           = params.gcp_location
            httpConnectTimeout = '120 sec'
            httpReadTimeout    = '120 sec'
            batch {
                bootDiskSize        = params.gcp_boot_disk_size
                usePrivateAddress   = params.gcp_use_private_address
                network             = params.gcp_network
                subnetwork          = params.gcp_subnetwork
                allowedLocations    = params.gcp_allowed_locations.split(',').collect { loc -> loc.trim() }
                spot                = params.gcp_spot
                maxSpotAttempts     = params.gcp_max_spot_attempts
                serviceAccountEmail = params.gcp_service_account
            }
        }
    }
```

The `local` profile needs no GCP block. Nextflow reads `gs://` paths through Application Default Credentials: the login from Installation on a local machine, and the VM's service account on the head node (https://docs.seqera.io/nextflow/google-storage).

The custom-image registry path for Artifact Registry is built from `gcp_project` and `gcp_location`. See `containers.md` in this folder.

The `local` and `googlebatch` profiles need no Artifact Registry block. The images are named in `conf/modules.config`.

## README text

### Installation

Paste after the local development machine commands.

Configure GCP credentials with Application Default Credentials (ADC). Nextflow uses ADC, not `gcloud auth login`, to read `gs://` paths (work directory, outputs, samplesheet FASTQs, reference databases). Sign in:

```bash
gcloud auth application-default login
gcloud config set project [gcp-project]
gcloud auth application-default print-access-token >/dev/null && echo "ADC OK"
```

Sign in to Docker for Artifact Registry, only if the pipeline has custom container images. A local run pulls the images with this login. `docker/build.sh` logs in by itself when it pushes:

```bash
gcloud auth configure-docker [gcp-region]-docker.pkg.dev
```

Sync the local test assets:

```bash
# Example: sync a reference database or test fixtures needed for local runs
mkdir -p assets/[reference-dir]
gcloud storage rsync \
  [gcp-reference-bucket]/[path-to-reference]/ \
  assets/[reference-dir]/
```

GCP head node. This is the VM that starts production runs. It uses its attached service account for credentials, not ADC from a user login.

1. Launch the head-node VM with the orchestrator service account.

    In the Google Cloud Console:

    1. Open Compute Engine, VM instances, in project `[gcp-project]`.
    2. Click Create instance.
    3. Choose an Ubuntu 24.04 LTS boot disk image, and set the name (for example `nf-head`), machine type, and other settings as needed.
    4. Expand Advanced, then Security (labeled Identity and API access in some console versions).
    5. Set the service account to `[gcp-orchestrator-service-account]`, not the default Compute Engine service account.
    6. Set the access scopes to Allow full access to all Cloud APIs.
    7. Create the instance, then connect through IAP.

    With the gcloud command line instead:

    ```bash
    gcloud compute instances create nf-head \
      --project=[gcp-project] \
      --zone=[gcp-zone] \
      --machine-type=e2-medium \
      --image-family=ubuntu-2404-lts-amd64 \
      --image-project=ubuntu-os-cloud \
      --service-account=[gcp-orchestrator-service-account] \
      --scopes=https://www.googleapis.com/auth/cloud-platform \
      --no-address
    ```

    If the VM already exists without the correct service account:

    ```bash
    gcloud compute instances set-service-account nf-head \
      --project=[gcp-project] \
      --zone=[gcp-zone] \
      --service-account=[gcp-orchestrator-service-account] \
      --scopes=https://www.googleapis.com/auth/cloud-platform
    ```

2. Install Docker Engine on the head node, then sign out and back in so the `docker` group applies.

    ```bash
    sudo apt update
    sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    sudo groupadd docker
    sudo usermod -aG docker $USER
    ```

3. Install the pipeline on the head node.

    ```bash
    git clone [repository URL]
    cd [project-name]
    mamba env create -f conf/[project-name].yml
    mamba activate [project-name]
    ./scripts/setup-githooks.sh
    ```

4. Check the VM metadata credentials and Docker. Revoke any user credentials left from a base image or a manual login, then confirm that the VM uses its attached service account.

    ```bash
    gcloud auth application-default revoke 2>/dev/null || true
    unset GOOGLE_APPLICATION_CREDENTIALS
    test ! -f ~/.config/gcloud/application_default_credentials.json \
      && echo "No user ADC file — metadata credentials will be used"

    curl -sf -H "Metadata-Flavor: Google" \
      http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/email
    # expect: [gcp-orchestrator-service-account]

    gcloud auth application-default print-access-token >/dev/null && echo "ADC OK"
    docker ps
    ```

### Usage

Paste after the explicit local example.

Run in production through Google Batch, from the head node. The head node's service account supplies the credentials:

```bash
nextflow run main.nf \
    -profile googlebatch \
    -work-dir [gcp-scratch-bucket]/work \
    --gcp_project [gcp-project] \
    --gcp_location [gcp-region] \
    --gcp_service_account [gcp-batch-service-account] \
    --gcp_network [gcp-network] \
    --gcp_subnetwork [gcp-subnetwork] \
    --gcp_allowed_locations [gcp-allowed-locations] \
    --outdir [gcp-output-bucket]/[path]/ \
    --input [gcp-scratch-bucket]/[path-to-samplesheet].csv \
    [additional required params with gs:// paths]
```

Run locally while reading data from Google Cloud Storage, with the ADC login from Installation.

```bash
nextflow run main.nf \
    -profile local \
    --gcp_project [gcp-project] \
    --gcp_location [gcp-location] \
    --outdir results \
    --input [gcp-scratch-bucket]/[path-to-samplesheet].csv \
    [additional required params with gs:// paths]
```

### Deployment

Access prerequisite, for the Prerequisites list:

- GCP access through ADC (local machine) or the head node's service account.

Cloud resources, for the Cloud resources subsection:

- Google Batch enabled in `[gcp-region]` in project `[gcp-project]`.
- The Batch worker service account `[gcp-batch-service-account]`. It needs permission to read `[gcp-repository]` when the pipeline has custom container images.
- The scratch bucket `[gcp-scratch-bucket]` for work directories and test outputs.
- The output bucket `[gcp-output-bucket]` for pipeline outputs.
- The reference bucket `[gcp-reference-bucket]` for databases and other reference data.
- The test bucket `[gcp-test-bucket]` for test samplesheet FASTQs.
- An Artifact Registry repository `[gcp-repository]` (address `[gcp-registry-path]`), only if the pipeline has custom container images.

### Development Guidelines

Rows to add to the nf-core lint disables table:

| Flag | nf-core check | Why disabled |
| ---- | ------------- | ------------ |
| `actions_awstest: false` | GitHub workflow for nf-test AWS test | No AWS; pipeline runs on GCP |
| `actions_awsfulltest: false` | GitHub workflow for full AWS test | No AWS; pipeline runs on GCP |

### Testing

Row for the test layers table:

| Layer | What it tests | When it runs |
| ----- | ------------- | ------------ |
| Pipeline integration (GCP) | Production Google Batch run (see below) | Push and Pull Request to `main` via `gcp-integration-test.yml` |

GitHub Actions CI section:

Linting and local nf-test run in the pre-commit hook (see `./scripts/setup-githooks.sh`). CI runs only the GCP integration test:

| Workflow | Trigger | Purpose |
| -------- | ------- | ------- |
| `gcp-integration-test.yml` | Push and Pull Request to `main` | Production Google Batch command below (isolated CI prefixes) |

Repository secrets:

| Secret | Value |
| ------ | ----- |
| `GCP_WORKLOAD_IDENTITY_PROVIDER` | `[gcp-wif-provider]` |
| `GCP_CI_SERVICE_ACCOUNT` | `[gcp-ci-service-account]` |

GCP CI needs workload identity federation (WIF) and these repository secrets. WIF is scoped to the GitHub account that owns the repository. Any repository under that account can reuse the same provider and CI service account once the secrets are set on that repository. The one-time WIF and IAM setup is shared by all of a client's pipelines and is described in the client skill. For a new repository, confirm that the project-level setup is in place and set the two secrets.

Integration test command:

```bash
nextflow run main.nf \
  -profile googlebatch \
  -work-dir [gcp-scratch-bucket]/work \
  --outdir [gcp-scratch-bucket] \
  --input assets/samplesheet_test_googlebatch.csv \
  [additional required params with gs:// paths]
```

CI replaces `-work-dir` and `--outdir` with `[gcp-scratch-bucket]/ci/<github.run_id>/work` and `[gcp-scratch-bucket]/ci/<github.run_id>/results`, so runs do not collide.

### Repo structure

Files to add to the tree:

- `.github/workflows/gcp-integration-test.yml`
- `assets/samplesheet_test_googlebatch.csv`
