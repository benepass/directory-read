# Infra

This repository contains the [Terraform](https://terraform.io) definition to create the infrastructure in the cloud. The environments are separated by [Terraform workspace](https://www.terraform.io/docs/state/workspaces.html). If you're looking to learn how to create or setup the application infrastructure locally check the [project README.md file](../README.md).

### Requirements

 - [Terraform 1.1.9](https://releases.hashicorp.com/terraform/1.1.9/terraform_1.1.9_darwin_amd64.zip)
 - [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)

### Getting started

If the application is already deployed to s3 the following steps can be skipped, but if this is the first run ever of Terraform, we need to create the S3 bucket and DynamoDB table that will be used has a backend for Terraform state. To create it, follow the step-by-step bellow:

    - `cd setup`
    - `terraform init`
    - `terraform apply` - Confirm with a "yes"
    - Copy the "bucket" output param (it will look like: `<project_name>-terraform-state`).
    - At `./main.tf` file, change the param `bucket` in the terraform block by the value you previously copied.
    - Copy the "dynamodb_table" output param (will look like: `<project_name>-terraform-locks`).
    - In the same `terraform` block that you edited, change the param `dynamodb_table` by the the value you previously copied.
    - Now, you can run the code of root directory.

### Deploy to AWS using terraform

Make sure to not have any file overriding the any configuration. Check for `<file>_override.tf` inside the `terraform` folder. These files are meant to run only on local mode.

There on, after you've created the s3 bucket and DynamoDB table you need to follow the steps below if you're creating a new environment on AWS. If you want to run a single command jump to item 6.

1. Initialize terraform in your local machine

``` shell
terraform init
```

2. Create a workspace

``` shell
terraform workspace new $(env)
```

3. Plan and apply the modifications

``` shell
terraform plan
terraform apply (if you agree with the modifications)
```

Note the command above will output a few environmnet variables that you may need to add into [chalice configuration file](../.chalice/config.json). Now you're ready to create the lambda terraform files using chalice and deploying it again.

4. Build terraform (make sure that you're on the root folder). This command will generate two files: `deployment.zip` and `chalice.tf.json` into the terraform folder.

``` shell
chalice package --stage $(env) --pkg-format terraform terraform/
```

5. Plan and apply the modifications again

Note: The steps above are all centralized on this [file](../Makefile).

6. Setup terraform, build app and deploy it. Ps: Use it with caution.

``` shell
make deploy env=$(env)
```

