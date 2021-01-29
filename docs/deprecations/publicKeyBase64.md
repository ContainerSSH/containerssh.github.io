<h1>Deprecating the publicKeyBase64 field in the authentication protocol {{ since("0.4") }}</h1>

Before ContainerSSH version 0.4 sent a field called `publicKeyBase64` to the authentication server which contained the SSH key in the binary OpenSSH wire format. However, this was not easy to integrate, so ContainerSSH 0.4 adds a field called `publicKey` containing the public key in the OpenSSH authorized keys format.

The `publicKeyBase64` field is now deprecated and will be removed in a future version. Authentication server implementations should switch to using the `publicKey` field.