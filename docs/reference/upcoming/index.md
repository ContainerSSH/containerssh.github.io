title: ContainerSSH 0.5.0 Reference Manual

<h1>ContainerSSH 0.5.0 Reference Manual</h1>

{{ reference_upcoming() }}

The Reference Manual provides reference material for ContainerSSH 0.4 and is oriented towards system operators wishing to use ContainerSSH on their system.

## Introduction

This manual contains documentation on how to set up, configure, monitor, and secure the ContainerSSH installation. If you need a one-minute primer on how ContainerSSH works please [watch this video](https://www.youtube.com/watch?v=Cs9OrnPi2IM).

## Changes since ContainerSSH 0.4.1

ContainerSSH 0.5.0 is a feature and bugfix release. The reference manual for the older ContainerSSH 0.4.1 is [available here](../index.md). This release adds two main new features:

1. oAuth2 and Kerberos authentication
2. Authorization webhook
3. Passing metadata from authentication to configuration servers and backends
4. Deploying files into the containers from the authentication and configuration hooks 
5. Passing SSH certificate information to the authentication webhook
6. X11 forwarding
7. SSH keepalives
8. Health check endpoint
9. Bugfixes to the Prometheus integration
10. Removed the deprecated DockerRun and KubeRun backends

## oAuth2 and Kerberos authentication

The biggest change of this release is support for multiple authentication backends. Thanks to our contributors we now have support for oAuth2 and Kerberos authentication.

oAuth2 authentication works with GitHub and any OIDC-compliant authentication server, such as Keycloak and Microsoft Active Directory Federation Services. We have actively worked with several SSH client vendors to make this authentication method work and we are happy to report that it works in OpenSSH, PuTTY, Filezilla, WinSCP, and more. The authenticaiton prompts the user to click on a link in their SSH client and then log in via their normal browser-based flow. What's more, you can automatically expose the GitHub or OIDC token to the container. Your users can directly use their credentials in your ContainerSSH environment.

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

## Health check endpoint

## Bugfixes to the Prometheus integration

## Removal of the deprecated DockerRun and KubeRun backends