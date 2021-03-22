---
title: Creating ContainerSSH library releases
---

# Releasing a library

ContainerSSH is made up of [over 30 libraries](https://github.com/ContainerSSH/). These libraries are all written in Go and must, therefore, follow the [Go modules specification](https://golang.org/ref/mod). It's not the most exciting read, but you should familiarize yourself with the process. We will attempt to outline the most important steps here.

## Versioning

When heading up to a release versioning must be kept in mind. We follow [SemVer](https://semver.org/), so only major versions may contain breaking changes. The only exception is versions before `1.0.0`, these may break in minor versions too. This includes methods like factories (e.g. `New` methods).

With Go modules versions beyond version 1 should have the module suffix `v2`, `v3`, etc. For example, you may have a module called `github.com/containerssh/auth/v2`.

## Release notes

Once the main branch is ready for release the last step is writing release notes. We do not follow the concept of simply listing the commits, we aim to write human-readable release notes that explain the changes. The explanation has to be detailed enough so anyone from the target audience can understand what is changing without needing to understand the implementation.

The release notes should be added to `CHANGELOG.md`.

## Updating the README

Before creating a release the `README.md` file should be updated such that consumers of the library know how to use the new version of the library. Except for a few libraries like [auth](https://github.com/ContainerSSH/auth/) and [configuration](https://github.com/ContainerSSH/configuration/) our libraries are intended only for consumption in ContainerSSH. This means that you can write the documentation from that perspective.

## Creating a release

The day has finally come: the release notes and codes are in, tests are passing. Now we need to create a release. We do this exclusively from the GitHub interface. We name versions for libraries in the format of `v1.2.3` so Go can pull them in, while applications are named `1.2.3` to avoid pulling them in from a Go program.

We copy the name and description from the `CHANGELOG.md` into the release notes on GitHub. For applications the release mechanism will create and upload the binaries.
