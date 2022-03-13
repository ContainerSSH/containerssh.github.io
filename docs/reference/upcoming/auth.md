title: Authentication

<h1>Authentication</h1>

{{ reference_upcoming() }}

ContainerSSH does not have a built-in user database. It needs to use external services to verify user credentials, such
as a webhook, oAuth2, or Kerberos. This page describes what authentication methods ContainerSSH supports and how you can
tie them to your external authentication databases.

## SSH authentication methods

This section gives a brief explanation on SSH authentication. In all authentication cases the SSH client may prompt the
user for a username.

### Password authentication

When the SSH client requests a password authentication it will prompt the user for a password and submit it to the SSH
server. The SSH server will then verify the password. In contrast to keyboard-interactive authentication (see below)
there is no way to customize the password prompt.

### Public key authentication

In case of public key authentication the client has a cryptographic key. The public component of the cryptographic key
is submitted to the server. The client signs this public key with its private key, so the server can verify that the
client indeed holds the corresponding key. ContainerSSH can then verify if the public key belongs to the username
that has been submitted.

Additionally, you can sign these keys with an SSH certificate authority. Using certificate authorities simplify the
key management since you do not have to put every single key in your database, having the CA certificate only is enough.

Be warned though, the SSH certificate authority is **not** the same as the certificate authorities you may be used to
from configuring a webserver. (x509 certificates) SSH certificate authorities are a lot simpler and do not have the same
capabilities as x509 authorities. They do not provide the ability to chain certificates, and they also don't provide a 
built-in mechanism for certificate revocation other than the expiration date of the certificate.

### Keyboard-interfactive authentication

At first glance keyboard-interactive authentication is very similar to password authentication. However, with this
method the SSH server can provide customized questions to the client, to which the user has to provide answers. There
can also be multiple consecutive questions and answers.

### GSSAPI

GSSAPI is a cryptographic authentication method that is embedded into the SSH encryption itself. It is mainly used as
part of Kerberos authentication. This is often used in corporate systems to auto-login users.

## Authentication backends supported by ContainerSSH

ContainerSSH supports a number of authentication backends. The table below summarizes which integration supports
which SSH authentication method. You can configure multiple backends in parallel, but one SSH authentication
method is always tied to one backend.

| SSH authentication method | Webhook               | oAuth2                | Kerberos              |
|---------------------------|-----------------------|-----------------------|-----------------------|
| Password                  | :material-check-bold: | :material-close:      | :material-check-bold: |
| Public key                | :material-check-bold: | :material-close:      | :material-close:      |
| Keyboard-interactive      | :material-close:      | :material-check-bold: | :material-close:      |
| GSSAPI                    | :material-close:      | :material-close:      | :material-check-bold: |

## Configuration

You can configure the authentication with the following options:

```yaml
auth:
  password:
    method: ""|webhook|kerberos
    webhook: 
      <webhook options>
    kerberos:
      <kerberos options>
  publicKey:
    method: ""|webhook
    webhook: 
      <webhook options>
  keyboardInteractive:
    method: ""|oauth2
    oauth2: 
      <oauth2 options>
  gssapi:
    method: ""|kerberos
    kerberos:
      <kerberos options>
```

### Detailed configuration options

- [Webhook configuration options](auth-webhook.md)
- [oAuth2 configuration options](auth-oauth2.md)
- [Kerberos configuration options](auth-kerberos.md)
