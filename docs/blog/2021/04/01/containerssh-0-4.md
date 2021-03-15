---
title: "ContainerSSH 0.4"
description: We are announcing the immediate availability of ContainerSSH 0.4 
image: images/blog/containerssh-0-4/preview.png
---

# No april fool's joke: ContainerSSH 0.4

In [November last year](../../../2020/11/25/the-road-to-0-4.md) we were optimistic that we'd be launching 0.4 early 2020 with the **new audit logging feature**. Now it is finally time: we are very proud to announce the [immediate availability of **ContainerSSH 0.4**](../../../../downloads/index.md).

## TL;DR

What we added:

- [Audit logging](/reference/audit.md)
- [Improved logging](/reference/logging.md)
- [New SSH proxy backend](/reference/sshproxy.md)
- [New Kubernetes backend](/reference/kubernetes.md)
- [New Docker backend](/reference/docker.md)
- [New security layer](/reference/security.md)

What we deprecated:

- [The KubeRun backend](/deprecations/kuberun.md)
- [The DockerRun backend](/deprecations/dockerrun.md)
- [The Listen config option](/deprecations/listen.md)
- [The sessionId parameter in the auth/config webhook](/deprecations/sessionId.md)
- [The pubKeyBase64 field in the auth webhook](/deprecations/publicKeyBase64.md)

## Audit logging

The biggest feature of this release is no doubt the audit logging feature. This audit log **records everything a user does, on a byte-by-byte basis**. That includes things like SFTP uploads, which may slip through your net if you just record typed commands. The audit logging feature can also upload the stored audit logs to an S3-compatible object storage for long-term archival.

In the future we plan to release a tool to visually inspect the stored audit logs, and the planned SSH proxy feature will allow you to use it with traditional SSH servers.

For details check out the [audit logging reference manual](../../../../reference/audit.md).

## New SSH proxy backend

This new backend forwards connections to a second SSH server instead of starting containers. This makes it possible to use ContainerSSH in two roles:

1. As a way to dynamically authenticate SSH users or dynamically route users to SSH backends.
2. As a way to audit SSH connections after decryption.

For details check out the [logging reference manual](../../../../reference/sshproxy.md).

## Better logging

One of the reasons why this release took so long to complete was the addition of a [comprehensive logging interface](../../../../reference/logging.md). We added **hundreds of log messages**, most of them on the debug level that allow you to trace exactly what ContainerSSH is doing. Each of the log messages contains a unique code you can use to identify what's wrong with your setup. These codes are documented [in the codes list](../../../../reference/codes.md).

We also added options for log targets: you can now log to a file, a syslog server via `/dev/log` or UDP, or to the standard output.

For details check out the [logging reference manual](../../../../reference/logging.md).

## New Kubernetes backend

Since we wanted to support more use cases we added a completely new backend for Kubernetes to replace the now-deprecated `KubeRun` backend. The `KubeRun` backend will remain available until the next release.

This new backend supports the new [agent we announced back in December](../../../2020/12/24/the-agent.md) to support all the SSH features Kubernetes doesn't normally support. For example, the agent will fix a long-standing issue with Kubernetes where the user would not see the shell because it was written to the standard output before ContainerSSH has attached to the pod.

In addition, ContainerSSH supports **multiple execution models**. The original execution from `KubeRun` would run one pod per session (multiple pods per SSH connection). The new (default) execution mode now creates one pod per SSH connection and uses the `kubectl exec` functionality to start the programs for the individual sessions.

This also paves the way for future development where we will have (semi) persistent pods. For details check the [Kubernetes backend reference manual](../../../../reference/kubernetes.md) and the [KubeRun deprecation notice](../../../../deprecations/kuberun.md).

## New Docker backend

Similar to the Kubernetes backend above this release also adds a new backend for Docker and Podman, deprecating the `DockerRun` backend. The old `DockerRun` backend will remain available until the next release.

As with Kubernetes the new backend supports the new [agent we announced back in December](../../../2020/12/24/the-agent.md) to support all the SSH features Kubernetes doesn't normally support, mainly signal delivery.

In addition, ContainerSSH supports **multiple execution models**. The original execution from `DockerRun` would run one container per session (multiple pods per SSH connection). The new (default) execution mode now creates one container per SSH connection and uses the `docker exec` functionality to start the programs for the individual sessions.

This also paves the way for future development where we will have (semi) persistent containers. For details check the [Docker backend reference manual](../../../../reference/docker.md) and the [DockerRun deprecation notice](../../../../deprecations/dockerrun.md).

## Security filters

This release also adds a set of security filters that can be used for **fine-grained control over what SSH interactions** to allow or block. For example, you could limit the user to a set of environment variables, only allow running certain programs, etc.

For details check the [security reference manual](../../../../reference/security.md).

## SSH key format

In the previous releases we transmitted the SSH key to the authentication server in the OpenSSH wire format. This was not easy to implement so in this release we switch to the more popular authorized key format, which is transmitted in the `publicKey` field.

For details check the [deprecation notice](https://containerssh.io/deprecations/publicKeyBase64/)

## Reference manual

Alongside of this release we are also adding a [comprehensive reference manual](../../../../reference/) which describes in great detail how to set up and configure ContainerSSH.

## Future plans

This release is a 90% rewrite of the ContainerSSH codebase which splits it into [modules](https://github.com/containerssh/). This presents a basis for exciting new features, such as SSH proxying, SSH single sign-on via a web interface (OAuth2/OIDC), web client, launching VMs instead of containers, etc.

For details on the planned features please check our [development dashboard](https://containerssh.io/development/dashboard/).
