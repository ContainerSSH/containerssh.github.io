<h1>Hardening ContainerSSH</h1>

ContainerSSH is built to secure its inner workings as much as possible. You can take several steps to secure it further.

## Running ContainerSSH

ContainerSSH should be run as an unprivileged user (e.g. root) as it does not need access to any privileged resources. When running it from the default container image `containerssh/containerssh` this is the default.

When running it outside a container you should keep the default bind port of 2222. On Linux you can then use iptables to redirect port 22 to the unprivileged port:

```
iptables -t nat -I PREROUTING -p tcp --dport 22 -j REDIRECT --to-port 2222
```

Don't forget to add this rule to your persistent firewall configuration.

## Securing authentication

### Authentication server connection

ContainerSSH talks to an authentication server over HTTP. There are two potential attacks here:

1. If an attacker can intercept the connection between ContainerSSH and the authentication server the attacker can read the passwords for password authentication.
2. If an attacker can send requests to the authentication server they can brute force SSH passwords.

Therefore, the connection between ContainerSSH and the authentication server should be secured in the following 3 ways:

1. Implement firewalls such that only ContainerSSH can access the authentication server.
2. Only use HTTPS with certificate verification to access the authentication server and disable the HTTP port.
3. Deploy client certificates to prevent unauthorized access to the authentication server.

To maximize security it is recommended that you deploy a custom CA for the server and client certificates. The details of deploying a CA infrastructure with cfssl are described in the [authentication chapter](auth.md).

### Rate limiting

ContainerSSH contains no rate limiting for authentication across connections, this is the job of the authentication server. The number of authentication attempts within a connection is limited to 6.

The authentication server must take care to do rate limiting right: within a single connection multiple authentication attempts may be made and if the authentication server returns a non-200 response code ContainerSSH will retry connections.

It is recommended that the authentication server use the `connectionId` field to distinguish between SSH connections as this field is guaranteed to be unique for a connection.

### Client credential security

Passwords are vulnerable to being stolen and cannot be transferred to hardware keys. For the most security it is recommended to disable password authentication and only use SSH keys.

When storing SSH keys on the client computer they should be protected by a passphrase and limited permissions on the key file. 

If possible, however, SSH keys should be transferred to a hardware token like the [Yubikey](https://developers.yubico.com/PGP/SSH_authentication/). The Yubikey should be configured to require a physical touch on every authentication and should be unlocked with a passcode to prevent unauthorized applications on the client accessing the key for connections.

## Securing the configuration server

ContainerSSH can optionally reach out to a configuration server to fetch dynamic backend configuration based on the username. The backend configuration may contain secrets, such as certificates for accessing Docker and Kubernetes, or application-specific secrets. Therefore, if an attacker can access the configuration server they can extract secrets from the returned configuration.

This can be mitigated similar to the authentication server:

1. Implement firewalls such that only ContainerSSH can access the configuration server.
2. Only use HTTPS with certificate verification to access the configuration server and disable the HTTP port.
3. Deploy client certificates to prevent unauthorized access to the configuration server.

To maximize security it is recommended that you deploy a custom CA for the server and client certificates. The details of deploying a CA infrastructure with cfssl are described in the [configuration server chapter](configserver.md).

## Limiting SSH requests

The [security module](security.md) provides the ability to limit which requests are allowed from a client. As ContainerSSH is upgraded the default is to allow new features that will come in with future releases (e.g. TCP port forwarding).

In order to secure ContainerSSH for future releases it is recommended 

## Securing Docker

Docker-specific settings for security are described in the [Docker documentation](docker.md). 

## Securing Kubernetes

Kubernetes-specific settings for security are described in the [Kubernetes documentation](docker.md).