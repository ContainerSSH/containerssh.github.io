# How we use the Docker Hub

[Docker Hub](https://hub.docker.com/u/containerssh) is our main distribution point for ContainerSSH images. We also maintain mirrors on [Quay.io](https://quay.io/repository/containerssh/containerssh).

Docker has graciously included us in their open source program so our images are **not subject to rate limits**. This is especially important because ContainerSSH pulls [the default guest image](https://hub.docker.com/repository/docker/containerssh/containerssh-guest-image) (an Ubuntu with the installed guest agent and SFTP) from the Docker Hub for every connection. At the time of writing this image has already been pulled more than 100.000 times.

In order to make sure that our pushes are independent from any one person we have created a machine user called `containersshbuilder`, which only has permissions to the ContainerSSH organization. The credentials of this user are added to [GitHub actions](github.md).

The container images are build using the [images repository](https://github.com/ContainerSSH/images). This repository contains a Go build program that uses [`docker-compose`](https://docs.docker.com/compose/) to build and test ContainerSSH images before pushing them. (We learned this [the hard way](../../blog/2021/03/19/we-messed-up.md).)

The default guest image on the other hand is rebuilt daily to incorporate the latest updates.