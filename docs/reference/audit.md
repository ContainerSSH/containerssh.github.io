---
image: images/auditlog-asciinema.jpg
---

<h1>Audit logging {{ upcoming("0.4.0") }}</h1>

!!! warning
    This is a feature still in development and is available in [0.4.0 Preview Release 1](https://github.com/ContainerSSH/ContainerSSH/releases/tag/0.4.0-PR1)

ContainerSSH contains an audit logging facility that can log every interaction happening over SSH. This functionality is disabled by default as it has serious security and privacy implications, as well as severe resource requirements.

Audit logging can be enabled in the configuration using the following structure:

```yaml
audit:
  format: none|audit|asciinema # Which format to log in. Defaults to none.
  storage: none|s3|file        # Where to write audit log. Defaults to none.
  intercept:
    stdin: true|false          # Intercept keystrokes from user
    stdout: true|false         # Intercept standard output
    stderr: true|false         # Intercept standard error
    passwords: true|false      # Intercept passwords during authentication
```

Audit logging is a powerful tool. It can capture the following events.

- Connections
- Authentication attempts, optionally with credentials
- Global and channel-specific SSH requests
- Programs launched from SSH
- Input from the user (optional)
- Output and errors to the user (optional)

The events recorded depend on the chosen format. With the `audit` format all information is recorded with nanosecond timing, so events can be accurately reconstructed after the fact.

## About interceptions

The `intercept` options give you a wide range of options when it comes to detailed logging of actions by users. You may want to, for example, enable `stdout` logging while keeping `stdin` disabled to avoid accidentally capturing passwords typed into the console.

However, this approach may fail if SFTP is enabled as you will fail to capture binaries uploaded to the server. Audit logging should therefore be enjoyed with great care and the logs should always be stored on an encrypted storage device.

## Log formats

### The `audit` format (recommended)

The audit format is intended for an accurate reconstruction of everything happening during an SSH session. It allows for accurate reconstruction of what happened during the session.

Audit logs are stored in a [compressed binary format](https://github.com/ContainerSSH/auditlog/blob/main/FORMAT.v1.md) and can be decoded to a series of JSON messages using the `containerssh-auditlog-decoder` supplied as part of the ContainerSSH release. Alternatively, you can [implement your own decoder](https://github.com/ContainerSSH/auditlog/blob/main/FORMAT.v1.md).

### The `asciinema` format

The [asciinema format](https://github.com/asciinema/asciinema/blob/develop/doc/asciicast-v2.md) stores logs in a format suitable for replay in the [Asciinema player](https://asciinema.org/).

<script id="asciicast-vMhS8fMI6tyICWdcszMvKQVFU" src="https://asciinema.org/a/vMhS8fMI6tyICWdcszMvKQVFU.js" async></script>

!!! note
    Make sure you enable the `stdout` and `stderr` interceptions otherwise the `asciinema` encoder won't capture anything. 

!!! warning
    Asciinema is intended for entertainment purposes only and doesn't store all relevant information required for an accurate audit log.

## Storage backends

### The `s3` storage (recommended)

The S3 storage sends the logs to an S3-compatible object storage for long term storage. This is the recommended way of storing audit logs because it is a server-independent storage device that supports permissions.

The S3 storage stores the logs in a local directory and uploads them once an upload part is full (default: 5MB) or the connection closes. If the upload fails, ContainerSSH will retry the upload as soon as possible. If ContainerSSH is stopped and restarted it will attempt to upload the audit logs still in the local directory, but no guarantee is made that these logs will not be corrupt after a crash.

!!! warning
    The local directory should be stored on a persistent storage and must not be shared between ContainerSSH instances. It must be large enough to host *all* sessions in their entirety that are currently running. When IO interception is enabled and your users are downloading or uploading large amounts of data this can run you up to several GB of storage needed locally. We recommend turning off IO interception for cases where large amounts of data are being transferred.  

The S3 storage can be configured as follows:

```yaml
audit:
  storage: s3
  s3:
    local: /local/storage/directory
    accessKey: "your-access-key-here"
    secretKey: "your-secret-key-here"
    bucket: "your-existing-bucket-name-here"
    region: "your-region-name-here"
    endpoint: "https://your-custom-s3-url" # Optional
    uploadPartSize: 5242880 # In bytes, min: 5MB, max: 5GB
    acl: "public-read" # Optional, in case you want to set an ACL
    metadata:
      username: true # Expose username via S3 metadata. Defaults to false.
      ip: true # Expose IP address via S3 metadata. Defaults to false.
    cacert: | # Optional
      Your trusted CA certificate in PEM format here for your S3 server.
```

!!! tip
    You can restrict the access key permissions to `PutObject`, `CreateMultipartUpload`, `UploadPart`, `CompleteMultipartUpload`, `ListMultipartUploads`, and `AbortMultipartUpload`. Other permissions are not required.

!!! tip
    You may also want to investigate if your S3 provider supports WORM / object locking, object lifecycles, or server side encryption for compliance.

### The `file` storage

The file storage writes audit logs to files on the disk. The storage location can be configured using the following option:

```yaml
audit:
  type: file
  file:
    directory: /var/log/audit
```
