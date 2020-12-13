---
title: Creating ContainerSSH releases
---

<h1>Creating releases</h1>

Once the code is written it comes to creating a release. This document will cover how a release is created, both for libraries and applications 

## Versioning

When heading up to a release versioning must be kept in mind. We follow [SemVer](https://semver.org/), so only major versions may contain breaking changes. The only exception is versions before `1.0.0`, these may break in minor versions too.

For applications we aim to support a major version as long as feasible. We do not want to break configuration file formats, backend features, protocols, etc. unless it is absolutely unavoidable.

However, such a guarantee is not made for libraries. Our libraries are primarily intended for consumption by ContainerSSH, so we may decide to bump the major version at any time. We have to keep in mind, however, that bumping a major version of a library means that all depending libraries will need to be updated.

## Release notes

Once the main branch is ready for release the last step is writing release notes. We do not follow the concept of simply listing the commits, we aim to write human-readable release notes that explain the changes. The explanation has to be detailed enough so anyone from the target audience can understand what is changing without needing to understand the implementation.

The release notes should be added to `CHANGELOG.md`.

## Creating a release

The day has finally come: the release notes and codes are in, tests are passing. Now we need to create a release. We do this exclusively from the GitHub interface. We name versions for libraries in the format of `v1.2.3` so Go can pull them in, while applications are named `1.2.3` to avoid pulling them in from a Go program.

We copy the name and description from the `CHANGELOG.md` into the release notes on GitHub. For applications the release mechanism will create and upload the binaries.

Once this process is complete we announce the release on the public channels.