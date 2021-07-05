{{ reference_outdated() }}

<h1>Troubleshooting ContainerSSH</h1>

When ContainerSSH doesn't work, several components can be involved. Is it ContainerSSH? Can it connect to [the authentication server](auth.md)? How about [the configuration server](configserver.md)? Is the [backend working](backends.md)?

This guide will lead you through the steps of debugging issues with ContainerSSH.

## Turning on debug logging

The first step in determining any potential issues is to enable [debug logging](logging.md). This will output a slew of log messages into the designated log destination that you can use to determine what's going wrong.

If you are trying to debug production failures with lots of traffic it can sometimes be hard to read these logs. That's why a useful field in all connection-related messages is the `connectionId` field. This can be used to tie related log messages together.

If your configuration server is flexible enough you can pass the `debug` log level on a per-user basis to increase the log verbosity for a single user only.

Each message has a unique code. The list of codes is documented in the [codes section](codes.md).

## Connecting in debug mode

Most SSH clients have a debug mode. In the command line SSH you can add the `-vvv` flag to get a lot more verbose output:

```
ssh youruser@youserver.com -vvv
```

## Turning on audit logging

Another useful tool to turn on is [audit logging](audit.md). Audit logging can be another helpful tool when trying to figure out what a certain user is doing. It can record every single interaction that happens over SSH. More importantly, audit logs are also tied to the `connectionId` that is also present in the logs above.

## Debugging webhook server failures

Apart from turning on logging you can also use network monitoring to debug [authentication](auth.md) and [configuration](configserver.md) webhook failures. Even if the connection itself is encrypted, using a tool like [tcpdump](https://www.tcpdump.org/) or [Wireshark](https://www.wireshark.org/) can give you useful clues if the connection is even established correctly or if something is failing on a connection level.

## Debugging container backend failures

When it comes to interacting with container backend you can also use logs as well as network monitoring to determine basic failures. Furthermore, both Docker and Kubernetes provide the ability to monitor events that are happening to get an idea of what's going on.

=== "Docker"
    ```
    docker events
    ```
    
=== "Kubernetes"
    ```
    kubectl get events --watch
    ```

## Debugging with strace

If none of the above steps help it is time to unpack the big tools. [strace](https://strace.io/) is a Linux utility that lets you list all system calls ContainerSSH is doing. This is not the easiest log to read, but the following snippet should help:

```
strace \
  -e trace=open,read,write,readv,writev,recv,recvfrom,send,sendto \
  -s 999 \
  -p CONTAINERSSH-PID-HERE
```

## If all else fails: ask for help

If all else fails we are here for you. Please collect the following items:

1. The debug logs from above.
3. Your configuration file without any sensitive details (credentials, IPs).

Please also prepare the following items if you can, but **don't submit them** as they may contain sensitive credentials:

1. Audit logs (if you have them).
2. Any pcap files from tcpdump or Wireshark you may have.
3. Any strace outputs you may have.
4. Any Docker or Kubernetes events you may have recorded.

You can raise your question in one of the following channels:

- [As a GitHub issue.](https://github.com/ContainerSSH/ContainerSSH/issues/new/choose)
- [As a discussion post.](https://github.com/ContainerSSH/ContainerSSH/discussions)
- [On the debugged.it Discord.](https://debugged.it/discord)

Please link the debug logs and configuration from a [GitHub Gist](http://gist.github.com) or a [Pastebin](https://pastebin.com).

Don't worry about submitting duplicate issues, just make sure to describe your issue in as much detail as possible.
