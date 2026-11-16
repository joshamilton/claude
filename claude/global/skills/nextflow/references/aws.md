# Nextflow pipelines on AWS (AWS Batch)

Use this file for a pipeline that runs on AWS: production runs go through AWS Batch with data in S3, and development runs use local Docker. Every pipeline on AWS uses the same settings and README text. Only the placeholder values differ from client to client.

Two parts follow the placeholder table:

- "Pipeline settings" holds the AWS parts of `nextflow.config` and `conf/base.config`.
- "README text" holds the sections that fill the bracketed lines that begin with "Cloud:" in the Nextflow README template of the `readme` skill.

## Placeholders

The values are identifiers, not credentials. They come from the cloud table in the client `CLAUDE.md`. Never put a credential, key, or token in a skill or in a repository file.

Cloud values are of two kinds:

- Values that identify an account or a user (for example project, account, region, profile, queue, service account, network) default to `null` in `params`. Pass them on the command line with the parameter name.
- Pipeline-specific settings (for example machine type, disk size, spot use, retries) keep a shared default in `params`.

AWS has job queues, so it has two queue values for spot- and on-demand instances. `docker/build.sh` takes `--cloud aws`, the account, the region, and the profile as flags (see `containers.md` in this folder).

| Placeholder | Meaning |
| ----------- | ------- |
| `[aws-account-id]` | AWS account ID |
| `[aws-region]` | AWS region |
| `[aws-profile]` | AWS CLI profile name for AWS SSO, on a local machine |
| `[aws-queue]` | AWS Batch job queue for production runs |
| `[aws-on-demand-queue]` | AWS Batch job queue for on-demand (not spot) processes |
| `[aws-compute-environment]` | AWS Batch compute environment behind the job queues |
| `[aws-instance-profile]` | IAM instance profile attached to the head-node EC2 instance |
| `[aws-repository]` | ECR repository name for custom container images (the `--repo` value of `docker/build.sh`; the project name by default) |
| `[aws-registry-path]` | ECR address for custom container images: `[aws-account-id].dkr.ecr.[aws-region].amazonaws.com/[aws-repository]` |
| `[aws-scratch-bucket]` | Scratch bucket for work directories and test outputs, with the `s3://` prefix |
| `[aws-output-bucket]` | Bucket for pipeline outputs, with the `s3://` prefix |
| `[aws-reference-bucket]` | Bucket with reference data, with the `s3://` prefix |
| `[aws-test-bucket]` | Bucket with test fixtures, with the `s3://` prefix |

## Pipeline settings

These pieces go into `nextflow.config` and `conf/base.config`. The rest of each file follows the client's template. Identity values are `null`, so no client value is written into the file.

Parameters, in the `params` block:

```groovy
    // AWS options (read by -profile local and -profile batch)
    aws_profile           = null
    aws_region            = null
    aws_queue             = null
    aws_on_demand_queue   = null
    aws_account_id        = null
    aws_max_spot_attempts = 3
```

Entries in `validation.defaultIgnoreParams`:

```groovy
        'aws_profile',
        'aws_region',
        'aws_queue',
        'aws_on_demand_queue',
        'aws_account_id',
        'aws_max_spot_attempts',
```

The `batch` profile, in the `profiles` block:

```groovy
    batch {
        docker {
            enabled = true
        }
        process {
            executor = 'awsbatch'
            queue = params.aws_queue
        }
        aws {
            profile = params.aws_profile
            region = params.aws_region
            batch {
                cliPath = '/home/ec2-user/miniconda/bin/aws'
                maxSpotAttempts = params.aws_max_spot_attempts
            }
        }
    }
```

`cliPath` is the location of the AWS CLI in the custom AMI that the compute environment uses. Every client's AMI installs it at `/home/ec2-user/miniconda/bin/aws`. See `aws.batch.cliPath` in the Nextflow AWS Batch documentation (https://docs.seqera.io/nextflow/reference/executor/aws-batch).

The `seqera` profile, after `batch`, only for a pipeline that runs on Seqera Platform:

```groovy
    seqera {
        docker.enabled = null
        aws = null
        aws {
            batch {
                maxSpotAttempts = 3
            }
        }
        params {
            aws_profile = null
            aws_queue  = null
        }
    }
```

The `local` profile reads S3 data through the same AWS settings, so it has this block:

```groovy
        aws {
            profile = params.aws_profile
            region = params.aws_region
        }
```

Queue assignment, in `conf/base.config`. Assign a queue to a process with `withName`. Processes that must not run on spot instances use the on-demand queue:

```groovy
process {
    // ... shared default configuration (errorStrategy, maxRetries, process_single/low/medium labels) ...

    withName: 'PROCESS_A' {
        cpus   = { 32    * task.attempt }
        maxRetries = 1  // Override default for this specific process
        queue = params.aws_on_demand_queue
    }

    withName: 'PROCESS_B' {
        cpus   = { 32    * task.attempt }
        maxRetries = 1
        queue = params.aws_on_demand_queue
    }
}
```

The custom-image registry path for ECR is built from `aws_account_id` and `aws_region`. See `containers.md` in this folder.

The `local` and `batch` profiles need no ECR block. The images are named in `conf/modules.config`.

## README text

### Installation

Paste after the local development machine commands.

Configure AWS credentials with AWS SSO (IAM Identity Center). Nextflow reads SSO credentials through the profile named by `--aws_profile`, and uses them to read `s3://` paths (work directory, outputs, samplesheet FASTQs, reference databases). Run `aws configure sso` once to create the profile, then sign in:

