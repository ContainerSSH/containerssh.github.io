# How we use Terraform

Our [GitHub organization contains more than 30 repositories](github.md). In order to manage the permissions and settings properly we maintain [a repository with Terraform code](https://github.com/ContainerSSH/github-terraform) that is consumed by [Terraform Cloud](https://terraform.io). To pull this off we make use of the [GitHub provider for Terraform](https://github.com/integrations/terraform-provider-github).

It is worth noting that the documentation may not always be up to date. It also doesn't support managing all properties of GitHub repositories, most prominently the OpenGraph preview images. These are put in place by hand.

Once the code is pushed into the `main` repository in our GitHub repository, the Terraform Cloud picks up the change and applies it. This can be used to generate new repositories or change the settings on a repository.