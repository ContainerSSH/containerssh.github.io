
{{ reference_upcoming() }}

<h1>Logging</h1>

ContainerSSH comes with configurable logging facilities. You can configure the following options:

1. The minimum log level to filter unnecessary log messages
2. The log format
3. The log destination

## Configuring the minimum log level

You can configure the minimum log level by adding the following to your configuration:

```yaml
log:
  level: "warning"
```

!!! tip
    You can configure the log level on a per-user basis using the [configuration server](configserver.md).


The supported levels are in accordance with the Syslog standard:

- `debug`
- `info`
- `notice`
- `warning`
- `error`
- `crit`
- `alert`
- `emerg`

## Configuring the log format

ContainerSSH can log in both text and newline-delimited JSON (`ljson`) format. You can change the format with the following setting:

```yaml
log:
  format: "ljson"
```

### The JSON log format

The LJSON format outputs a JSON-formatted string per log message. For file and stdout these JSON messages are separated by a newline from each other.

When writing to the `stdout` or `file` destinations the format is the following:

```json
{
  "timestamp":"Timestamp in RFC3339 format",
  "level":"the log level",
  "code":"ERROR_CODE_HERE",
  "message":"the message (optional)",
  "details": {
    "the detail object if any (optional)"
  }
}
```

When writing to syslog the format is the same, but does not contain the `timestamp` and `level` fields as they are redundant.

### The text log format

When writing to the `stdout` or `file` destinations the text log format has the following fields delimited by a tab (`\t`) character:

```
TIMESTAMP\tLEVEL\tMESSAGE
```

The `TIMESTAMP` will be formatted according to RFC3339, while the `LEVEL` will be the text-representation of the log level. The `MESSAGE` field will contain the text representation of the message.

!!! warning
    The text message is not intended for machine processing and may change across versions. If you intend to do machine processing please use the `details` field from the `ljson` format.
    
## Setting the output

The output configuration of ContainerSSH is the following:

```yaml
log:
  destination: "stdout|file|syslog"
  <other destination options>
``` 

### Writing to the stdout

The stdout destination is the simplest: it will write error messages to the standard output of ContainerSSH. This is the default logging method.

```yaml
log:
  destination: "stdout"
``` 

### Writing to a file

You can write to a specific file using the following options:

```yaml
log:
  destination: "file"
  file: "/var/log/containerssh/containerssh.log"
``` 

ContainerSSH will write to the specified file in the specified format.

!!! tip
    ContainerSSH supports *log rotation*. You can trigger a log rotation by sending a HUP (hangup) signal to ContainerSSH.

### Writing to syslog

ContainerSSH supports writing to syslog via a Unix socket or UDP. TCP syslog is not supported due to the complexity of maintaining a stable connection and buffering messages between disconnects.

Syslog can be configured as follows:

```yaml
log:
  destination: syslog
  syslog:
    # Change to IP and port for UDP
    destination: /dev/log
    # See below for supported names
    facility: auth
    # Program name to log as
    tag: ContainerSSH
    # Log PID with program name
    pid: false
```

The following facilities are supported:

- `kern`
- `user`
- `mail`
- `daemon`
- `auth`
- `syslog`
- `lpr`
- `news`
- `uucp`
- `cron`
- `authpriv`
- `ftp`
- `ntp`
- `logaudit`
- `logalert`
- `clock`
- `local0..7`

!!! warning
    ContainerSSH can log very long messages with lots of details. Please make sure to bump your maximum line length to at least 4096 characters in your Syslog server to avoid message truncation. *([rsyslog](https://www.rsyslog.com/doc/master/configuration/global/index.html) and [syslog-ng](https://www.syslog-ng.com/technical-documents/doc/syslog-ng-open-source-edition/3.17/administration-guide/log-msg-size) have higher default values, so you don't need to change the configuration if you are using these syslog servers.)*