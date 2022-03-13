---
title: HTTP and TLS configuration
---

{{ reference_upcoming() }}

ContainerSSH can act as a HTTP server in the following roles:

- [Metrics server](metrics.md)
- [OAuth2 redirect page](auth-oauth2.md)

It can also act as a HTTP client in the following scenarios:

- [Authentication webhook](auth-webhook.md)
- [Configuration webhook](configserver.md)

This page describes how to configure ContainerSSH for secure HTTP communication in these roles.

## HTTP server configuration

All HTTP servers in ContainerSSH have the following options. They may have additional options depending on their context, see the individual module documentation for details.

| Option | Type | Description |
|--------|------|-------------|
| `listen` | `string` | IP and port to listen on. |
| `clientcacert` | `string` | CA certificate in PEM format or filename that contains the CA certificate used for authenticating connecting clients.  See the [Mutual TLS authentication](#mutual-tls-authentication) section below. |
| `cert` | `string` | Client certificate in PEM format or filename that contains the server certificate. |
| `key` | `string` | Private key in PEM format or filename that contains the server certificate. |
| `tlsVersion` | `[]string` | Minimum TLS version to support. See the [TLS version](#tls-version) section below. |
| `curve` | `[]string` | Elliptic curve algorithms to support. See the [Elliptic curve algorithms](#elliptic-curve-algorithms) section below. |
| `cipher` | `[]string,string` | Which cipher suites to support. See the [Cipher suites](#cipher-suites) section below. |

## HTTP client configuration

All HTTP clients have the following options. They may have additional options depending on their context, see the individual module documentation for details.

| Name | Type   | Description |
|------|--------|-------------|
| `url`  | `string` | HTTP URL of the server to call. |
| `timeout` | `string` | Timeout for the call. Can be provided with time units (e.g. `6s`), defaults to nanoseconds if provided without a time unit. |
| `cacert` | `string` | CA certificate in PEM format or filename that contains the CA certificate. This is field is required for `https://` URL's on Windows because of Golang issue [#16736](https://github.com/golang/go/issues/16736) |
| `cert` | `string` | Client certificate in PEM format or filename that contains the client certificate for x509 authentication with the configuration server. See the [Mutual TLS authentication](#mutual-tls-authentication) section below. |
| `key` | `string` | Private key in PEM format or filename that contains the client certificate for x509 authentication with the configuration server.  See the [Mutual TLS authentication](#mutual-tls-authentication) section below. |
| `tlsVersion` | `[]string` | Minimum TLS version to support. See the [TLS version](#tls-version) section below. |
| `curve` | `[]string` | Elliptic curve algorithms to support. See the [Elliptic curve algorithms](#elliptic-curve-algorithms) section below. |
| `cipher` | `[]string,string` | Which cipher suites to support. See the [Cipher suites](#cipher-suites) section below. |
| `allowRedirects` | `bool` | Allow following HTTP redirects. Defaults to false. |

## TLS version

The minimum supported TLS version can be configured using the `tlsVersion` option. It defaults to `1.3` and also supports `1.2`. Versions lower than `1.2` are not supported. Server certificates *must* use Subject Alternative Names (SAN's) for proper server verification.

## Elliptic curve algorithms

The elliptic curve algorithms can be specified in the `curve` option. We support and default to the following options:

- `x25519`
- `secp256r1`
- `secp384r1`
- `secp521r1`

## Cipher suites

The following cipher suites are supported in ContainerSSH:

| Suite | Default |
|-------|---------|
| TLS_AES_128_GCM_SHA256 | :material-check-bold: |
| TLS_AES_256_GCM_SHA384 | :material-check-bold: |
| TLS_CHACHA20_POLY1305_SHA256 | :material-check-bold: |
| TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256 | :material-check-bold: |
| TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 | :material-check-bold: |
| TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384 | :material-close: |
| TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384 | :material-close: |
| TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305 | :material-close: |
| TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305 | :material-close: |

!!! tip
    Cipher suites can be provided as a list or as a colon (`:`) separated string.

## Mutual TLS authentication

If ContainerSSH is acting as a HTTP client it can authenticate itself with the HTTPS server using mutual TLS authentication. Conversely, when ContainerSSH is acting as a HTTPS server it can authenticate clients using mutual TLS authentication.

To create a CA infrasturcture for this authentication we recommend using [cfssl](https://github.com/cloudflare/cfssl). First we need to create the CA certificates:

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

The resulting ca.pem file can be used on the server side as a CA certificate for clients. If ContainerSSH is the server the certificate can be added in the `clientcacert` field.

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

The resulting `containerssh.pem` and `containerssh-key.pem` can be used in the connecting client. If ContainerSSH is the client these files can be added to the `cert` and `key` fields, respectively.
