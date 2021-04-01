# The SSH proxy backend

The SSH proxy backend does not launch containers, instead it connects to a second SSH server and forwards the connections to that backend.

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

Read more in the [SSH proxy reference manual &raquo;](../reference/sshproxy.md)