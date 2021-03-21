# How we use GitHub

Our [GitHub account](https://github.com/ContainerSSH) contains over 30 repositories. These repositories are managed by [Terraform](terraform.md) and most of them are created from the [library-template](https://github.com/ContainerSSH/library-template) template repository. This is done in an effort to make sure each component has its own tests and documentation.

Tests in each repository are executed by GitHub actions. Most repositories use [CodeQL](https://github.com/github/codeql-action) for security analysis, [golangci-lint](https://github.com/golangci/golangci-lint-action) for code quality, and run `go test` for executing tests.

Some repositories have integrations with Docker and Kubernetes. Docker is included in GitHub Actions and Kubernetes support is added by using the [Kubernetes in Docker action](https://github.com/marketplace/actions/kind-kubernetes-in-docker-action). When running against Kubernetes we run against all [currently supported versions](https://kubernetes.io/docs/setup/release/version-skew-policy/). The tests use the kubeconfig of the current user to fetch the configuration on how to connect Kubernetes. An example of this can be found [in the Kubernetes repository](https://github.com/ContainerSSH/kubernetes/blob/main/.github/workflows/tests.yml).

When we release ContainerSSH we use [Goreleaser](https://github.com/goreleaser/goreleaser-action) to create binaries for multiple platforms. Goreleaser is also responsible for uploading the generated binaries to GitHub as a release. Currently, Goreleaser also generates `.deb` and `.rpm` packages. Later on, this will be replaced by providing a package repository that people can add to their operating systems. [This is also hosted in GitHub Pages](https://github.com/ContainerSSH/packages).

