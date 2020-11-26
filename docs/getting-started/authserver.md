<h1>Implementing an authentication server</h1>

ContainerSSH does not know your users and their passwords. Therefore, it calls out to a microservice that you have to provide. Your service can verify the users, passwords, and SSH keys. You will have to provide the microservice URL in the configuration"

```yaml
auth:
  url: "http://your-server-name/"
```

!!! tip
    We have an [OpenAPI document](/api/authconfig) available for the authentication and configuration server. You can check the exact values available there, or use the OpenAPI document to generate parts of your server code.

For password authentication ContainerSSH will call out to the `/password` path on your authentication server. The request body will be the following:

```json
{
    "username": "username",
    "remoteAddress": "127.0.0.1:1234",
    "sessionId": "A base64 SSH session ID",
    "passwordBase64": "Base 64 password"
}
```

The public key auth ContainerSSH will call out to `/pubkey` in the following format:

```json
{
    "username": "username",
    "remoteAddress": "127.0.0.1:1234",
    "sessionId": "A base64 SSH session ID",
    "publicKeyBase64": "Base 64 public key in SSH wire format"
}
```

The public key is provided in the SSH wire format in base64 encoding.

Your server will need to respond with the following JSON:

```json
{
  "success": true
}
```

> **Tip** You can find the source code for a test authentication and configuration server written in Go
> [in the code repository](https://github.com/containerssh/containerssh/blob/stable/cmd/containerssh-testauthconfigserver/main.go)
