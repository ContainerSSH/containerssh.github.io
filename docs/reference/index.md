title: ContainerSSH 0.5.0 Reference Manual

<h1>ContainerSSH 0.5.0 Reference Manual</h1>

The Reference Manual provides reference material for ContainerSSH 0.4 and is oriented towards system operators wishing to use ContainerSSH on their system.

## Introduction

This manual contains documentation on how to set up, configure, monitor, and secure the ContainerSSH installation. If you need a one-minute primer on how ContainerSSH works please [watch this video](https://www.youtube.com/watch?v=Cs9OrnPi2IM).

## Changes since ContainerSSH 0.4.1

ContainerSSH 0.5.0 is a feature release. The reference manual for ContainerSSH 0.4.1 is [available here](0.4.1/index.md). This release adds two main new features:

1. OAuth authentication
2. Passing metadata from authentication to configuration servers and backends

## [OAuth authentication](auth-oauth2.md)

In this release we are adding first class OAuth2 support using the keyboard-interactive authentication method. While not all clients support this, the main desktop SSH clients (OpenSSH, PuTTY, WinSCP, Filezilla, etc) do.

With this authentication method the user is prompted to visit a website and complete an OAuth2 authentication process in order to log in. Depending on the OAuth2 flow used the user must then either enter a return code or will simply be logged in automatically.

If a return code is needed, the code the user should copy is presented on a built-in web interface.

As the implementation is provider-specific, ContainerSSH currently only supports OIDC-compliant providers and GitHub. Please request additional via [a GitHub feature request](https://github.com/ContainerSSH/ContainerSSH/issues/new/choose).

[Read more &raquo;](auth-oauth2.md)

## Authentication metadata

Based on a [user request](https://github.com/ContainerSSH/ContainerSSH/issues/109) we have added the ability to return key-value pairs from the authentication server and pass them on to the configuration server, or expose them directly as environment variables in backends.

[Read more &raquo;](auth-webhook.md#response)

## Health check endpoint

This release also adds a health check endpoint to integrate ContainerSSH with load balancers.

[Read more &raquo;](health.md)