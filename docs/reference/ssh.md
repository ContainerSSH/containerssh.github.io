<h1>SSH configuration</h1>

SSH is the main service of ContainerSSH. It has the following configuration structure:

```yaml
ssh:
  <options>
```

The options are as follows:

| Name | Type | Description |
|------|------|-------------|
| `listen` | `string` | IP and port pair to bind the SSH service to. Defaults to `0.0.0.0:2222` |
| `serverVersion` | `string` | Server version string presented to any connecting client. Must start with `SSH-2.0-`. Defaults to `SSH-2.0-ContainerSSH`. |
| `cipher` | `[]string` | List of ciphers the server should support. See the [Ciphers](#Ciphers) section below. |
| `kex` | `[]string` | List of key exchange algorithms the server should support. See the [Key exchange](#Key exchange) section below. |
| `macs` | `[]string` | List of MAC algorithms the server should support. See the [MAC](#MAC) section below. | 
| `banner` | `[]string` | The banner text to presented to any connecting client. |
| `hostkeys` | `[]string` | List of host keys in PEM format, or file names to read the key from. |

## Configuring the server version

The SSH server version is presented to any connecting client in plain text upon connection. It has the following format:

```
SSH-2.0-softwareversion <SP> comments <CR> <LF>
```

The `softwareversion` can only contain printable US-ASCII characters without whitespace and minus (`-`) signs. The `comments` field is optional and is separated from the `softwareversion` with a single space. The maximum length of the version string is 255 characters.   

## Configuring a banner

SSH offers the ability to output a message to the clients before they enter passwords. This can be configured in the `banner` option. The banner can contain multiple lines. 

## Ciphers

ContainerSSH supports the following ciphers. The defaults are configured based on [Mozilla Modern suite](https://infosec.mozilla.org/guidelines/openssh.html).

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

## Key exchange

ContainerSSH supports the following key exchange algorithms. The defaults are configured based on [Mozilla Modern suite](https://infosec.mozilla.org/guidelines/openssh.html).

| Algorithm | Default |
|-----------|---------|
| curve25519-sha256@libssh.org | :material-check-bold: |
| ecdh-sha2-nistp521 | :material-check-bold: |
| ecdh-sha2-nistp384 | :material-check-bold: |
| ecdh-sha2-nistp256 | :material-check-bold: |
| diffie-hellman-group14-sha1 | :material-close: |
| diffie-hellman-group1-sha1 | :material-close: |

## MAC

ContainerSSH supports the following MAC algorithms. The defaults are configured based on [Mozilla Modern suite](https://infosec.mozilla.org/guidelines/openssh.html).

| Algorithm | Default |
|-----------|---------|
| hmac-sha2-256-etm@openssh.com | :material-check-bold: |
| hmac-sha2-256 | :material-check-bold: |
| hmac-sha1 | :material-close: |
| hmac-sha1-96 | :material-close: |
