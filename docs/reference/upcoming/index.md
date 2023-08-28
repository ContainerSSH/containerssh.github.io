title: ContainerSSH 0.5.0 Reference Manual

<h1>ContainerSSH 0.5.0 Reference Manual</h1>

{{ reference_upcoming() }}

The Reference Manual provides reference material for ContainerSSH 0.4 and is oriented towards system operators wishing to use ContainerSSH on their system.

## Introduction

This manual contains documentation on how to set up, configure, monitor, and secure the ContainerSSH installation. If you need a one-minute primer on how ContainerSSH works please [watch this video](https://www.youtube.com/watch?v=Cs9OrnPi2IM).

## Changes since ContainerSSH 0.4.1

ContainerSSH 0.5.0 is a feature and bugfix release. The reference manual for the older ContainerSSH 0.4.1 is [available here](../index.md). This release adds two main new features:

1. OAuth2 and Kerberos authentication
2. Authorization webhook
3. Passing metadata from authentication to configuration servers and backends
4. Deploying files into the containers from the authentication and configuration hooks 
5. Passing SSH certificate information to the authentication webhook
6. X11 forwarding
7. SSH keepalives
8. Health check endpoint
9. Bugfixes to the Prometheus integration
10. Removed the deprecated DockerRun and KubeRun backends

## OAuth2 and Kerberos authentication

The biggest change of this release is support for multiple authentication backends. Thanks to our contributors we now have support for OAuth2 and Kerberos authentication.

OAuth2 authentication works with GitHub and any OIDC-compliant authentication server, such as Keycloak and Microsoft Active Directory Federation Services. We have actively worked with several SSH client vendors to make this authentication method work and we are happy to report that it works in OpenSSH, PuTTY, Filezilla, WinSCP, and more. The authenticaiton prompts the user to click on a link in their SSH client and then log in via their normal browser-based flow. What's more, you can automatically expose the GitHub or OIDC token to the container. Your users can directly use their credentials in your ContainerSSH environment.

Similarly, Kerberos authentication is also useful in an enterprise setting. When users are logged in to their personal devices using company credentials, they will now be able to automatically log in to ContainerSSH with Kerberos. Optionally, users can also log in to ContainerSSH from a non-authenticated device using username and password, and ContainerSSH will automatically create a Kerberos ticket for them. This ticket is available in the container directly, so your users can work with their Kerberos credentials without any additional steps.

[Read more »](auth.md){: .md-button}

## Authorization webhook

As part of our authentication and authorization overhaul we added a separate webhook. This webhook lets you match up the username entered in SSH and the authenticated credentials in a separate step. You can, for example, authenticate a user from Kerberos and then use a webhook to match up their Kerberos identity with the SSH username. 

[Read more »](auth.md){: .md-button}

## Metadata handling and passing

## Deploying files

## SSH certificate information

## Port, socket and X11 forwarding

From this release support for forward and reverse port forwarding is supported natively. For these features the ContainerSSH agent has to be anbled as the agent acts as the entry & exit points of the connections inside the container.

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

[Read more »](forwarding.md){: .md-button}

## SSH keepalives

Explicit support has been added for SSH KeepAlives. Previously, keepalives received from the client would wield an unknown global command warning and flood the logs, keepalives are now handled transparently and do not generate a warning.

Additionally, support has been added to send keepalives to all clients from the server at a pre-defined interval. This can be configured with the following parameters:

```yaml
ssh:
    // The interval that keepalive messages are sent to each client, defaults to 0 which disables the feature (no keepalives are sent).
    clientAliveInterval: 10s
    // The number of unanswered keepalives before ContainerSSH considers a client unresponsive and kills the connection, defaults to 3.
    clientAliveCountMax: 3
```

This can be useful if ContainerSSH is sitting behind a load balancer which automatically kills idle connections after a pre-defined interval. A keepalive will keep the connection active as long as the client is responsive.

## Health check endpoint

A new health check service has been created that can be used with Kubernetes or loadbalancers to automatically remove unhealthy ContainerSSH instances from the pool.

[Read more »](health.md){: .md-button}

## Bugfixes to the Prometheus integration

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

Following the deprecation notice in the previous versions, the dockerrun and kuberun backends have been removed. The updated [docker](./docker.md) and [kubernetes](./kubernetes.md) backends should be used instead.
