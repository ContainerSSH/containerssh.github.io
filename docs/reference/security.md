<h1>Security configuration</h1>

The security module provides the ability to limit or force the behavior of SSH. It can be configured using the following structure:

```yaml
security:
  maxSessions: 10
  forceCommand: "/run/this/command"
  defaultMode: enable|filter|disable
  env:
    mode: enable|filter|disable
    allow:
      - ENV_VARIABLE_NAME
    deny:
      - ENV_VARIABLE_NAME
  command:
    mode: enable|filter|disable
    allow:
      - /allow/this/command
  shell:
    mode: enable|disable
  subsystem:
    mode: enable|filter|disable
    allow:
      - <enable-this-subsystem>
    deny:
      - <disable-this-subsystem>
  tty:
    mode: enable|disable
  signal:
    mode: enable|filter|disable
    allow:
      - TERM
    deny:
      - KILL
```

## Maximum sessions

The `maxSessions` option lets you limit the number of parallel sessions a client can open. When this number of sessions is reached further session requests are rejected until a session is closed. The recommended value for this option is `10`. 

## Forcing commands

The `forceCommand` option lets you force the execution of a command even when the client has specified a different command to be run. This turns all shell and subsystem requests into command execution requests to run the specified command. The original command will be available in the `SSH_ORIGINAL_COMMAND` environment variable.

## Filtering requests

SSH allows a client to request a multitude of things. The security module allows you to either enable, filter, or deny requests.

- `allow` will allow all requests except the ones specified in the `deny` list.
- `filter` will only allow requests specified in the `allow` list.
- `deny` denies all requests.

You can configure the settings either individually, or using the `defaultMode` setting. It is **strongly recommended** to set a default mode so future ContainerSSH versions adding new features don't accidentally allow something you don't want to enable.

## Environment variable filtering

Using the `env` option you can filter which environment variables the client can set. In `enable` mode you can deny specific environment variables by specifying disallowed variables in the `deny` list. In `filter` mode you can specify allowed variables in the `allow` list. If you want to completely disable setting environment variables you can set the mode to `disable`.

## Command execution

A client can explicitly request running a specific command by specifying it in the command line:

```
ssh yourserver.com run-this-program
```

In `enable` mode command execution is enabled with no filtering. There is no `deny` option as it is trivially easy to work around a simple matching.

In `filter` mode only the commands that are specified in the `allow` list are executed. The match must be exact.

In `deny` mode all command execution is disabled.

## Shell execution

When not specifying a command to the SSH client by default a shell is launched. You can only set the `enable` and `disable` modes. The `filter` mode is valid, but is equal to the `disable` mode.

## Subsystem execution

SSH clients can also execute well-known subsystems, such as `sftp`. The server then decides which binary to execute for the requested subsystem.

When set to `enable` all subsystems except the ones in the `deny` list. In `filter` mode only subsystems in the `allow` list are allowed. In `deny` mode no subsystem execution is allowed.

## TTY/PTY requests

When a client wants to use the SSH server interactively they can send a `PTY` request to the server before executing the program.

The only security options for TTY are `enable` and `disable`. `filter` mode is not explicitly invalid, but behaves like `deny`.

## Signals

Although not used very often, SSH clients can request signals to be delivered to the running program. In `enable` mode all signals except for the ones listed in the `deny` list are allowed. In `filter` mode only the signals in the `allow` list are allowed. In `disable` mode no signal delivery is allowed.

!!! warning
    Signal names have to be specified *without* the `SIG` prefix.

ContainerSSH supports the following signals:

- `ABRT`
- `ALRM`
- `FPE`
- `HUP`
- `ILL`
- `INT`
- `KILL`
- `PIPE`
- `QUIT`
- `SEGV`
- `TERM`
- `USR1`
- `USR2`
