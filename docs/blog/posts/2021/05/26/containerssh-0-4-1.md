---
date: 2021-05-26
title: "ContainerSSH 0.4.1: Bugfixing Audit & Proxy"
description: "We are announcing the immediate availability of ContainerSSH 0.4.1: Bugfixing Audit & Proxy"
---

# ContainerSSH 0.4.1: Bugfixing Audit & Proxy

ContainerSSH 0.4.1 is [now available](/downloads/) and contains several bugfixes for the previous version. We encourage all users to upgrade. 

<!-- more -->

## Changes in detail

This release fixes 3 bugs that were introduced with the refactor to version 0.4.0. These are:

- [#201: Incorrect JSON serialization/deserialization from the configuration server when using the Docker backend](https://github.com/containerssh/containerssh/issues/201)
- [#209: Incorrect YAML deserialization when using the Kubernetes backend](https://github.com/containerssh/containerssh/issues/209)
- [#167: Authentication server ignores password and pubkey options](https://github.com/containerssh/containerssh/issues/167)

Thanks to GitHub users [ne-bknn](https://github.com/ne-bknn) and [tomcsi](https://github.com/tomcsi) for reporting these issues.

## Incorrect JSON serialization/deserialization from the configuration server when using the Docker backend

When refactoring ContainerSSH for version 0.4.0 we implemented the JSON serialization and deserialization for the Docker backend incorrectly [as reported by GitHub user ne-bknn](https://github.com/containerssh/containerssh/issues/201). The returned JSON from the configuration server had this structure:

```json
{
  "docker": {
    "execution": {
      "Launch": {
      }
    }
  }
}
```

The `Launch` component is not supposed to be in this structure and should be inlined. The serialization is now fixed and the `Launch` component is removed.

## Incorrect YAML deserialization when using the Kubernetes backend

Another serialization issue [has been reported by GitHub user tomcsi](https://github.com/containerssh/containerssh/issues/209). This issue has been present since version 0.3 where we added Kubernetes support. Kubernetes uses its own YAML serialization and [deserialization library](https://sigs.k8s.io/yaml) based on [ghodss/yaml](https://github.com/ghodss/yaml). This library doesn't add separate YAML tags to the configuration structures, but instead uses the JSON tags. This prevented using several Kubernetes configuration options, such as the `hostPath` volume type:

```yaml
backend: kubernetes
kubernetes:
  pod:
    spec:
      volumes:
        - name: home
          hostPath:
            path: /home/ubuntu
            type: Directory
```

We have now introduced using the Kubernetes YAML decoding library for the Kubernetes and KubeRun backends only to facilitate proper serialization. 

## Authentication server ignores password and pubkey options

Another bug we discovered after the release was that the new version did't take into account the `password` or `pubkey` options in the authentication section.

The authentication server could just reject those authentication methods, but in order to cut down on 404 entries in the logs we added these options. This release restores the aforementioned functionality.

## Upgrading to the new release

If you haven't upgraded to version 0.4.0 yet please see the [0.4.0 announcement](../../04/01/containerssh-0-4.md) for details on what changed from version 0.3. If you have already upgraded to 0.4.0 we recommend testing the new release for you scenario before upgrading and scheduling a brief downtime as you upgrade both the auth-config servers and ContainerSSH itself.
