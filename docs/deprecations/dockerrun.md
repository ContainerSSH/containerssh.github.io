---
title: Deprecating the DockerRun backend
image: deprecations/dockerrun.png
---

# Deprecating the DockerRun backend {{ since("0.4") }}

In version `0.4` ContainerSSH receives a [generalized Docker backend](../reference/docker.md) and we are deprecating the `dockerrun` backend from version `0.3.1` and earlier. We are adding this new backend because we are changing several default values to options which could cause security problems if the old configuration was used. Version `0.4` still includes support for the `dockerrun` backend, but log a warning when used:

> You are using the dockerrun backend deprecated since ContainerSSH 0.4. This backend will be removed in the future. Please switch to the new docker backend as soon as possible. See https://containerssh.io/deprecations/dockerrun for details.

This page explains how to switch to the new backend.

## Changing the configuration structure

The new configuration is structured into 3 components:

```yaml
docker:
  connection:
    # These options were on the root level of the dockerrun configuration.
    host:
    cacert:
    cert:
    key:
  execution:
    # These options are moved here from the old dockerrun -> config option.
    container:
      # ...
    host:
      # ...
    network:
      # ...
    platform:
      # ...
    containername: ""

    # Subsystems that can be requested.
    subsystems:
      sftp: /usr/lib/openssh/sftp-server

    # the "disableCommand" option has been removed and is configured in the
    # "security" option.

    # Pick an image pull policy from "Always", "IfNotPresent" or "Never". See below.
    imagePullPolicy: "IfNotPresent"
 
    # Execution mode, see below.
    mode: connection
    # Idle command for the new "connection" mode, see below.
    idleCommand:
      - "/bin/sh"
      - "-c"
      - "sleep infinity & PID=$!; trap \"kill $PID\" INT TERM; wait"
    # Shell command  for the new "connection" mode, see below.
    shellCommand:
      - "/bin/bash"
    # Path to the new ContainerSSH Guest Agent.
    agentPath: "/usr/bin/containerssh-agent"
    # Disable the ContainerSSH guest agent.
    disableAgent: true
    
  timeouts:
    # This section replaces the dockerrun -> config -> timeout option.

    # Timeout for a container to start.
    containerStart: 60s
    # Timeout for a container to stop.
    containerStop: 60s
    # Timeout for a shell or command to start.
    commandStart: 60s
    # Timeout for HTTP calls
    http: 15s
    # Timeout for signal requests
    signal: 60s
    # Timeout for window change requests
    window: 60s
```

## The new execution modes

The new `docker` backend supports two execution modes: `connection` or `session`. The old `dockerrun` backend worked identical to the `session` mode, where each command execution within an SSH connection would cause a new container to be started.

The new `connection` mode, on the other hand, starts a container with an idle command from the configuration and then uses the `docker exec` facility to launch commands.

In `connection` mode the pods are launched with the command specified in `docker` &rarr; `execution` &rarr; `idleCommand` as a command. The purpose of this command is to keep the pod alive and wait for a `TERM` signal. Any commands (shell, etc.) will be launched similar to how you would use `docker exec` to run an additional command in the pod. When a shell is requested the `docker` &rarr; `execution` &rarr; `shellCommand` parameter is used.

!!! warning
    The `connection` execution mode means that the `CMD` and `ENTRYPOINT` settings from the container image or the configuration are ignored. If you are switching from the `dockerrun` backend and used the `CMD` as a security measure it is strongly recommended that you configure the `idleCommand` and `shellCommand` options properly.

## The guest agent

ContainerSSH 0.4 also includes support for the new [ContainerSSH Guest Agent](https://github.com/containerssh/agent) that enables support for various features the Docker API does not provide, such as sending signals to processes.

The agent [must be included into the guest image](https://github.com/containerssh/agent) in order to work. When the agent is included it can be configured as follows:

```yaml
docker:
  execution:
    # Path to the new ContainerSSH Guest Agent.
    agentPath: "/usr/bin/containerssh-agent"
    # Disable the ContainerSSH guest agent.
    disableAgent: true
```

!!! warning
    The agent is enabled by default, you should explicitly disable it if you want to run an image that doesn't have an integrated agent.

## Image pull policy

The new `docker` backend also includes an option when to pull images. This option helps with the [Docker Hub rate limits](https://docs.docker.com/docker-hub/download-rate-limit/) and is built to be similar to the [Kubernetes option with the same name](https://kubernetes.io/docs/concepts/containers/images/#updating-images).

!!! tip
    Docker has added ContainerSSH as an [Open Source Community Application](https://www.docker.com/community/open-source/application). Pulls to `containerssh/containerssh` and the default guest image `containerssh/containerssh-guest-image` are excluded from the rate limits.

```yaml
docker:
  execution:
    # Pick an image pull policy from "Always", "IfNotPresent" or "Never". See below.
    imagePullPolicy: "IfNotPresent"
```

The following options are supported:

`Always`
: Always pulls images. This is the same behavior as the `dockerrun` backend.

`IfNotPresent`
: Pull image if it is not locally present, has no image tag, or has the `:latest` tag.

`Never`
: Never pulls the image. If the image is not locally present the execution will fail.

## Removing the `disableCommand` option

The `disableCommand` option was added to ContainerSSH to prevent connecting users to run a custom application. This filled a similar role to the `ForceCommand` option in OpenSSH: it prevented connecting users to launch custom commands.

However, this command was separately implemented in the `kuberun` and in the `dockerrun` backend. This was not maintainable, so it was moved into the `security` module and can be configured as follows:

```yaml
security:
  command:
    mode: disable
```
