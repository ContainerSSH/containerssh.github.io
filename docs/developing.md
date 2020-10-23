<h1>Developing ContainerSSH</h1>

Welcome! And a big thank you for wanting to contribute! This page will explain how to get started with contributing to ContainerSSH.

## Tooling

ContainerSSH is written in [go](https://golang.org/). Love it or hate it, it's one of the simplest way to create a single binary you can package into a container and it happens to have an excellent SSH library, which is somewhat of a rarity. If you want to contribute you will have to do so in Go. If you are not familiar with it you might want to take [Effective Go](https://golang.org/doc/effective_go.html) for a spin.

If you have Go somewhat in your grasp we would recommend installing either [VSCode](https://code.visualstudio.com/) or [Goland](https://www.jetbrains.com/go/) as having an IDE with code completion will help you with navigating around the code. We personally use Goland, but it's not free so VSCode may be the way to go for you.

Finally, you will need a working Docker or Kubernetes environment. We recommend installing Docker Desktop as it provides both out of the box.

## Running in a development environment

Before you can start with writing code you will need to grab the `config.example.yaml` in the repository and the `ssh_host_rsa_key` file in the `example` folder. Copy these to the `cmd/containerssh` folder and then run the following command in the same folder:

```
go run . --config config.example.yaml
```

Additionally, you will need to run the dummy config-auth server. Execute the following command in the `cmd/containerssh-testconfigauthserver` directory:

```
go run .
```

Now that you have both daemons running, you can connect the SSH server:

```
ssh foo@localhost -p 2222
```

That's it! You can now start hacking the code.

## Running tests

You can run the tests using `go test`. Make sure to **stop the SSH and auth-config server** you started above, otherwise some tests will fail.

## Understanding ContainerSSH

ContainerSSH is a reasonably complex piece of software. It uses the built-in Go SSH library to create a server and the client libraries for Docker and Kubernetes to forward the data from the SSH channel to the standard input and output of the container.

Before you begin we recommend reading [this blog post](https://pasztor.at/blog/ssh-direct-to-docker/) that runs you through a simplified version of ContainerSSH called [MiniContainerSSH](https://github.com/janoszen/minicontainerssh).