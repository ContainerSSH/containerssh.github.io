---
date: 2026-03-22
title: "ContainerSSH 0.6.0: Persistent Pods"
description: "ContainerSSH 0.6.0: Persistent Pods"
---

# ContainerSSH 0.6: Persistent Pods

ContainerSSH 0.6 has been released! This release introduces the persistent Kubernetes execution mode, extra scope support for OIDC authentication, important bug fixes for Kerberos and Docker image pulling, and a lot of dependency updates.

## Change summary

1. [Persistent Kubernetes execution mode](#persistent-kubernetes-execution-mode)
2. [OIDC extra scopes](#oidc-extra-scopes)
3. [Kerberos authentication fixes](#kerberos-authentication-fixes)
4. [Docker image pull policy fix](#docker-image-pull-policy-fix)

## Persistent Kubernetes execution mode

A new `persistent` execution mode has been added to the Kubernetes backend. Unlike the existing `connection` mode which create a new pod for each SSH connection and terminates the pod after the session terminates, `persistent` mode execs into an already existing pod with an option to create the pod if it doesn't exist, or to simply refuse entry if it doesn't. This mode can be useful for use-cases where stateful sessions are needed, including but not limited to managing long-running interactive processes, resource sharing etc.

!!! warning "ContainerSSH cannot guarantee user isolation in this mode"
    It is expeced that the users of this feature will use the configuration server to **ensure that every user is dropped into the correct pod**, ideally unique per-user. Do not specify the pod to use in the global configuration as this will lead to all users to be sent to the same pod without any isolation. If this is combined with any type of credential forwarding it can lead to the users credentials being compromised.

In the simplest form the persistent mode can be configured with the following block:

```yaml
kubernetes:
  pod:
    mode: persistent
    metadata:
      name: my-existing-pod
      namespace: default
```

With the `createMissingPods` option a minimal pod spec is also required:

```yaml
kubernetes:
  pod:
    mode: persistent
    createMissingPods: true
    metadata:
      name: my-pod
      namespace: default
    spec:
      containers:
        - name: shell
          image: containerssh/containerssh-guest-image
```

Thanks to [@gigabyte132](https://github.com/gigabyte132) for contributing this feature.

[Read more »](/reference/kubernetes){: .md-button}

## OIDC extra scopes

The OIDC authentication provider now supports requesting additional scopes beyond the default `openid` scope. 

Two new configuration options have been added for the oidc provider:

- **`extraScopes`**: A list of additional OIDC scopes to request during authentication.
- **`enforceScopes`**: When set to `true`, authentication will be rejected if the user does not grant all requested extra scopes.

```yaml
auth:
  keyboardInteractive:
    method: oauth2
    oauth2:
      provider: oidc
      oidc:
        url: https://your-oidc-server.example.com/
        extraScopes:
          - profile
          - email
        enforceScopes: true
```

These options work with both the device flow and authorization code flow.

Thanks to [@hashkrish](https://github.com/hashkrish) for contributing this feature.

[Read more »](/reference/auth-oauth2){: .md-button}

## Kerberos authentication fixes

This release fixes two issues with Kerberos authentication:

- **`enforceUsername=false` now works correctly.** Previously, disabling username enforcement would still reject valid logins with differing usernames.
- **Metadata merging is now additive.** Kerberos authentication metadata is now correctly merged with existing connection metadata instead of replacing it. This ensures that metadata set by earlier authentication or configuration steps is preserved.

Thanks to [@gigabyte132](https://github.com/gigabyte132) for contributing this feature.

## Docker image pull policy fix

The behavior of the `IfNotPresent` image pull policy has been corrected. Previously, images with no tag or the `:latest` tag were always pulled even when already present locally, which prevented using local images. The `IfNotPresent` policy now consistently skips pulling when the image is already available locally, regardless of the tag.

Thanks to [@AlbertoPimpo](https://github.com/AlbertoPimpo) for the fix
