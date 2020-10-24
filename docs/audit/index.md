<h1>Audit logging {{ upcoming("0.4.0") }}</h1>

ContainerSSH contains an audit logging facility that can log every interaction happening over SSH. This functionality is disabled by default as it has serious security and privacy implications, as well as severe resource requirements.

Audit logging can be enabled in the configuration using the following structure:

```yaml
audit:
  type: none|s3|file|log  # Which audit logger to use. Defaults to none.
  intercept:
    stdin: true|false     # Intercept keystrokes from user
    stdout: true|false    # Intercept standard output
    stderr: true|false    # Intercept standard error
    passwords: true|false # Intercept passwords during authentication
```

Audit logs can be decoded to a series of JSON messages using the `containerssh-auditlog-decoder` supplied as part of the ContainerSSH release. Alternatively, you can [implement your own decoder](format.md).

## About interceptions

The `intercept` options give you a wide range of options when it comes to detailed logging of actions by users. You may want to, for example, enable `stdout` logging while keeping `stdin` disabled to avoid accidentally capturing passwords typed into the console.

However, this approach may fail if SFTP is enabled as you will fail to capture binaries uploaded to the server. Audit logging should therefore be enjoyed with great care and the logs should always be stored on an encrypted storage device.

## The "s3" audit logger (recommended)

The S3 audit logger encodes the audit logs and sends them to an S3-compatible object storage for long term storage. This is the recommended way of storing audit logs because it is a server-independent storage device that supports permissions. You may also want to investigate if your S3 provider supports WORM / object locking, object lifecycles, or server side encryption for compliance.

The S3 audit logger can be configured as follows:

```yaml
audit:
  type: s3
  s3:
    accessKey: "your-access-key-here"
    secretKey: "your-secret-key-here"
    bucket: "your-existing-bucket-name-here"
    region: "your-region-name-here"
    endpoint: "https://your-custom-s3-url" # Optional
    cacert: | # Optional
      Your trusted CA certificate in PEM format here for your S3 server.
```

!!! warning
    The S3 upload can be slow. If your users are uploading or downloading a huge amount of data and you have enabled I/O interception your local memory usage may climb rapidly.

## The "file" audit logger

The file audit logger writes audit logs to files on the disk. The storage location can be configured using the following option:

```yaml
audit:
  type: file
  file:
    directory: /var/log/audit
```

If you wish to decode the file format you can use the provided `containerssh-auditlog-decoder` utility or [decode the audit log format yourself](format.md).

## The "log" audit logger

The log audit logger is intended as a debugging facility. It prints the audit log as a structure to the log.

## The "none" audit logger (default)

The "none" audit logger doesn't log anything. This is the default.


