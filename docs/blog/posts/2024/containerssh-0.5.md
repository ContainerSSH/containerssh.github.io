---
date: 2024-01-06
title: "ContainerSSH 0.5: Everything but the kitchen sink"
description: "ContainerSSH 0.5 has been released, including a huge amount of changes and features. Port forwarding, ..."
---

# ContainerSSH 0.5: Everything but the kitchen sink

After a long slumber ContainerSSH is back with a brand new release! A tremendous amount of changes have been incorporated since the last release including multiple codebase refactors, a move to a monorepo setup for our internal modules and many long and highly requested features such as Oauth2, Kerberos authentication, port and connection forwarding and an advanced metadata handling system.

<!-- more -->

## Configuration Restructure

The structure of the configuration file has been slightly altered especially when pertaining to the authentication settings and the configuration server. Please consult the [reference docs](/reference) or the [quickstart guide](/getting-started/configuration) and update your configuration file to the new format.

## Change summary

1. [OAuth2 and Kerberos authentication](#oauth2-and-kerberos-authentication)
2. [Authorization webhook](#authorization-webhook)
3. [Passing metadata from authentication to configuration servers and backends](#metadata-handling)
4. [Deploying files into the containers from the authentication and configuration hooks](#deploying-files)
5. [X11 forwarding](#port-socket-and-x11-forwarding)
6. [SSH keepalives](#ssh-keepalives)
7. [Health check endpoint](#health-check-endpoint)
8. [Changes to the Prometheus integration](#changes-to-the-prometheus-integration)
9. [Removed the deprecated DockerRun and KubeRun backends](#removal-of-the-deprecated-dockerrun-and-kuberun-backends)

## OAuth2 and Kerberos authentication

The biggest change of this release is support for multiple authentication backends. Thanks to our contributors we now have support for OAuth2 and Kerberos authentication.

OAuth2 authentication works with GitHub and any OIDC-compliant authentication server, such as Keycloak and Microsoft Active Directory Federation Services. We have actively worked with several SSH client vendors to make this authentication method work and we are happy to report that it works in OpenSSH, PuTTY, Filezilla, WinSCP, and more. The authentication prompts the user to click on a link in their SSH client and then log in via their normal browser-based flow. What's more, you can automatically expose the GitHub or OIDC token to the container. Your users can directly use their credentials in your ContainerSSH environment.

Similarly, Kerberos authentication is also useful in an enterprise setting. When users are logged in to their personal devices using company credentials, they will now be able to automatically log in to ContainerSSH with Kerberos. Optionally, users can also log in to ContainerSSH from a non-authenticated device using username and password, and ContainerSSH will automatically create a Kerberos ticket for them. This ticket is available in the container directly, so your users can work with their Kerberos credentials without any additional steps.

[Read more »](/reference/auth){: .md-button}

## Authorization webhook

As part of our authentication and authorization overhaul we added a separate webhook. This webhook lets you match up the username entered in SSH and the authenticated credentials in a separate step. You can, for example, authenticate a user from Kerberos and then use a webhook to match up their Kerberos identity with the SSH username. 

[Read more »](/reference/auth-webhook){: .md-button}

## Metadata handling

The authentication and configuration servers now support passing metadata between each-other and to ContainerSSH.

[Read more »](/reference/auth-webhook#response){: .md-button}

## Deploying files

As part of the new metadata system both the authentication and configuration servers can now set environment variables and deploy files in the container user containers. This functionality depends on the ContainerSSH agent to be installed and available in the container image.

[Read more »](/reference/auth-webhook#response){: .md-button}

## Port, socket and X11 forwarding

From this release support for forward and reverse port forwarding is supported natively, as a result remote development with VSCode and similar functionalities in other IDEs can now be used with ContainerSSH as long as forwarding is enabled. For these features the ContainerSSH agent has to be enabled as the agent acts as the entry & exit points of the connections inside the container.

The features implemented correspond to the openssh commands:

### Forward & Reverse port forwarding

Example: Forward port 8080 on the local host the service running on port 8080 on the remote container
```
ssh -L 8080:127.0.0.1:8080 user@example.org
```

Example: Forward connections from a socket on the local machine to a socket in the container
```
ssh -L /path/to/local/socket:/path/to/remote/socket
```

Example: Forward connections from port 8080 on the container to the service running on port 8080 on the local machine
```
ssh -R 8080:127.0.0.1:8080
```

Example: Forward connections from a socket on the container to a socket on the local machine
```
ssh -L /path/to/local/socket:/path/to/remote/socket
```

### Connection proxying support (e.g. SOCKS)

```
ssh -D 8080 user@example.com
```

You can then use ContainerSSH as a proxy with anything that supports the SOCKS protocol (e.g. Firefox)

### X11 forwarding

```
ssh -X user@example.com
```
Any X11 applications launched within the container will be visible on the local machine

[Read more »](/reference/forwarding){: .md-button}

## SSH keepalives

Explicit support has been added for SSH KeepAlives. Previously, keepalives received from the client would wield an unknown global command warning and flood the logs, keepalives are now handled transparently and do not generate a warning.

Additionally, support has been added to send keepalives to all clients from the server at a pre-defined interval. This can be configured with the following parameters:

```yaml
ssh:
    # The interval that keepalive messages are sent to each client, defaults to 0 which disables the feature (no keepalives are sent).
    clientAliveInterval: 10s
    # The number of unanswered keepalives before ContainerSSH considers a client unresponsive and kills the connection, defaults to 3.
    clientAliveCountMax: 3
```

This can be useful if ContainerSSH is sitting behind a load balancer which automatically kills idle connections after a pre-defined interval. A keepalive will keep the connection active as long as the client is responsive.

## Health check endpoint

A new health check service has been created that can be used with Kubernetes or loadbalancers to automatically remove unhealthy ContainerSSH instances from the pool.

[Read more »](/reference/health){: .md-button}

## Changes to the Prometheus integration

The name of some prometheus metrics and units has been altered to adhere to the convension of the metric name ending with the unit.

In detail the following metrics have been modified:

* `containerssh_auth_server_requests`:
    - Name changed to `containerssh_auth_server_requests_total`
    - Unit name change from `requests` to `requests_total`
* `containerssh_auth_server_failures`: 
    - Name changed to `containerssh_auth_server_failures_total`
    - Unit name change from `requests` to `failures_total`
* `containerssh_auth_success`: 
    - Name changed to `containerssh_auth_success_total`
    - Unit name change from `requests` to `success_total`
* `containerssh_auth_failures`:
    - Name changed to `containerssh_auth_failures_total`
    - Unit name change from `requests` to `failures_total`


* `containerssh_backend_requests`:
    - Name changed to `containerssh_backend_requests_total`
    - Unit name change from `requests` to `requests_total`
* `containerssh_backend_errors`:
    - Name changed to `containerssh_backend_errors_total`
    - Unit name change from `requests` to `errors_total`


* `containerssh_config_server_requests`:
    - Name changed to `containerssh_config_server_requests_total`
    - Unit name change from `requests` to `requests_total`
* `containerssh_config_server_failures`:
    - Name changed to `containerssh_config_server_failures_total`
    - Unit name change from `requests` to `failures_total`

* `containerssh_ssh_connections`:
    - Name changed to `containerssh_ssh_connections_total`
    - Unit name change from `connections` to `connections_total`
* `containerssh_ssh_handshake_successful`:
    - Name changed to `containerssh_ssh_successful_handshakes_total`
    - Unit name change from `handshakes` to `handshakes_total`
* `containerssh_ssh_handshake_failed`:
    - Name changed to `containerssh_ssh_failed_handshakes_total`
    - Unit name change from `handshakes` to `handshakes_total`


## Removal of the deprecated DockerRun and KubeRun backends

Following the deprecation notice in the previous versions, the dockerrun and kuberun backends have been removed. The updated [docker](/reference/docker) and [kubernetes](/reference/kubernetes) backends should be used instead.
