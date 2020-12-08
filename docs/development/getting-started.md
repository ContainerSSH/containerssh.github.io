<h1>Getting started with ContainerSSH development</h1>

Welcome to developing ContainerSSH! For the purposes of this guide we will assume you have your [development environment set up and ready to go](devenv/index.md). If not, please [follow our handy guide to do just that](devenv/index.md).

Ready? Good.

## Cloning the repository

Before we begin you will have to decide what you want to do. If you just want to **get ContainerSSH running** to get the big picture you will need to clone the [ContainerSSH/ContainerSSH repository](https://github.com/containerssh/containerssh). This contains the main ContainerSSH executable, as well as the Auth-Config server used for testing:

```
git clone https://github.com/containerssh/containerssh
```

However, ContainerSSH is built in a highly modular fashion so you may need to change a specific library. You can find the list of libraries [on our development dashboard](dashboard.md). This dashboard contains an overview of all repositories, issues, pull requests, and everything else you will need to find your way around the codebase.

Each repository contains a **readme** explaining how to use that specific component. If you find the readme not helpful please open an issue on that repository asking for more information.

If you find yourself needing a new repository because you want to develop something completely new please file a pull request against the [github-terraform](https://github.com/containerssh/github-terraform) repository.

!!! tip
    For the best results we recommend cloning the ContainerSSH repos into `/path/to/your/home/go/src/github.com/containerssh/REPONAME`.

## Running ContainerSSH

Running ContainerSSH is simple. You will need a clone of the main ContainerSSH repository. Then you have to run two commands.

First, the auth-config server needs to be run from the `cmd/containerssh-testauthconfigserver` directory:

```
go run .
```

When that's running create the `cmd/containerssh/config.yaml` file with the following content:

```yaml
---
log:
  level: debug
ssh:
  hostkeys:
    - ssh_host_rsa_key
backend: dockerrun
auth:
  url: "http://127.0.0.1:8080"
  pubkey: false
configserver:
  url: "http://127.0.0.1:8080/config"
```

Now copy the `ssh_host_rsa_key` file from the `example` folder and then run ContainerSSH from the `cmd/containerssh` folder:

```
go run . --config config.yaml
```

That's it! Now you have a running ContainerSSH you can connect to on port 2222:

```
ssh foo@localhost -p 2222
```

## Running the tests

There are two types of tests for ContainerSSH: end to end tests and component-level tests. Both can be run using the following command from each library's main folder:

```
go test ./...
```

!!! tip
    Some tests require a working Docker or Kubernetes backend. Make sure that your Docker socket is running on your platform default and your Kubernetes configuration is available in the `.kube/config` file in your home directory as the tests will use these to connect to.

## Submitting a pull requests

Once you are done with your development you should fork the repository on GitHub and [create a pull request](https://docs.github.com/en/free-pro-team@latest/github/collaborating-with-issues-and-pull-requests/about-pull-requests). This pull request will automatically be tested by the CI system. Feel free to keep working on your PR until you are happy with it.

## Understanding ContainerSSH

ContainerSSH is a reasonably complex piece of software. It uses the built-in Go SSH library to create a server and the client libraries for Docker and Kubernetes to forward the data from the SSH channel to the standard input and output of the container.

We have dedicated a [whole section](containerssh/index.md) to understanding how SSH and ContainerSSH in particular work.