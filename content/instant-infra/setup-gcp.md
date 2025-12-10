---
title: "InstantInfra: Setup a GCP Account"
date: 2025-11-20
draft: false
cover:
  image: https://oschvr.s3.dualstack.us-west-2.amazonaws.com/004_instantinfra_setup_gcp_account_201125.png
---

> Setting up a new GCP account with a minimal IAM setup that can be used with TF (IaC)

Today, I will attempt to:

- Open a new GCP cloud account
- Create the necessary IAM resources to be used by Terraform/OpenTofu (for this channel !)
- Test it out

> DISCLAIMER: This is ONE solution of many different approaches. As of today, what you will see here is commonly found in forums. Keep in mind it might evolve.

#### You will need the following

- **A valid credit card** _(No charges will be made, unless you start deploying stuff)_
- **A physical address** _(For the billing)_
- **An email** (This email has to be registered previously as a Google Account)
- [gcloud cli](https://docs.cloud.google.com/sdk/docs/install)
- One of the following:
  - [Terraform (>v1.10.0)](https://developer.hashicorp.com/terraform/tutorials/gcp-get-started/install-cli) installed
  - [OpenTofu (>v1.10.0)](https://opentofu.org/docs/intro/install/) installed

---

I created an alias that I will be using throughout the series ([learn more about my opinion about terraform vs opentofu](/instant-infra/opentofu-vs-terraform/))

```shell
# If you use Terraform
alias tf="terraform"

# If you use OpenTofu
alias tf="tofu"
```

---

### Setting up the account:

1. Go to https://cloud.google.com/
2. Click on **Start free**
3. Connect using your Google Account
4. Enter your address and payment method

You'll get US $300 in credits **valid for 90 days** in your new account, however, you are likely to get charged a €25 (or your local currency equivalent) one time payment to make sure the card works and its valid, but as it says in the disclaimer, you can get this refunded

Anyways, after this you should be logged in and ready to use the GCP console.

> We will not go over the Organisation setup as that is more targeted to production-ready enterprise workloads.

Feel free to use the default project or create a new one If you choose to create a new one, go to the project selector at the top and the click create project. Name it whatever you like

In any case, save the project id, we'll use it later.

### Configure the initial IAM

We will proceed to create a (**Service Account**)[https://docs.cloud.google.com/iam/docs/service-account-overview] for TF

We will use [`Basic > Owner`](https://docs.cloud.google.com/iam/docs/roles-overview#legacy-basic) (_which is generally not recommended_). Basic roles provide **broad** access to Google Cloud resources, and thus they can be quite insecure. Learn more about [GCP roles](https://docs.cloud.google.com/iam/docs/roles-overview)

However, since I will be using this account with the broadest level of access to experiment... it doesn't really matter !

### Create the IAM account for TF

1. Login using the root/owner account
2. Go to **IAM & Admin**
3. Go to **Service Accounts** and click **Create Service Account**
4. Add a descriptive, but short name, then optionally add a description. I will use `tf` and `infrastructure as code service account` respectively
5. Click **Create and continue**
6. In permissions, click select role `Basic > Owner`
7. Finally, click **Done** to skip the last step (Principals with access)
8. Once created, click on your new service account
9. Go to `Keys > Add key > Create new key` and leave `JSON`. I like to use the `{{name}} + - + sa` (`tf-sa.json`)
10. Download it to a safe location in your computer, I'll use `~/.gcp/` (First do `mkdir ~/.gcp`)

### Testing it out

We now have the GCP key associated to our TF service account that will allow us to start provisioning Infrastructure as Code. There are [multiple ways](https://docs.cloud.google.com/docs/terraform/authentication) to authenticate with TF to GCP. The one I will be using is to (export the env var)[https://docs.cloud.google.com/docs/terraform/authentication#auth_using_sa_keys_onprem] `GOOGLE_APPLICATION_CREDENTIALS` in my `~/.zshrc` (note: you might be using Bash, or Fish, so this will change for you)

```shell
# export the env var on session start
echo "export GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/tf-sa.json" >> ~/.zshrc

# reload
source ~/.zshrc
```

Let's test this with TF

> You'll find [here](https://github.com/oschvr/instantinfra) all the code bellow

```terraform


# main.tf
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.8.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = "europe-west2"
  zone    = "europe-west2-a"
}

# data.tf
data "google_project" "project" {
  project_id = var.project_id
}

output "project_number" {
  value = data.google_project.project.number
}

output "project_id" {
  value = data.google_project.project.id
}

```

This is essentially a "ping" or a "hello world" to verify that TF can talk to GCP

Then do the following

```shell
tf init
tf apply
```

You should be able to see TF communicating with GCP and creating a plan that you will be prompted to apply

Hit `yes` and then you should see an output like this

```terraform
project_number = XXXXX
project_id = XXX/XXX
```

Since we didn't create any resource, we will not run `tf destroy`

See you on the next one !
