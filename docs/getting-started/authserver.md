---
title: Implementing an authentication server
---

<h1>Implementing an authentication server</h1>

ContainerSSH does not know your users and their passwords. Therefore, it calls out to a microservice that you have to provide. Your service can verify the users, passwords, and SSH keys. You will have to provide the microservice URL in the configuration.

```yaml
auth:
  url: "http://your-server-name/"
```

!!! tip
    We have an [OpenAPI document](/reference/api/authconfig) available for the authentication and configuration server. You can check the exact values available there, or use the OpenAPI document to generate parts of your server code.

For password authentication ContainerSSH will call out to the `/password` path on your authentication server. The request body will be the following:

```json
{
    "username": "username",
    "remoteAddress": "127.0.0.1:1234",
    "connectionId": "An opaque ID for the SSH connection",
    "passwordBase64": "Base 64-encoded password"
}
```

The public key auth ContainerSSH will call out to `/pubkey` in the following format:

```json
{
    "username": "username",
    "remoteAddress": "127.0.0.1:1234",
    "connectionId": "An opaque ID for the SSH connection",
    "publicKey": "ssh-rsa ..."
}
```

The public key is provided in the SSH wire format in base64 encoding.

Your server will need to respond with the following JSON:

```json
{
  "success": true
}
```

!!! tip
    We provide a [Go library to implement a authentication server](https://github.com/containerssh/auth).

