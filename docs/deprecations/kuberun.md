---
title: Deprecating the KubeRun backend
image: deprecations/kuberun.png
---

# Deprecating the KubeRun backend {{ since("0.4") }}

In version `0.4` ContainerSSH receives [a generalized Kubernetes backend](../reference/kubernetes.md) and we are deprecating the `kuberun` backend from version `0.3.1` and earlier. We are adding this new backend because we are changing several default values to options which could cause security problems if the old configuration was used. Version `0.4` still includes support for the `kuberun` backend, but log a warning when used:

> You are using the kuberun backend deprecated since ContainerSSH 0.4. This backend will be removed in the future. Please switch to the new docker backend as soon as possible. See https://containerssh.io/deprecations/kuberun for details.

This page explains how to switch to the new backend.

## Changing the configuration structure

The new configuration structure is very similar to the old `kuberun` structure. The most important change is the relocated and more detailed timeouts section:  

```yaml
kubernetes:
  timeouts:
    # Timeout for a container to start.
    podStart: 60s
    # Timeout for a container to stop.
    podStop: 60s
    # Timeout for a shell or command to start.
    commandStart: 60s
    # Timeout for HTTP calls
    http: 15s
    # Timeout for signal requests
    signal: 60s
    # Timeout for window change requests
    window: 60s
```

This replaces the old `kubernetes` &rarr; `connection` &rarr; `timeout` option.

The configuration now also moves the `kubernetes` &rarr; `pod` &rarr; `namespace` option to the new `metadata` section, which is can now be fully customized with Kubernetes pod metadata. The `podSpec` option was renamed `spec` to align with Kubernetes:

```yaml
kubernetes:
  pod:
    metadata:
      namespace: default
      generateName: myPodNamePrefix-
      labels:
        foo: bar
  # Rename podSpec
  spec:
```

Please run `kubectl explain pod.metadata` for the full list of options.

## The new execution modes

The new `kubernetes` backend supports two execution modes: `connection` or `session`. The old `kuberun` backend worked identical to the `session` mode, where each command execution within an SSH connection would cause a new container to be started.

The new `connection` mode, on the other hand, starts a container with an idle command from the configuration and then uses the `exec` facility to launch commands.

In `connection` mode the pods are launched with the command specified in `kubernetes` &rarr; `pod` &rarr; `idleCommand` as a command. The purpose of this command is to keep the pod alive and wait for a `TERM` signal. Any commands (shell, etc.) will be launched similar to how you would use `kubectl exec` to run an additional command in the pod. When a shell is requested the `kubernetes` &rarr; `pod` &rarr; `shellCommand` parameter is used.

!!! warning
    The `connection` execution mode means that the `CMD` and `ENTRYPOINT` settings from the container image or the configuration are ignored. If you are switching from the `kuberun` backend and used the `CMD` as a security measure it is strongly recommended that you configure the `idleCommand` and `shellCommand` options properly.

## The guest agent

ContainerSSH 0.4 also includes support for the new [ContainerSSH Guest Agent](https://github.com/containerssh/agent) that enables several features the Kubernetes API does not support support. For example, the guest agent enables waiting for ContainerSSH to attach to the process in `session` mode before starting the desired program. **It is strongly recommended to enable the guest agent for Kubernetes** as the API misses several features required for proper operations.

The agent [must be included into the guest image](https://github.com/containerssh/agent) in order to work. When the agent is included it can be configured as follows:

```yaml
kubernetes:
  pod:
    # Path to the new ContainerSSH Guest Agent.
    agentPath: "/usr/bin/containerssh-agent"
    # Disable the ContainerSSH guest agent.
    disableAgent: true
```

!!! warning
    The agent is enabled by default, you should explicitly disable it if you want to run an image that doesn't have an integrated agent.

## Removing the `disableCommand` option

The `disableCommand` option was added to ContainerSSH to prevent connecting users to run a custom application. This filled a similar role to the `ForceCommand` option in OpenSSH: it prevented connecting users to launch custom commands.

However, this command was separately implemented in the `kuberun` and in the `dockerrun` backend. This was not maintainable, so it was moved into the `security` module and can be configured as follows:

```yaml
security:
  command:
    mode: disable
```