```bash
aws sso login --profile [aws-profile]
aws sts get-caller-identity --profile [aws-profile]
```

Sign in to Docker for ECR, only if the pipeline has custom container images. A local run pulls the images with this login, which lasts 12 hours (https://docs.aws.amazon.com/AmazonECR/latest/userguide/registry_auth.html). `docker/build.sh` logs in by itself when it pushes:

```bash
aws ecr get-login-password \
    --region [aws-region] \
    --profile [aws-profile] | \
    docker login \
    --username AWS \
    --password-stdin [aws-account-id].dkr.ecr.[aws-region].amazonaws.com
```

Sync the local test assets:

```bash
# Example: sync a reference database or test fixtures needed for local runs
mkdir -p assets/[reference-dir]
aws s3 sync \
  [aws-reference-bucket]/[path-to-reference]/ \
  assets/[reference-dir]/ \
  --profile [aws-profile]
```

AWS head node. This is the EC2 instance that starts production runs. It uses its instance profile for credentials, not SSO.

1. Launch the head-node EC2 instance with the instance profile.

    In the AWS Console:

    1. Open EC2, Instances, in region `[aws-region]`, and click Launch instances.
    2. Choose an Amazon Linux 2023 image, and set the name (for example `nf-head`), instance type, and storage as needed.
    3. Expand Advanced details, and set IAM instance profile to `[aws-instance-profile]`.
    4. Launch the instance, then connect to it.

2. Install Docker Engine on the head node, then sign out and back in so the `docker` group applies.

    ```bash
    sudo yum update -y
    sudo yum install -y docker
    sudo service docker start
    sudo usermod -a -G docker ec2-user
    ```

3. Install the pipeline on the head node.

    ```bash
    git clone [repository URL]
    cd [project-name]
    mamba env create -f conf/[project-name].yml
    mamba activate [project-name]
    ./scripts/setup-githooks.sh
    ```

4. Check the instance credentials and Docker. Nextflow looks for a named profile, environment variables, and the default profile before it uses the instance profile (https://docs.seqera.io/nextflow/amazons3), so remove any user credentials left from a base image or a manual login, then confirm that the instance uses its instance profile.

    ```bash
    unset AWS_PROFILE AWS_DEFAULT_PROFILE AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY AWS_SESSION_TOKEN
    test ! -f ~/.aws/credentials \
      && echo "No credentials file — the instance profile will be used"

    aws configure list
    # expect: the access_key and secret_key lines do not name a credentials file or an environment variable

    aws sts get-caller-identity
    # expect: an assumed-role ARN for the role in [aws-instance-profile]

    docker ps
    ```

    If `~/.aws/credentials` exists, delete its profiles by hand, and remove any `[default]` profile that holds credentials from `~/.aws/config`.

### Usage

Paste after the explicit local example.

For a pipeline that runs on Seqera Platform, put this subsection in Usage, before the AWS Batch run command:

````markdown
### Running the pipeline in production via Seqera Platform

[Usage instructions]
````

Run in production through AWS Batch, from the head node. The head node's instance profile supplies the credentials, so `--aws_profile` is not needed. `--aws_account_id` is needed only when the pipeline has custom container images:

```bash
nextflow run main.nf \
    -profile batch \
    -work-dir [aws-scratch-bucket]/work \
    --aws_region [aws-region] \
    --aws_account_id [aws-account-id] \
    --aws_queue [aws-queue] \
    --aws_on_demand_queue [aws-on-demand-queue] \
    --outdir [aws-output-bucket]/[path]/ \
    --input [aws-scratch-bucket]/[path-to-samplesheet].csv \
    [additional required params with s3:// paths]
```

Run locally while reading data from S3, with the SSO profile from Installation:

```bash
nextflow run main.nf \
    -profile local \
    --aws_profile [aws-profile] \
    --aws_region [aws-region] \
    --outdir results \
    --input [aws-scratch-bucket]/[path-to-samplesheet].csv \
    [additional required params with s3:// paths]
```

### Deployment

Access prerequisite, for the Prerequisites list:

- AWS access through AWS SSO (local machine) or the head node's instance profile.

Cloud resources, for the Cloud resources subsection:

- An AWS Batch compute environment `[aws-compute-environment]`, using the custom AMI with the AWS CLI at `/home/ec2-user/miniconda/bin/aws`. Its instance role needs permission to pull from `[aws-repository]` when the pipeline has custom container images.
- The job queues `[aws-queue]` and `[aws-on-demand-queue]` in `[aws-region]`.
- The head-node instance profile `[aws-instance-profile]`, with permission to submit Batch jobs and read and write the buckets.
- A VPC, subnets, and security groups set up for the compute environment.
- The scratch bucket `[aws-scratch-bucket]` for work directories and test outputs.
- The output bucket `[aws-output-bucket]` for pipeline outputs.
- The reference bucket `[aws-reference-bucket]` for databases and other reference data.
- The test bucket `[aws-test-bucket]` for test samplesheet FASTQs.
- An ECR repository `[aws-repository]` (address `[aws-registry-path]`), only if the pipeline has custom container images.

### Development Guidelines

Rows to add to the nf-core lint disables table: none recorded. If the pipeline's `.nf-core.yml` disables `actions_awstest` or `actions_awsfulltest`, add a row for each with the reason.

### Testing

Row for the test layers table: none. There is no AWS CI workflow yet.

GitHub Actions CI section: none. Delete the GitHub Actions CI subsection from the README.

Integration test command: none. Leave the cloud integration command out of the README.

### Repo structure

Files to add to the tree: none.
