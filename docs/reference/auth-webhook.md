title: Webhook authentication

<h1>Webhook authentication</h1>

|SSH Authentication method | Password              | Public-Key            |  Keyboard-interactive |  GSSAPI               |
|--------------------------|-----------------------|-----------------------|-----------------------|-----------------------|
| Webhook support          | :material-check-bold: | :material-check-bold: | :material-close:      | :material-close:      |

The webhook authentication backend authenticates users by consulting an external authentication server implementing the [ContainerSSH authentication API](../api/authconfig).

The authentication webhook can be configured in the main configuration using the following structure:

```yaml
auth:
  password:
    method: webhook
    webhook:
      url: https://myauthenticationserver.example.org
      <options>
  publicKey:
    method: webhook
    webhook:
      url: https://myauthenticationserver.example.org
      <webhook options>
  authz:
    method: webhook
    webhook: 
      url: https://myauthenticationserver.example.org
      <webhook options>
```

The following options are supported:

| Name          | Type     | Description                                                                                                                              |
|---------------|----------|------------------------------------------------------------------------------------------------------------------------------------------|
| `authTimeout` | `string` | Timeout for the authentication process. HTTP calls that result in a non-200 response call will be retried until this timeout is reached. |

Additional options here are described on the [HTTP and TLS](http.md#http-client-configuration) page. The `url` field
must be provided.

## The authentication webhook

The authentication webhook is a simple JSON `POST` request to which the server must respond with a JSON response.

!!! note
    We have an [OpenAPI document](../api/authconfig) available for the authentication and configuration server. You can check the exact values available there, or use the OpenAPI document to generate parts of your server code.

!!! tip
    We provide a [Go library](https://github.com/ContainerSSH/libcontainerssh) to create an authentication server.

!!! warning
    A warning about rate limiting: if the authentication server desires to do rate limiting for connecting users it should take into account that a user is allowed to try multiple authentication attempts (currently hard-coded to 6 per connection) before they are disconnected. Some of the authentication attempts (e.g. public keys) happen automatically on the client side without the user having any influence on them. Furthermore, ContainerSSH retries failed HTTP calls. To be effective the authentication server should count the unique connection identifiers seen in the `connectionId` field and implement a lock-out based on these.

### Password authentication

On password authentication the authentication server will receive the following request to the `/password` endpoint:

```json
{
  "username": "username",
  "remoteAddress": "127.0.0.1:1234",
  "connectionId": "An opaque ID for the SSH connection",
  "clientVersion": "SSH client version string",
  "passwordBase64": "Base 64-encoded password"
}
```

### Public key authentication

On public key authentication the authentication server will receive the following request to the `/pubkey` endpoint:

```json
{
  "username": "username",
  "remoteAddress": "127.0.0.1:1234",
  "connectionId": "An opaque ID for the SSH connection",
  "publicKey": "ssh-rsa ..."
}
```

The public key will be sent in the authorized key format. It is the responsibility of the authentication server only to verify that the provided public key matches the public key on record for the user. If a positive authentication response is received ContainerSSH will then continue to verify that the client has posession of the private key before completing the authentication process.

### Authorization

When the separate authorization webhook is configured, you will receive a separate request on the `/authz` endpoint. This is most useful when the primary authentication was done via other methods, such as [OAuth2](auth-oauth2.md) or [Kerberos](auth-kerberos.md).

```json
{
  "username": "username",
  "authenticatedUsername": "username obtained during authentication",
  "remoteAddress": "127.0.0.1:1234",
  "connectionId": "An opaque ID for the SSH connection",
  "clientVersion": "SSH client version string",
  "metadata": {
    "metadata_name": {
      "value": "metadata_value",
      "sensitive": true|false
    }
  },
  "environment": {
    "env_variable_name": {
      "value": "env variable value",
      "sensitive": true|false
    }
  },
  "files": {
    "/path/to/file": {
      "value": "base64-encoded contents of the file",
      "sensitive": true|false
    }
  }
}
```

### Response

The authorization server should always respond with a 200 status code regardless of the authentication status, non-200 status codes are reserved for (permanent or not) errors. The response, at a minimum, consists of a `success` field indicating if the authentication should be considered successful and the `authenticatedUsername` field which indicates the username of the authenticated user.

```json
{
  "success": true,
  "authenticatedUsername": "foo",
}
```

When responding the authentication server has the opportunity to define extra metadata, environment variables or files for the user connection. All three are forwarded to all following requests (e.g. Authentication Webhook -> Authorization Webhook -> [Configuration Webhook](./configserver.md)) made and can be used to influence authorization or configuration decisions, the environment variables are added to the users environment when the connection is established and the files are placed in the container before the users command executes.

If any metadata, environment variables or files are marked as sensitive they will not be re-transmitted with further webhook calls but they will be taken account of and added to the users environment or, in the case of files, placed in the container. This can be used to limit exposure in case the file contains sensitive information e.g. users credentials.

All endpoints need to respond with an `application/json` response of the following content:

```json
{
  "success": true,
  "authenticatedUsername": "username that was verified",
  "metadata": {
    "metadata_name": {
      "value": "metadata_value",
      "sensitive": true|false
    }
  },
  "environment": {
    "env_variable_name": {
      "value": "env variable value",
      "sensitive": true|false
    }
  },
  "files": {
    "/path/to/file": {
      "value": "base64-encoded contents of the file",
      "sensitive": true|false
    }
  }
}
```

!!! tip
    We provide a [Go library to implement an authentication server](https://github.com/containerssh/libcontainerssh).

