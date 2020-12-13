---
title: Understanding SSH
---

<h1>Understanding SSH</h1>

Let's face it: we don't think about SSH all that much. We SSH into a server and merrily type away our commands. *Until we need to write an SSH server.*

This document describes the high level concepts of SSH: how do you open a connection, what are channels, and how do requests work.

This is a very high level overview, but should contain everything you need to get started with ContainerSSH development.

## Handshake

When the user connects an SSH server the SSH keys are verified. We won't discuss this here as for ContainerSSH the Go SSH library takes care of that.

The first thing we are concerned with is authentication. Authentication is described by [RFC 4252](https://tools.ietf.org/html/rfc4252) and it states the following:

> The server drives the authentication by telling the client which authentication methods can be used to continue the exchange at any given time.  The client has the freedom to try the methods listed by the server in any order.

In other words, when the user connects the SSH server tells the client which authentication method it supports. The client picks one of them and performs the authentication. The server can then decide to reject, allow, or show the client another list of methods (e.g. to perform two factor authentication). The Go library vastly simplifies this process and only allows a single means of authentication for each connection.

Each authentication request contains a username. The username may change between authentication attempts to authenticate against different systems, but this is not customary.

## Connection

Once the authentication is complete the connection is open and both the client and the server may now send two types of messages: *global requests* and *channels*.

Global requests describe requests in either direction that one party wants from the other. For example, the [OpenSSH extensions](http://cvsweb.openbsd.org/cgi-bin/cvsweb/~checkout~/src/usr.bin/ssh/PROTOCOL?content-type=text/plain) describe the `no-more-sessions@openssh.com` to indicate that no more session channels should be opened on this connection.

The channels, on the other hand are means of transporting data. For example, the `session` channel is responsible for executing a program and then transporting the standard input, output, and error data streams to and from the program. They also give both ends the ability to send channel-specific requests (e.g. setting environment variables, resizing the window, etc.).

## Session channels

While there are theoretically other types of channels possible, we currently only support `session` channels. The client can request channels to be opened at any time.

We currently support the following *requests* on the `session` channel. These are described in [RFC 4254](https://tools.ietf.org/html/rfc4254).

`env`
: Sets an environment variable for the soon to be executed program.

`pty`
: Requests an interactive terminal for user input.

`shell`
: Requests the default shell to be executed.

`exec`
: Requests a specific program to be executed.

`subsystem`
: Requests a well-known subsystem (e.g. `sftp`) to be executed.

`window-change`
: Informs the server that an interactive terminal window has changed size. This is only sent once the program has been started with the requests above.

`signal`
: Requests the server to send a signal to the currently running process.

In addition, we also send an `exit-status` request to the client from the server when the program exits to inform the client of the exit code.

## Interactive terminals 

As you can see above, the user can request an interactive terminal using the `pty` request. This is done automatically by SSH clients if they detect that their input is an interactive terminal.

Using interactive terminals changes the operation mode of stdin, stdout, and stderr. While programs normally write their standard output to `stdout` and their error output to `stderr`, programs running in interactive mode send their combined output to `stdout` using a special framing. (TTY multiplexing)

Thankfully, we don't need to know too much about TTY multiplexing for writing an SSH server since it is transparently passed through from the container engine to the SSH channel and we don't interact with it.

## RFCs

The SSH protocol is governed by the following RFCs:

[RFC 913: Simple File Transfer Protocol](https://tools.ietf.org/html/rfc913)
: This document describes the SFTP protocol used over SSH.

[RFC 4250: The Secure Shell (SSH) Protocol Assigned Numbers](https://tools.ietf.org/html/rfc4250)
: This document describes the protocol numbers and standard constants used in SSH.

[RFC 4251: The Secure Shell (SSH) Protocol Architecture](https://tools.ietf.org/html/rfc4251)
: This document describes the design decisions taken to work with SSH.

[RFC 4252: The Secure Shell (SSH) Authentication Protocol](https://tools.ietf.org/html/rfc4252)
: This document describes how user authentication works in SSH.

[RFC 4253: The Secure Shell (SSH) Transport Layer Protocol](https://tools.ietf.org/html/rfc4253)
: This document describes the details of how data is transported over SSH.

[RFC 4254: The Secure Shell (SSH) Connection Protocol](https://tools.ietf.org/html/rfc4254)
: This document contains the parts most interesting to us: how channels, sessions, etc. work.

[RFC 4255: Using DNS to Securely Publish Secure Shell (SSH) Key Fingerprints](https://tools.ietf.org/html/rfc4255)
: This document describes how to publish SSH fingerprints using DNS. It has not seen wide adoption.

[RFC 4256: Generic Message Exchange Authentication for the Secure Shell Protocol (SSH)](https://tools.ietf.org/html/rfc4256)
: This document describes the keyboard-interactive authentication for SSH, which is often used for two factor authentication.

[RFC 4335: The Secure Shell (SSH) Session Channel Break Extension](https://tools.ietf.org/html/rfc4335)
: This document describes the telnet-compatible break request for use in SSH.

[RFC 4344](https://tools.ietf.org/html/rfc4344), [RFC 4345](https://tools.ietf.org/html/rfc4345), [RFC 4419](https://tools.ietf.org/html/rfc4419), [RFC 4432](https://tools.ietf.org/html/rfc4432)
: These documents describe various encryption-related topics.

[RFC 4462: Generic Security Service Application Program Interface (GSS-API) Authentication and Key Exchange for the Secure Shell (SSH) Protocol](https://tools.ietf.org/html/rfc4462)
: This document describes the GSS-API authentication method that can be used to authenticate with a Kerberos ticket.

[RFC 4716: The Secure Shell (SSH) Public Key File Format](https://tools.ietf.org/html/rfc4716)
: This document describes the PEM-like format to store SSH keys in.

[RFC 4819: Secure Shell Public Key Subsystem](https://tools.ietf.org/html/rfc4819)
: This document describes the SSH public key subsystem usable for adding, removing, and listing public keys.

[RFC 5647](https://tools.ietf.org/html/rfc5647), [RFC 5656](https://tools.ietf.org/html/rfc5656), [RFC 6187](https://tools.ietf.org/html/rfc6187), [RFC 6239](https://tools.ietf.org/html/rfc6239), [RFC 6594](https://tools.ietf.org/html/rfc6594), [RFC 6668](https://tools.ietf.org/html/rfc6668)
: These documents describe various cryptography and authentication related topics.

[RFC 7479: Using Ed25519 in SSHFP Resource Records](https://tools.ietf.org/html/rfc7479)
: This document describes publishing ED25519 host keys using DNS.

[RFC 5592: Secure Shell Transport Model for the Simple Network Management Protocol (SNMP)](https://tools.ietf.org/html/rfc5592)
: This protocol describes using SNMP over SSH.

[RFC 6242: Using the NETCONF Protocol over Secure Shell (SSH)](https://tools.ietf.org/html/rfc6242)
: This document describes transporting the [RFC 6241 Network Configuration Protocol](https://tools.ietf.org/html/rfc6241) over SSH. This can be used to manage networking equipment.

In addition, OpenSSH defines the following extensions:

[The OpenSSH Protocol](http://cvsweb.openbsd.org/cgi-bin/cvsweb/~checkout~/src/usr.bin/ssh/PROTOCOL?content-type=text/plain)
: This document describes new cryptographic methods, tunnel forwarding, domain socket forwarding, and many more changes.

[The CertKeys Document](http://cvsweb.openbsd.org/cgi-bin/cvsweb/~checkout~/src/usr.bin/ssh/PROTOCOL.certkeys?content-type=text/plain)
: This document describes the OpenSSH CA method.

[SSH Agent Protocol](https://tools.ietf.org/html/draft-miller-ssh-agent-04)
: Describes the protocol used by the SSH agent holding the SSH keys in escrow.