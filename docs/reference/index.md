title: ContainerSSH Reference Manual

<h1>ContainerSSH Reference Manual</h1>

The Reference Manual provides reference material for ContainerSSH 0.4 and is oriented towards system operators wishing to use ContainerSSH on their system.

## Introduction

This manual contains documentation on how to set up, configure, monitor, and secure the ContainerSSH installation. If you need a one minute primer on how ContainerSSH works please [watch this video](https://www.youtube.com/watch?v=Cs9OrnPi2IM).

## Changes since ContainerSSH 0.4.0

ContainerSSH 0.4.1 is a bugfix release resolving several issues with the previous release. The reference manual for ContainerSSH 0.4.0 is [available here](0.4.0/index.md).

### Incorrect handling of container configuration with Docker backend

The 0.4.0 release introduced [a bug discovered by a user](https://github.com/ContainerSSH/ContainerSSH/issues/201) which prevented setting the ContainerSSH image from the configuration server. The reason behind this failure was the incorrect JSON serialization. This release fixes the serialization and restores the correct way of operations.

### Incorrect handling of Kubernetes configuration

Kubernetes uses a different YAML serialization library which lead to it being impossible to set volume parameters and potentially other options in the configuration file [as discovered by a user](https://github.com/ContainerSSH/ContainerSSH/issues/209). This release fixes this issue by using the Kubernetes YAML serialization for the Kubernetes configuration only.

### Incorrect handling of the password/pubkey options

The previous version [ignored the `password` and `pubkey` options](https://github.com/ContainerSSH/ContainerSSH/issues/167) in the authentication section and sent all requests to the authentication server regardless of the setting. This release fixes that and restores the function of these options to the way they worked in version 0.3.