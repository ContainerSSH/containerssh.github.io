<h1>ContainerSSH Reference Manual</h1>

The Reference Manual provides reference material for ContainerSSH 0.4 and is oriented towards system operators wishing to use ContainerSSH on their system.

## Introduction

This manual contains documentation on how to set up, configure, monitor, and secure the ContainerSSH installation.

## Changes since ContainerSSH 0.3

ContainerSSH 0.4 is major overhaul to the internal structure. As such, this release contains several major improvements to the stability of ContainerSSH. The reference manual for ContainerSSH 0.3 is [available here](./0.3/index.md).

### Audit logging

The most visible improvement of this release is the new [audit logging facility](audit.md). Audit logging allows operators to capture everything that is happening within an SSH connection, including passwords, keys, typed commands, or SFTP uploads. The audit log can automatically be uploaded to an S3-compatible object storage.

### The Kubernetes backend

The new [Kubernetes backend](kubernetes.md) replaces the previous [KubeRun backend](kuberun.md). The new Kubernetes backend supports two modes of operation: running a pod per session (multiple per connection) or one pod per connection, using the `exec` facility. Support for the new [ContainerSSH agent](https://github.com/containerssh/agent) means that the Kubernetes backend now has support for all functions in SSH.

The full list of changes is described in the [KubeRun deprecation notice](../deprecations/kuberun.md).

### The Docker backend

The new [Docker backend](docker.md) replaces the previous [DockerRun backend](dockerrun.md). The new Docker backend supports two modes of operation: running a pod per session (multiple per connection) or one pod per connection, using the `exec` facility. Support for the new [ContainerSSH agent](https://github.com/containerssh/agent) means that the Docker backend now has support for all functions in SSH.

The full list of changes is described in the [DockerRun deprecation notice](../deprecations/dockerrun.md).

### Scoped SSH configuration

In order to facilitate multiple daemons in a single binary the SSH `listen` configuration is now located under the `ssh` key. 

The change is described in the [listen deprecation notice](../deprecations/listen.md).

### Unified connectionId for authentication and configuration webhooks

In the previous version ContainerSSH sent a `sessionId` field to the authentication and configuration servers. This is now replaced with the opaque `connectionId`, which is mirrored in log files.

The change is described in the [sessionId deprecation notice](../deprecations/sessionId.md).

### SSH key format

In the previous version ContainerSSH sent the SSH key in the OpenSSH binary format in the `publicKeyBase64` field. This format was not easy to integrate to it is replated with the `publicKey` field containing the SSH key in the authorized key format.

The change is described in the [publicKeyBase64 deprecation notice](../deprecations/publicKeyBase64.md).

### Multiple log formats

This release also adds the ability to output the logs in text format next to the JSON format. The details are described in the [logging reference](logging.md).
