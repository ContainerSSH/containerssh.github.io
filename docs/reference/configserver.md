---
title: Configuration server
---

<h1>Configuration Server</h1>

ContainerSSH has the ability to configure the backend and the launched container dynamically based on the username and/or IP address. To do this ContainerSSH calls out to a configuration server if configured.

## Configuration

The configserver webhook can be configured in the main configuration using the following structure:

```yaml
configuration:
  <options>
```

The following options are supported:

| Name | Type   | Description |
|------|--------|-------------|
| `url`  | `string` | HTTP URL of the configuration server to call. Leaving this field empty disables the webhook. |
| `timeout` | `string` | Timeout for the webhook. Can be provided with time units (e.g. `6s`), defaults to nanoseconds if provided without a time unit. |
| `cacert` | `string` | CA certificate in PEM format or filename that contains the CA certificate. This is field is required for `https://` URL's on Windows because of Golang issue [#16736](https://github.com/golang/go/issues/16736) |
| `cert` | `string` | Client certificate in PEM format or filename that contains the client certificate for x509 authentication with the configuration server. |
| `key` | `string` | Private key in PEM format or filename that contains the client certificate for x509 authentication with the configuration server. |
| `tlsVersion` | `string` | Minimum TLS version to support. See the [TLS version](#tlsversion) section below. |
| `curve` | `string` | Elliptic curve algorithms to support. See the [Elliptic curve algorithms](#ellipticcurvealgoritms) section below. |
| `cipher` | `[]string` | Which cipher suites to support. See the [Cipher suites](#ciphersuites) section below. |

## Configuring TLS

TLS ensures that the connection between ContainerSSH and the configuration server cannot be intercepted using a Man-in-the-Mittle attack. We recommend checking the [Mozilla Wiki](https://wiki.mozilla.org/Security/Server_Side_TLS) for information about which configuration can be considered secure.

### TLS version

The minimum supported TLS version can be configured using the `tlsVersion` option. It defaults to `1.3` and also supports `1.2`. Versions lower than `1.2` are not supported.

### Elliptic curve algorithms

The elliptic curve algorithms can be specified in the `curve` option. We support and default to the following options:

- `x25519`
- `secp256r1`
- `secp384r1`
- `secp521r1`

### Cipher suites

The following cipher suites are supported in ContainerSSH:

| Suite | Default |
|-------|---------|
| TLS_AES_128_GCM_SHA256 | :material-check-bold: |
| TLS_AES_256_GCM_SHA384 | :material-check-bold: |
| TLS_CHACHA20_POLY1305_SHA256 | :material-check-bold: |
| TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256 | :material-close: |
| TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 | :material-close: |
| TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384 | :material-close: |
| TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384 | :material-close: |
| TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305 | :material-close: |
| TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305 | :material-close: |

## Client authentication

In order to safeguard secrets in the configuration the configuration server should be protected by either firewalling it appropriately, but it is better to use x509 client certificates as a means of authentication.

We recommend using [cfssl](https://github.com/cloudflare/cfssl) for creating the CA infrastructure. First we need to create the CA certificates:

```bash
cat > ca-config.json <<EOF
{
  "signing": {
    "default": {
      "expiry": "8760h"
    },
    "profiles": {
      "containerssh": {
        "usages": ["signing", "key encipherment", "server auth", "client auth"],
        "expiry": "8760h"
      }
    }
  }
}
EOF

cat > ca-csr.json <<EOF
{
  "CN": "ContainerSSH CA",
  "key": {
    "algo": "rsa",
    "size": 4096
  },
  "names": [
    {
      "C": "Your Country Code",
      "L": "Your Locality",
      "O": "Your Company",
      "OU": "",
      "ST": "Your State"
    }
  ]
}
EOF

cfssl gencert -initca ca-csr.json | cfssljson -bare ca
```

The resulting `ca.pem` should be added as a client CA in your configuration server. This CA does *not* have to be the same used to sign the *server* certificate.

Then we can create the client certificate:

```bash
cat > containerssh-csr.json <<EOF
{
  "CN": "ContainerSSH",
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "Your Country Code",
      "L": "Your Locality",
      "O": "Your Company",
      "OU": "",
      "ST": "Your State"
    }
  ]
}
EOF

cfssl gencert \
  -ca=ca.pem \
  -ca-key=ca-key.pem \
  -config=ca-config.json \
  -profile=containerssh \
  containerssh-csr.json | cfssljson -bare containerssh
```

The resulting `containerssh.pem` and `containerssh-key.pem` should then be added to the configuration as client credentials:

```yaml
configuration:
  cert: /path/to/containerssh.pem
  key: /path/to/containerssh-key.pem
```

## The configuration webhook

The configuration webhook is a simple JSON `POST` request to which the server must respond with a JSON response.

!!! note
    We have an [OpenAPI document](../api/authconfig) available for the authentication and configuration server. You can check the exact values available there, or use the OpenAPI document to generate parts of your server code.

The config server will receive a request in following format:

```json
{
  "username":"ssh username",
  "connectionId": "ssh session ID"
}
```

The configuration server will have to respond with the following response accompanied with the content type of `application/json`. 

```json
{
  "config": {
    // Provide a partial configuration here 
  }
}
```

The configuration JSON structure is identical to the YAML described in this reference manual and the full configuration can be dumped by running `./containerssh --dump-config`. The server is free to return only partial options that it wants to set. Any options that are sent overwrite the ones from the configuration file.

Currently only the following options can be set from the configuration server:

- [Backend](backends.md)
- [Docker](docker.md)
- [Kubernetes](kubernetes.md)
- [DockerRun](dockerrun.md)
- [KubeRun](kuberun.md)
- [Security](security.md)

!!! tip
    We provide a [Go library to implement a config server](https://github.com/containerssh/configuration).