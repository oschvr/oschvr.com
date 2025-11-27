---
title: "InstantInfra: AWS S3 Storage Bucket"
date: 2025-11-18
draft: false
cover:
  image: https://oschvr.s3.dualstack.us-west-2.amazonaws.com/003_instantinfra_aws_storage_bucket_181125.png
---

> Setup a simple storage bucket resource using IaC

Today, I will:

- Setup a basic storage bucket through tf
  In less than 10 minutes

### Prerequisites

- **An active AWS account**: Make sure to check my previous video/post where I setup a brand new AWS account and configure IAM <> tf.

> I will be using [this repo](https://github.com/oschvr/instantinfra) to run my challenges, so you'll find all the challenges code there.

I do have to mention that you can provision an AWS S3 Bucket using the fantastic [terraform-aws-modules](https://github.com/terraform-aws-modules) however for the purposes of the channel, I will use the native provider resources

To see what resources you have available, you can consult the providers documentation

[Terraform](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
[OpenTofu](https://search.opentofu.org/provider/opentofu/aws/latest)

Here's the one I will do today

[aws_s3_bucket](https://registry.terraform.io/providers/hashicorp/aws/5.44.0/docs/resources/s3_bucket)

### Code

Go to `clouds/aws/s3-bucket` and you'll see the following files

```
# main.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "6.21.0"
    }
  }
}

provider "aws" {
  region = "eu-west-2"
}
```

```
# variables.tf
variable "prefix" {
  type = string
  default = "instantinfra"
}
```

```
# bucket.tf
resource "aws_s3_bucket" "instantinfra_bucket" {
  bucket = "${var.prefix}-bucket"
}
```

Once you see this, you can hit
`

```
tf init
tf apply
```

And your bucket should be created.

To destroy this bucket, go and do

```
tf destroy
```
