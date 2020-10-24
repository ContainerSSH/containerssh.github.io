<h1>The ContainerSSH Audit Log Format, version 1</h1>

The ContainerSSH audit log is stored in [CBOR](https://cbor.io/) + GZIP format. You will first need to decode the GZIP container and then the CBOR format.

The main element of the CBOR container is an *array of messages* where each message has the following format:

```
Message {
    ConnectionID []byte # opaque binary value that uniquely identifies the connection 
    Timestamp    int64  # nanosecond timestamp when this message happened
    MessageType  int32  # message type identifier (see below)
    Payload      map    # Map of details. See payload structure below
    ChannelID    int64  # Channel identifier. -1 if the message is not related to a channel
}
```

The audit log protocol has the following message types at this time:

| Message type ID | Name | Description | Payload type |
|-----------------|------|-------------|--------------|
| 0   | Connect | TCP connection established | [PayloadConnect](#payloadconnect) |
| 1   | Disconnect | TCP connection closed | *none* |
| 100 | AuthPassword | Password authentication attempt | [PayloadAuthPassword](#payloadauthpassword) |
| 101 | AuthPasswordSuccessful | Successful password authentication | *none* |
| 102 | AuthPasswordFailed | Failed password authentication | *none* |
| 103 | AuthPasswordBackendError | Backend failed to respond | *none* |
| 104 | AuthPubKey | Public key authentication attempt | [PayloadAuthPubKey](#payloadauthpubkey) |
| 105 | AuthPubKeySuccessful | Successful public key authentication | *none* |
| 106  | AuthPubKeyFailed | Failed public key authentication | *none* |
| 107 | AuthPubKeyBackendError | Backend failed to respond | *none* |
| 200 | GlobalRequestUnknown | Unknown global request received | [PayloadGlobalRequestUnknown](#payloadglobalrequestUnknown) |
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
| 500 | Channel I/O | I/O event | [PayloadIO](#payloadio) |

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

## PayloadAuthPubKey

```
PayloadAuthPassword {
    Username string
    Key      []byte  # Public key in OpenSSH wire format
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
    Reason      string  # Freeform message for channel request failure. Do not rely on this text.
}
```

## PayloadChannelRequestUnknownType

```
PayloadChannelRequestUnknownType {
    RequestType string
}
```

## PayloadChannelRequestDecodeFailed

```
PayloadChannelRequestDecodeFailed {
    RequestType string
    Reason      string  # Freeform reason message  
}
```

## PayloadChannelRequestSetEnv

```
PayloadChannelRequestSetEnv {
    Name string
    Value string
}
```

## PayloadChannelRequestExec

```
PayloadChannelRequestExec {
    Program string
}
```

## PayloadChannelRequestPty

```
PayloadChannelRequestPty {
    Columns uint
    Rows    uint
}
```

## PayloadChannelRequestSignal

```
PayloadChannelRequestSignal {
    Signal string
}
```

## PayloadChannelRequestSubsystem

```
PayloadChannelRequestSubsystem {
    Subsystem string
}
```

## PayloadChannelRequestWindow

```
PayloadChannelRequestWindow {
    Colums uint
    Rows uint
}
```

## PayloadIO

```
PayloadIO {
    Stream uint # 0=stdin, 1=stdout, 2=stderr
    Data   []byte
}
```