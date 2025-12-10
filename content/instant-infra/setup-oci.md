---
title: "InstantInfra: Setup a OCI Account"
date: 2025-12-03
draft: false
cover:
  image: https://oschvr.s3.dualstack.us-west-2.amazonaws.com/010_instantinfra_setup_oci_account_031225.png
---

> Setting up an OCI account with a minimal IAM setup that can be used with TF (IaC)

Today, I will attempt to:

- Open a new OCI (Oracle Cloud) cloud account
- Create the necessary IAM resources to be used by TF
- Test it out

All of this within 10 minutes (excluding any verification or external waiting times)

#### You will need the following

- **An email**
- [OCI CLI](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/cliconcepts.htm) installed
- One of the following:
  - [Terraform (>v1.10.0)](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli) installed
  - [OpenTofu (>v1.10.0)](https://opentofu.org/) installed

---

I created an alias that I will be using throughout the series ([learn more about my opinion about terraform vs opentofu](/instant-infra/opentofu-vs-terraform/))

```shell
# If you use Terraform
alias tf="terraform"

# If you use OpenTofu
alias tf="tofu"
```

---

Let's begin

### Setting up the account

1. Head to https://www.oracle.com/cloud/free
2. Hit **Start for free**
3. Enter your details and click continue

You'll get US $300 in credits **valid for 30 days** (for all the managed services) and access to all [_Always Free Resources_](https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm) which should allow us to play around with self hosted stuff

### Configuring the initial IAM

Oracle calls their accounts, `tenancies` which can have `identity domains` (we're not going to use these as we'll use the `default`) and `compartments`. This is likely usefuly for large scale operations/accounts.

And I believe the concept of compartments is similar to projects in GCP. At first we land in the `root` compartment and normally this logical abstraction becomes the parent of `dev`, `staging`, `prod` etc.

But we are ignoring that and we'll use `root` for everything here. (unless we explicitly want to play around with IAM later)

### Create the IAM account for TF

Having said that we'll use the `default` identity domain and that we want to use the `root` compartment (all), we first need to create

- A (**User**)[https://docs.oracle.com/en-us/iaas/Content/GSG/Tasks/addingusers.htm] I'll use `tf`
- A (**Group**)[https://docs.oracle.com/en-us/iaas/Content/Identity/groups/create-groups.htm] For this I'll use `instantinfra`

and finally

- A (**Policy**)[https://docs.oracle.com/en-us/iaas/Content/Identity/policymgmt/managingpolicies_topic-To_create_a_policy.htm]

OCI's policies use the following structure (case insensitive)

```
allow group [group_name] to [verb] [resource-type] in compartment [compartment-name] where [condition]
```

you can replace `in compartment ...` by `in tenancy` and that will apply to all subsequent `compartments`

```
allow group [group_name] to [verb] [resource-type] in tenancy
allow group instantinfra to manage all-resources in tenancy
```

1. Head to (search for) **Identity & Security**
2. Then to **Domains** and
3. Click **Default** and got to **User management**
4. Create a **Group** called `instantinfra`
5. Create a **User** Add first name, last name and email and then add the user to the `instantinfra` Group
6. Go back from **Domains** into **Policies** and click create
7. Name it `instantinfra`, click on manual editor
8. Paste `allow group instantinfra to manage all-resources in tenancy` and create

You are effectively allowing the **User** in the **Group** that we created, admin access to every resource in the account, I hope you are aware of the power you just gave to yourself !

1. Go back to **Identity & Security**/**Domains**/**User management** and click on the user you just created
2. Go to the **API keys** section and click add
3. Leave the `Generate API key pair`
4. Download both your private and public keys to a safe location in your computer, I like to use `{{name}}.key` (`tf.key`) and then for location, I'll use `~/.oci` (First do `mkdir ~/.oci`)
5. Click add and you will get a snippet that starts with `[DEFAULT]`. Copy it
6. Paste it in a new file `~/.oci/config`
7. Make sure that when you paste it, the field `key_file` actually points to the key

```shell
[DEFAULT]
user=ocid1.user.oc1..aaaaaaaa*****
fingerprint=0f:**:**:**
tenancy=ocid1.tenancy.oc1..aaaaaaaa*****
region=uk-london-1
key_file=/path/to/your/tf.key
```

### Testing it out

Ok so we have a OCI API Key from a User with a Policy that we can use with our TF setup. Similar to other clouds, there are [multiple ways](https://docs.oracle.com/en-us/iaas/Content/dev/terraform/configuring.htm#authentication) to authenticate with TF to OCI. Since we're using the [API Key](https://docs.oracle.com/en-us/iaas/Content/dev/terraform/configuring.htm#api-key-auth) method (default), the documentation specifies that the provider will read the auth config from `~/.oci/config` (which we just did above)

Let's test this with TF

> You'll find [here](https://github.com/oschvr/instantinfra) all the code bellow

```terraform
# main.tf
terraform {
  required_providers {
    oci = {
      source = "oracle/oci"
    }
  }
}

provider "oci" {
  region = var.region
}

# data.tf
data "oci_identity_tenancy" "main" {
  tenancy_id = var.tenancy_ocid
}

# output.tf
output "tenancy_name" {
  value = data.oci_identity_tenancy.main.name
}

# variables.tf
variable "region" {
  type    = string
  default = "uk-london-1"
}

variable "tenancy_ocid" {
  type = string
}

# variables.auto.tfvars
tenancy_ocid = "ocid1.tenancy.oc1..aaaaaaaa*****"

```

This is essentially a "ping" or a "hello world" to verify that TF can talk to OCI

Then do the following

```shell
tf init
tf apply
```

You should be able to see TF communicating with OCI and creating a plan that you will be prompted to apply

Hit `yes` and then you should see an output like this

```terraform
tenancy_name = XXXXX
```

Since we didn't create any resource, we will not run `tf destroy`

See you on the next one !
