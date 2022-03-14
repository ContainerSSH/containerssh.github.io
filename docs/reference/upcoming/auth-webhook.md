title: Webhook authentication

<h1>Webhook authentication</h1>

{{ reference_upcoming() }}

The authentication webhook can be configured in the main configuration using the following structure:

```yaml
auth:
  method: webhook
  webhook:
    <options>
```

The following options are supported:

| Name          | Type     | Description                                                                                                                              |
|---------------|----------|------------------------------------------------------------------------------------------------------------------------------------------|
| `authTimeout` | `string` | Timeout for the authentication process. HTTP calls that result in a non-200 response call will be retried until this timeout is reached. |

Additional options here are described on the [HTTP and TLS](http.md#http-client-configuration) page. The `url` field
must be provided.

## The authentication webhook

The authentication webhook is a simple JSON `POST` request to which the server must respond with a JSON response.

!!! note We have an [OpenAPI document](../api/authconfig) available for the authentication and configuration server. You
can check the exact values available there, or use the OpenAPI document to generate parts of your server code.

!!! tip We provide a [Go library](https://github.com/ContainerSSH/libcontainerssh) to create an authentication server.

!!! warning A warning about rate limiting: if the authentication server desires to do rate limiting for connecting users
it should take into account that a user is allowed to try multiple authentication attempts (currently hard-coded to 6
per connection) before they are disconnected. Some of the authentication attempts (e.g. public keys) happen
automatically on the client side without the user having any influence on them. Furthermore, ContainerSSH retries failed
HTTP calls. To be effective the authentication server should count the unique connection identifiers seen in
the `connectionId` field and implement a lock-out based on these.

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

The public key will be sent in the authorized key format.

### Authorization

When the separate authorization webhook is configured, you will receive a separate request on the `/authz` endpoint. This is most useful when the primary authentication was done via other methods, such as [oAuth2](auth-oauth2.md) or [Kerberos](auth-kerberos.md).

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

Both endpoints need to respond with an `application/json` response of the following content:

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

!!! tip We provide a [Go library to implement an authentication server](https://github.com/containerssh/libcontainerssh).

