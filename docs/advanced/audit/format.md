<h1>The ContainerSSH Audit Log Format, version 1 (draft)</h1>


The ContainerSSH audit log is stored in [CBOR](https://cbor.io/) + GZIP format.

However, before GZIP decoding you must provide/decode the **file header**. The file header is 40 bytes long. The fist 32 bytes must contain the string `ContainerSSH-Auditlog`, the rest padded with 0 bytes. The last 8 bytes contain the audit log format version number as a 64 bit little endian integer.

After the first 40 bytes you will have to GZIP-decode the rest of the file and then the CBOR format.

!!! note
    We provide a Go library to decode the audit log format. Check out the details [on GitHub](https://github.com/ContainerSSH/auditlog).

The main element of the CBOR container is an *array of messages* where each message has the following format:

```
Message {
    ConnectionID string # opaque hex value
                        # that uniquely identifies the connection
 
    Timestamp    int64  # nanosecond timestamp when this message happened

    MessageType  int32  # message type identifier (see below)

    Payload      map    # Map of details. See payload structure below

    ChannelID    int64  # Channel identifier.
                        # -1 if the message is not related to a channel
}
```

The audit log protocol has the following message types at this time:

| Message type ID | Name | Description | Payload type |
|-----------------|------|-------------|--------------|
| 0   | Connect | TCP connection established | [PayloadConnect](#payloadconnect) |
| 1   | Disconnect | TCP connection closed | *none* |
| 100 | AuthPassword | Password authentication attempt | [PayloadAuthPassword](#payloadauthpassword) |
| 101 | AuthPasswordSuccessful | Successful password authentication | [PayloadAuthPassword](#payloadauthpassword) |
| 102 | AuthPasswordFailed | Failed password authentication | [PayloadAuthPassword](#payloadauthpassword) |
| 103 | AuthPasswordBackendError | Backend failed to respond | [PayloadAuthPasswordBackendError](#payloadauthpasswordbackenderror) |
| 104 | AuthPubKey | Public key authentication attempt | [PayloadAuthPubKey](#payloadauthpubkey) |
| 105 | AuthPubKeySuccessful | Successful public key authentication | [PayloadAuthPubKey](#payloadauthpubkey) |
| 106 | AuthPubKeyFailed | Failed public key authentication | [PayloadAuthPubKey](#payloadauthpubkey) |
| 107 | AuthPubKeyBackendError | Backend failed to respond | [PayloadAuthPubKeyBackendError](#payloadauthpubkeybackenderror) |
| 198 | HandshakeFailed | Indicates a handshake failure | [PayloadHandshakeFailed](#payloadhandshakefailed) |
| 199 | HandshakeSuccessful | Indicates a successful handshake | [PayloadHandshakeFailed](#payloadhandshakesuccessful) |
| 200 | GlobalRequestUnknown | Unknown global request received | [PayloadGlobalRequestUnknown](#payloadglobalrequestunknown) |
| 300 | NewChannel | Requesting a new SSH channel | [PayloadNewChannel](#payloadnewchannel) |
| 301 | NewChannelSuccessful | New SSH channel successful | [PayloadNewChannelSuccessful](#payloadnewchannelsuccessful) |
| 302 | NewChannelFailed | New SSH channel failed | [PayloadNewChannelFailed](#payloadnewchannelfailed) |
| 400 | ChannelRequestUnknownType | A channel request of unknown type | [PayloadChannelRequestUnknownType](#payloadchannelrequestunknowntype) |
| 401 | ChannelRequestDecodeFailed | An invalid request payload was received | [PayloadChannelRequestDecodeFailed](#payloadchannelrequestdecodefailed) |
| 402 | ChannelRequestSetEnv | An environment variable was requested | [PayloadChannelRequestSetEnv](#payloadchannelrequestsetenv) |
| 403 | ChannelRequestExec | A program execution was requested | [PayloadChannelRequestExec](#payloadchannelrequestexec) |
| 404 | ChannelRequestPty | An interactive terminal was requested | [PayloadChannelRequestPty](#payloadchannelrequestpty) |
| 405 | ChannelRequestShell | A shell was requested | *none* |
| 406 | ChannelRequestSignal | A signal was sent | [PayloadChannelRequestSignal](#payloadchannelrequestsignal) |
| 407 | ChannelRequestSubsystem | A subsystem (e.g. SFTP) was requested | [PayloadChannelRequestSubsystem](#payloadchannelrequestsubsystem) |
| 408 | ChannelRequestWindow | Window size change | [PayloadChannelRequestWindow](#payloadchannelrequestwindow) |
| 499 | ChannelExit | The program running has exited | [PayloadExit](#payloadexit) |
| 500 | Channel I/O | I/O event | [PayloadIO](#payloadio) |
| 501 | RequestFailed | A global or channel request has failed | [PayloadRequestFailed](#payloadrequestfailed) |

!!! note
    When writing a decoder, your decoder should ignore unknown fields and message codes as the format may be extended to accommodate new ContainerSSH features.

## PayloadConnect

```
PayloadConnect {
    RemoteAddr string  # IP address of the connecting party 
}
```

## PayloadAuthPassword

```
PayloadAuthPassword {
    Username string
    Password []byte  # Password can contain special characters, so it's a byte array
}
```

## PayloadAuthPasswordBackendError

```
PayloadAuthPasswordBackendError {
    Username string
    Password []byte  # Password can contain special characters, so it's a byte array
    Reason   string
}
```

## PayloadAuthPubKey

```
PayloadAuthPassword {
    Username string
    Key      string  # Public key in the authorized_keys format
}
```

## PayloadAuthPubKeyBackendError

```
PayloadAuthPasswordBackendError {
    Username string
    Key      string  # Public key in the authorized_keys format
    Reason   string
}
```

## PayloadHandshakeFailed

```
PayloadHandshakeFailed {
    Reason string
}
```

## PayloadHandshakeSuccessful

```
PayloadHandshakeSuccessful {
    Username string
}
```

## PayloadGlobalRequestUnknown

```
PayloadGlobalRequestUnknown {
    ChannelType string
}
```

## PayloadNewChannel

```
PayloadNewChannel {
    ChannelType string
}
```

## PayloadNewChannelSuccessful

```
PayloadNewChannelSuccessful {
    ChannelType string
}
```

## PayloadNewChannelFailed

```
PayloadNewChannelFailed {
    ChannelType string
    Reason      string  # Freeform message for channel request failure.
                        # Do not rely on this text.
}
```

## PayloadChannelRequestUnknownType

```
PayloadChannelRequestUnknownType {
	RequestID   uint64
    RequestType string
    Payload     []byte
}
```

## PayloadChannelRequestDecodeFailed

```
PayloadChannelRequestDecodeFailed {
	RequestID   uint64
    RequestType string
    Payload     []byte
    Reason      string  # Freeform reason message.
                        # Do not rely on this text, it may change between versions.
}
```

## PayloadChannelRequestSetEnv

```
PayloadChannelRequestSetEnv {
	RequestID uint64
    Name      string
    Value     string
}
```

## PayloadChannelRequestExec

```
PayloadChannelRequestExec {
	RequestID uint64
    Program   string
}
```

## PayloadChannelRequestPty

```
PayloadChannelRequestPty {
	RequestID uint64
    Term      string
	Columns   uint32
	Rows      uint32
	Width     uint32
	Height    uint32
    ModeList  []byte
}
```

## PayloadChannelRequestSignal

```
PayloadChannelRequestSignal {
	RequestID uint64
    Signal    string
}
```

## PayloadChannelRequestSubsystem

```
PayloadChannelRequestSubsystem {
	RequestID uint64
    Subsystem string
}
```

## PayloadChannelRequestWindow

```
PayloadChannelRequestWindow {
	RequestID uint64
	Columns   uint32
	Rows      uint32
	Width     uint32
	Height    uint32
}
```

## PayloadExit

```
PayloadExit {
    ExitStatus uint32
}
```

## PayloadIO

```
PayloadIO {
    Stream uint # 0=stdin, 1=stdout, 2=stderr
    Data   []byte
}
```

## PayloadRequestFailed

```
PayloadRequestFailed {
	RequestID uint64
	Reason    string
}
```