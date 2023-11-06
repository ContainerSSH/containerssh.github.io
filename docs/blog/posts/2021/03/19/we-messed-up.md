---
date: 2021-03-19
title: We broke your images
description: Two days ago we pushed a change that broke all ContainerSSH container images on the Docker hub.
image: images/blog/we-messed-up/preview.png
---

# We broke your images 😢

Two days ago, on *March 17, 2021 around 4:30 PM UTC* we pushed a change to our build system that broke the container images we published on the [Docker Hub](https://hub.docker.com/u/containerssh/). This change resulted in the following error when running the container:

> Cannot start service containerssh: OCI runtime create failed: container_linux.go:349: starting container process caused "exec: \"/containerssh\": permission denied": unknown

To make matters worse, this did not only affect the most recent image, it broke all container images. The issue [was reported an hour later](https://github.com/ContainerSSH/ContainerSSH/issues/146) and fixed on around *noon UTC on the 18th of March, 2021*.

If you are affected by this issue you can pull the fixed ContainerSSH image by pulling it:

=== "Docker"
    ```
    docker pull containerssh/containerssh:<version>
    ```
=== "Podman"
    ```
    podman pull containerssh/containerssh:<version>
    ```
=== "Kubernetes"
    Please set the `imagePullPolicy` in your pod spec to `Always` or switch to the image `containerssh/containerssh:<version>-20200318`

The `<version>` tag in this case should be replaced with your ContainerSSH version (e.g. `0.3.1`).

<!-- more -->

**There is no way around it: we messed up.** Pretty badly at that, we potentially broke your production environment without an easy way to roll back to a previous version. This should not happen, not even in a pre-1.0 version, especially not with something as trivial as a permission mistake.

These images should have never made it to the Docker Hub, our testing procedures (obviously lacking) should have caught this and [we are determined to fix them](https://github.com/ContainerSSH/images/issues/1). **We are very sorry for the inconvenience and the potential outage this issue has caused.**

!!! tip "Please reach out to us"
    If you need to reach out quickly you can [tag or DM us in Twitter](https://twitter.com/ContainerSSH) to notify the core maintainers.

## Versioning in the future

Going forward the ContainerSSH images will be versioned in two parts: the ContainerSSH version and the image build date. For example, the image tag `0.3.1-20200318` points to the image built from ContainerSSH version 0.3.1 on the 18th of March, 2020. The tag `0.3.1` points to the latest built from ContainerSSH version 0.3.1. The tag `0.3` points to the latest ContainerSSH version in the 0.3 series, and so on. You can find the full list of available tags on the [Docker hub](https://hub.docker.com/r/containerssh/containerssh/tags).

!!! tip "Why are we doing this?"
    This is necessary because container base images (Alpine Linux in our case) get security updates much more frequently than we release ContainerSSH versions.

## Why did this happen (post mortem)

With the upcoming 0.4 release we are drawing closer to creating a first stable version of ContainerSSH (1.0). As part of the effort to secure the container images we publish we are now using [Snyk](https://snyk.io/), graciously made available to open source projects for free. As we scanned our container images built late last year we realized that there were multiple vulnerable libraries in them. These vulnerabilities did not affect ContainerSSH, but it highlights the need to update the images we release much more frequently than we release new ContainerSSH versions. It is also unreasonable to ask system administrators to jump through the hoops of switching to a new ContainerSSH version just because there is a new container image available. Therefore, we decided to version the container images separately from ContainerSSH as described above.

However, our existing build system ([Goreleaser](https://goreleaser.com/), an excellent tool) does not have the capability to manage images in this manner. Therefore, we had to come up with a new build system. We were looking at several ones, but none of them could fulfill the need for a cross-platform build system that is easy for developers to run on their potentially non-Linux machines. Therefore, [we decided to code](https://github.com/ContainerSSH/images) the relatively simple process of building a container image in [Go](https://golang.org/). This tool downloads the Linux `.tar.gz` files from the [GitHub releases](https://github.com/ContainerSSH/ContainerSSH/releases) as specified in the [configuration](https://github.com/ContainerSSH/images/blob/3824289b8966f5ff481d2d6ff7bc87e85e0389b1/build.yaml) and unpacks them.

This is where the critical mistake happened: the unpacking code [used `os.Create()` instead of `os.OpenFile()`](https://github.com/ContainerSSH/images/blob/3824289b8966f5ff481d2d6ff7bc87e85e0389b1/build.go#L169). This resulted in the permissions not being set on the files extracted from the archive. The [`Dockerfile` moved from the Goreleaser build system](https://github.com/ContainerSSH/images/blob/c1528274e331254eb6758cefdb467c5d975d09bc/containerssh/Dockerfile) also did not contain the required `chmod` instruction.

How did this make it into production? It clearly never should have, and that's a hole in our testing procedures. It is not enough for us to test the ContainerSSH code, we should have tested the built images before pushing them, no matter what build tool was used. Mistakes can happen, we need to make sure big ones don't make it to the images you are using.

To fix this issue we will institute automated tests in the build tool that [test the functionality of ContainerSSH end-to-end](https://github.com/ContainerSSH/images/issues/1) by opening a real SSH connection and executing a real command. This will not be a comprehensive test suite since those are covered by lower level tests, but we will test if the SSH connection can be established, the containers are started, and the output of an executed command is as expected.

To sum it up, here's what we learned:

1. Create automated end to end tests for container images before they are pushed.
2. Don't rely on a previously-working `Dockerfile` in different circumstances.
3. Always explicitly set permissions for binaries in the `Dockerfile`, don't rely on filesystem permissions.
4. Make sure you keep permissions across the whole toolchain.

Again, we are very sorry we messed up this badly, we will do everything we can to not repeat this mistake.
