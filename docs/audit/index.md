<h1>Audit logging {{ upcoming("0.4.0") }}</h1>

ContainerSSH contains an audit logging facility that can log every interaction happening over SSH. This functionality is disabled by default as it as serious security and privacy implications, as well as severe resource requirements.

Audit logging can be enabled in the configuration using the following structure:

```yaml
audit:
  type: none|file|log     # Which audit logger to use. Defaults to none.
  intercept:
    stdin: true|false     # Intercept keystrokes from user
    stdout: true|false    # Intercept standard output
    stderr: true|false    # Intercept standard error
    passwords: true|false # Intercept passwords during authentication
```

## About interceptions

The `intercept` options give you a wide range of options when it comes to detailed logging of actions by users. You may want to, for example, enable `stdout` logging while keeping `stdin` disabled to avoid accidentally capturing passwords typed into the console.

However, this approach may fail if SFTP is enabled as you will fail to capture binaries uploaded to the server. Audit logging should therefore be enjoyed with great care and the logs should always be stored on an encrypted storage device.

## The "file" audit logger

The file audit logger writes audit logs to files on the disk. The storage location can be configured using the following option:

```yaml
audit:
  //...
  file:
    directory: /var/log/audit
```

If you wish to decode the file format you can use the provided `containerssh-auditlog-decoder` utility or [decode the audit log format yourself](format.md).

## The "log" audit logger

The log audit logger is intended as a debugging facility. It prints the audit log as a structure to the log.

## The "none" audit logger

The "none" audit logger doesn't log anything.


