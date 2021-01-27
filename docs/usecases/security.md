---
title: High security environments
---

Do you need to provide secure access to a console environment and highly sensitive credentials to users? Key management systems like [HashiCorp Vault](https://www.vaultproject.io/) can change credentials frequently to counteract credential leakage or theft by users. However, educating your users to use the key management system can be time-consuming. 

ContainerSSH provides a user-friendly solution. When your users connect to the SSH server it reaches out to an [authentication server](../reference/auth.md) provided by you. This lets you authenticate them against your own user database using passwords or SSH keys.

When authenticated successfully, ContainerSSH contacts your [configuration server](../reference/configserver.md) to get the configuration for your user. The configuration server can expose *short lived* credentials from the key management system in the container environment. Even if your users steal or leak the credentials, they are only valid for a short time.

The [audit log](../reference/audit.md) can record any action taken by a user and upload it to an S3-compatible object storage.

[Get started »](../getting-started/index.md){: .md-button}