---
title: "InstantInfra: Setup an AWS account"
date: 2025-11-17T12:59:54+01:00
draft: false
cover:
  image: https://oschvr.s3.dualstack.us-west-2.amazonaws.com/002_instantinfra_setup_aws_account_171125.png
---

> Setting up an AWS account with a minimal IAM setup that can be used with Terraform (IaC)

Today, I will attempt to:

- Open a new AWS cloud account
- Set up their recommended IAM structure
- Create the necessary IAM resources to be used by Terraform/OpenTofu
- Test it out

All of this within 10 minutes (excluding any verification or external waiting times)

> DISCLAIMER: This is ONE solution of many different approaches. As of today, what you will see here is commonly found in forums. Keep in mind it might evolve.

#### You will need the following

- **A valid credit card** _(No charges will be made, unless you start deploying stuff)_
- **A physical address** _(For the billing)_
- **An email** _(AWS recommends to use an email address that can be accessed by a group, in order to maintain accessibility)_
- [AWS CLI v2](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) installed
- One of the following:
  - [Terraform (v1.10.0)](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli) installed
  - [OpenTofu (v1.10.0)](https://opentofu.org/) installed

So let's get started:

### Setting up the account

This is the manual part of the exercise. And by manual I mean, not programmatic or that you need to go to their website and follow their instructions.

1. Let's go to https://aws.amazon.com/
2. Click on **Create an AWS account**
3. Follow their instructions to accept their terms
4. Enter a payment method
5. Follow through
6. Choose a Basic/Developer Support Plan, you can change this later
7. Wait for activation

### Configuring the IAM

So, at this point you have a fresh AWS account usable with the root account (the email you just used to create the AWS account).

**It is EXTREMELY important that you keep this account safe and you don't use it except for very exceptional cases**

You might or might not be familiar with the AWS console, but in every cloud platform, there is a similar concept (perhaps even the same name) of IAM, that is, Identity and Access Management.
This is where you configure who has access to what, and how.

Given that this is the first time you do it, you will have to configure the IAM to avoid touching the root account in day to day activities:

1. Login using the root account
2. Go to IAM to protect it with MFA
3. Configure another account with less privileges
4. Create access keys for this new account and save them somewhere safe.

Let's do step 1 and 2 first.

1. Go to https://aws.amazon.com/
2. Click on login using the root account

Once that's done, we can move onto creating the IAM resources needed to interact with AWS programmatically

#### Creating the IAM account for Terraform/OpenTofu

So now we need to create a "user" for our IaC tools, that will have a "policy" (set of permissions to perform actions on resources).

You might ask, What is the correct policy?

> [The correct policy will be the policy that allows the user to perform the actions on the resources you need](https://stackoverflow.com/a/72140646)

In this case and for this series, we will create an [IAM User](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users.html) and assign it a [AdministratorAccess](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AdministratorAccess.html) (managed) policy, so our IaC tooling will have full access to all AWS services and resources

The policy looks like this:

```
{
  "Version" : "2012-10-17",
  "Statement" : [
    {
      "Effect" : "Allow",
      "Action" : "*",
      "Resource" : "*"
    }
  ]
}
```

Allow every (`*`) action on every (`*`) resource.

Alternatively you could at this point go and create a custom policy to `DENY` some

```
{
  "Version" : "2012-10-17",
  "Statement" : [
    {
      "Effect" : "Allow",
      "Action" : "*",
      "Resource" : "*"
    },
    {
      "Effect" : "Deny",
      "Action" : "*",
      "Resource" : "iam:*"
    }
  ]
}
```

Which would mean: allow every (`*`) action on every resource except those of `iam:`

There are many more approaches that cater to the different security postures, one that requires a bit more work to setup, but it's recommended is to use [IAM Roles](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html).

For now we'll proceed to create a IAM User for the IaC tools:

1. Go to IAM > Access management
2. Click on Create user
3. Assign the name `iac` (or whatever you want)
4. Don't provide access to the console
5. Attach policies directly and then search for `AdministratorAccess`
6. Create user
7. Click on the user > Security credentials
8. Go to Access keys and create a pair
9. Select other and click Next
10. Save your credentials somewhere safe

### Testing out

Finally, you've a set of AWS access keys that you can use to configure Terraform with and start provisioning Infrastructure as Code

The best way is to use the official provider https://registry.terraform.io/providers/hashicorp/aws/latest

Create a new file `main.tf`

```terraform
terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "5.91.0"
    }
  }
}

provider "aws" {
  # Configuration options
}


data "aws_billing_service_account" "main" {}

output {
	value = data.aws_billing_service_account.main
}

```

This is essentially a "ping" or a "hello world" to verify that Terraform can talk to AWS

Before proceeding, I created an alias that I will be using throughout the series, [learn more about my opinion about terraform vs opentofu](/posts/instant-infra-opentofu-vs-terraform/)

```shell
# If you use Terraform
alias tf="terraform"

# If you use OpenTofu
alias tf="tofu"
```

Then do the following

```shell
tf init
tf apply
```

You should be able to see Terraform communicating with AWS and creating a plan that you will be prompted to apply

Hit `yes` and then you should see an output like this

```terraform
aws_billing_service_account = XXXXX
```

Done, you're all setup.
