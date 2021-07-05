{{ reference_outdated() }}

<h1>Metrics</h1>

ContainerSSH contains a [Prometheus](https://prometheus.io/)-compatible metrics server which can be enabled using the following configuration:

```yaml
metrics:
  <options here>
```

The metrics server has the following options:

| Option | Type | Description |
|--------|------|-------------|
| `enable` | `bool` | Enable metrics server. Defaults to false. |
| `path` | `string` | HTTP path to serve metrics on. Defaults to `/metrics`. |
| `listen` | `string` | IP and port to listen on. Defaults to `0.0.0.0:9100`. |
| `clientcacert` | `string` | CA certificate in PEM format or filename that contains the CA certificate used for authenticating connecting clients. |
| `cert` | `string` | Client certificate in PEM format or filename that contains the server certificate. |
| `key` | `string` | Private key in PEM format or filename that contains the server certificate. |
| `tlsVersion` | `[]string` | Minimum TLS version to support. See the [TLS version](#tls-version) section below. |
| `curve` | `[]string` | Elliptic curve algorithms to support. See the [Elliptic curve algorithms](#elliptic-curve-algorithms) section below. |
| `cipher` | `[]string,string` | Which cipher suites to support. See the [Cipher suites](#cipher-suites) section below. |

## Available metrics

You can configure Prometheus to grab the following metrics:

`containerssh_auth_server_failures`
: Number of failed requests to the authentication server since start.

`containerssh_auth_success`
: Number of successful authentications since start. Contains labels for `authtype` (`password` or `pubkey`) and `country` (see below).

`containerssh_auth_failures`
: Number of failed authentications since start. Contains labels for `authtype` (`password` or `pubkey`) and `country` (see below).

`containerssh_config_server_failures`
: Number of failed requests to the configuration server since start.

`containerssh_ssh_connections`
: Number of SSH connections since start. Contains a label for `country` (see below).

`containerssh_ssh_handshake_successful`
: Number of successful SSH handshakes since start. Contains a label for `country` (see below).

`containerssh_ssh_handshake_failed`
: Number of failed SSH handshakes since start. Contains a label for `country` (see below).

`containerssh_ssh_current_connections`
: Number of currently open SSH connections. Contains a label for `country` (see below).

## Country identification

Country identification works using [GeoIP2 or GeoLite2 from MaxMind](https://www.maxmind.com/en/geoip2-services-and-databases). This database needs to be provided to ContainerSSH externally due to licensing concerns.

The default path for the GeoIP database is `/var/lib/GeoIP/GeoIP2-Country.mmdb`, but you can change that using the following configuration snippet:

```yaml
geoip:
  provider: "maxmind"
  maxmind-geoip2-file: '/var/lib/GeoIP/GeoIP2-Country.mmdb'
```

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
| TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256 | :material-check-bold: |
| TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 | :material-check-bold: |
| TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384 | :material-close: |
| TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384 | :material-close: |
| TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305 | :material-close: |
| TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305 | :material-close: |

## Client authentication

In order to safeguard the metrics ContainerSSH supports authenticating connecting clients using x509 mutual TLS authentication. For this you will need to generate a CA certificate and configure the metrics service with it, as well as client certificates that your connecting clients must use.

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

The resulting `ca.pem` should be added to the metrics configuration:

```yaml
metrics:
  clientcacert: /path/to/ca.pem
```

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

The resulting `containerssh.pem` and `containerssh-key.pem` can be used in your connecting client. For an example see the [Prometheus documentation](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#tls_config).