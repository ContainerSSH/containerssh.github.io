
{{ reference_upcoming() }}

<h1>The SSH proxy backend</h1>

The SSH proxy backend does not launch containers, instead it connects to a second SSH server and forwards the connections to that backend. This allows for using the [audit log](audit.md) to inspect SSH traffic, or to dynamically forwarding connections using the [configuration webhook](configserver.md).

## The base configuration structure

The minimum configuration is the following:

```yaml
backend: sshproxy
sshproxy:
  # Add the backend server here
  server: 127.0.0.1
  # Set the following option to true to reuse the connecting user's username.
  usernamePassThrough: true
  # Or specify a username manually
  username: root
  # Specify the password
  password: changeme
  # Or the private key. This can reference a file or be added directly.
  privateKey: |
    -----BEGIN OPENSSH PRIVATE KEY-----
    ...
  # Provide all fingerprints of the backing SSH server's host keys:
  allowedHostKeyFingerprints:
    - SHA256:...
```

!!! tip
    You can obtain the fingerprints of OpenSSH host keys by running the following script:
    ```
    for i in /etc/ssh/ssh_host_*.pub; do ssh-keygen -l -f $i; done | cut -d ' ' -f
 2
    ```

!!! warning
    ContainerSSH does not support passing through password or private key to the backing server. We recommend setting up a private-public key authentication for the backing server.
    
## Configuration options

| Option | Type | Description |
|--------|------|-------------|
| `server` | `string` | Host name or IP address of the backing SSH server. Required. |
| `port` | `uint16` | Port number of the backing SSH service. Defaults to 22. |
| `usernamePassThrough` | `bool` | Take username from the connecting client. |
| `username` | `string` | Explicitly set the username to use for the backing connection. Required if `usernamePassThrough` is `false`. |
| `password` | `string` | Password to use to authenticate with the backing SSH server. |
| `privateKey` | `string` | Private key to use to authenticate with the backing SSH server. Can be a reference to a file or the private key in PEM or OpenSSH format. |
| `allowedHostKeyFingerprints` | `[]string` | List of SHA256 fingerprints of the backing SSH server. |
| `ciphers` | `[]string` | List of SSH ciphers to use. See [Ciphers](#ciphers) below. |
| `kex` | `[]string` | List of key exchange algorithms to use. See [Key exchange algorithms](#key-exchange-algorithms) below. |
| `macs` | `[]string` | List of MAC algorithms to use. See [MAC algorithms](#mac-algorithms) below. |
| `hostKeyAlgorithms` | `[]string` | List of host key algorithms to request from the backing server. See [Host key algorithms](#host-key-algorithms) below. |
| `timeout` | `string` | Timeout for connecting / retrying the SSH connection. |
| `clientVersion` | `string` | Client version string to send to the backing server. Must be in the format of `SSH-protoversion-softwareversion SPACE comments`"`. See [RFC 4235 section 4.2. Protocol Version Exchange](https://tools.ietf.org/html/rfc4253#page-4) for details. The trailing CR and LF characters should NOT be added to this string. |

## Ciphers

ContainerSSH supports the following ciphers for contacting the backing server.  The defaults are configured based on [Mozilla Modern suite](https://infosec.mozilla.org/guidelines/openssh.html).

| Algorithm | Default |
|-----------|---------|
| chacha20-poly1305@openssh.com | :material-check-bold: |
| aes256-gcm@openssh.com | :material-check-bold: |
| aes128-gcm@openssh.com | :material-check-bold: |
| aes256-ctr | :material-check-bold: |
| aes192-ctr | :material-check-bold: |
| aes128-ctr | :material-check-bold: |
| aes128-cbc | :material-close: |
| arcfour256 | :material-close: |
| arcfour128 | :material-close: |
| arcfour | :material-close: |
| tripledescbcID | :material-close: |

## Key exchange algorithms

ContainerSSH supports the following key exchange algorithms for contacting the backing server. The defaults are configured based on [Mozilla Modern suite](https://infosec.mozilla.org/guidelines/openssh.html).

| Algorithm | Default |
|-----------|---------|
| curve25519-sha256@libssh.org | :material-check-bold: |
| ecdh-sha2-nistp521 | :material-check-bold: |
| ecdh-sha2-nistp384 | :material-check-bold: |
| ecdh-sha2-nistp256 | :material-check-bold: |
| diffie-hellman-group14-sha1 | :material-close: |
| diffie-hellman-group1-sha1 | :material-close: |

## MAC algorithms

ContainerSSH supports the following MAC algorithms for contacting the backing server. The defaults are configured based on [Mozilla Modern suite](https://infosec.mozilla.org/guidelines/openssh.html).

| Algorithm | Default |
|-----------|---------|
| hmac-sha2-256-etm@openssh.com | :material-check-bold: |
| hmac-sha2-256 | :material-check-bold: |
| hmac-sha1 | :material-close: |
| hmac-sha1-96 | :material-close: |

## Host key algorithms

ContainerSSH supports the following host key algorithms for verifying the backing server identity.

| Algorithm | Default |
|-----------|---------|
| ssh-rsa-cert-v01@openssh.com | :material-close: |
| ssh-dss-cert-v01@openssh.com | :material-close: |
| ecdsa-sha2-nistp256-cert-v01@openssh.com | :material-close: |
| ecdsa-sha2-nistp384-cert-v01@openssh.com | :material-close: |
| ecdsa-sha2-nistp521-cert-v01@openssh.com | :material-close: |
| ssh-ed25519-cert-v01@openssh.com | :material-close: |
| ssh-rsa | :material-close: |
| ssh-dss | :material-close: |
| ssh-ed25519 | :material-close: |