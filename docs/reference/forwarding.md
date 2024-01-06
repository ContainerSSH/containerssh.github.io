title: Connection Forwarding

<h1>Connection Forwarding</h1>

This page details setting up connection forwarding for ContainerSSH. Connection forwarding works by having the ContainerSSH agent act as the proxy when a connection forwarding is placed. Connection forwarding comes in multiple flavours: You can ask for the listening end to be either on the client or inside the container, and respectively you can choose listen from a ip:port combo or a named/unix socket and send to either an ip:port combo or a named socket. Additionally, the direct forward option is also supported which enables the usage of the SOCKS proxy support in OpenSSH. Finally, X11 forwarding is also supported.

## Supported clients

We have tested the following clients and know them to work:

- OpenSSH

## Configuration

Forwarding is disabled by default, you can enable it via the [security settings](./security.md). Currently only enable/disable directives are supported, no filtering rules. In order for specific ports to be forwarded, or a specific forwarding function please consult the documentation of your SSH Client. 

In order to enable all forwarding functionality the following configuration can be used:

```yaml
security:
    forwarding:
        reverseForwardingMode: enable
        forwardingMode: enable
        socketForwardingMode: enable
        socketListenMode: enable
        x11ForwardingMode: enable
```

- The `reverseForwardingMode` setting how to treat reverse port forwarding requests, connections from the container to the client.
- The `forwardingMode` setting configures how to treat port forwarding requests from the client to the container. Enabling this setting also allows using ContainerSSH as a SOCKs proxy.
- The `socketForwardingMode` setting configures how to treat connection requests from the client to a unix socket in the container.
- The `socketListenMode` setting configures how to treat requests to listen for connections to a unix socket in the container.
- The `x11ForwardingMode` setting configures how to treat X11 forwarding requests from the container to the client
