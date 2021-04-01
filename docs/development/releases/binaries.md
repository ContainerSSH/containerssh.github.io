title: Creating ContainerSSH binary releases

# Creating ContainerSSH binary releases

ContainerSSH binaries are what our users consume. This guide will attempt to outline the steps we take to make sure these releases are stable and no steps have been left out.

## Documentation

The first step when preparing a new release the first step is to start preparing the documentation. The documentation for a new release always goes on the `containerssh.io/reference/upcoming/` section. This section is copied from the current documentation and is modified for the new release. The new documentation pages must also be added to the `mkdocs.yaml` to make sure they are in the menu.

If there are deprecated features they must be added to the `deprecations` section of the documentation. Deprecation notices should be written from the perspective of a user, explaining not only what's been deprecated, but also how to upgrade and replace the deprecated feature.

You should also pay attention to the quick start section of the website, which may need to be updated for the new version. However, these changes should be added to a branch, only to be merged when the new release goes online.

## Versioning

When creating a new release you must consider what version number to pick. We follow [SemVer](https://semver.org/) for ContainerSSH. Backwards-incompatible changes should increase the minor version number before 1.0, and increase the major version number after 1.0. Minor, backwards incompatible features should increase the minor version number, while bugfixes and security updates should increase the patch version number.

## Tests

The main [ContainerSSH repository](https://github.com/ContainerSSH/ContainerSSH) contains a battery of tests that should pass before any release is made. If new features are added tests should be added to match.

## Releasing binaries

Binaries are automatically generated using [Goreleaser](https://goreleaser.com) when a tag is created in the [ContainerSSH repository](https://github.com/ContainerSSH/ContainerSSH). This will create and upload the built binaries to the GitHub releases section.

However, with the binaries being available the job is not done. The build configuration in the [images repository](https://github.com/ContainerSSH/images) must be updated and a tag must be made. This will ensure that the new container images are pushed to the registries.

 