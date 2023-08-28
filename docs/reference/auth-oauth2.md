title: OAuth2 authentication

<h1>OAuth2 authentication</h1>

|SSH Authentication method | Password              | Public-Key            |  Keyboard-interactive |  GSSAPI               |
|--------------------------|-----------------------|-----------------------|-----------------------|-----------------------|
| OAuth2 backend           | :material-close:      | :material-close:      | :material-check-bold: | :material-close:      |

!!! warning "Feature Preview"
    OAuth2 support is considered as a feature preview as it doesn't have adequate test coverate

The OAuth2 authentication backend authenticates users using any OIDC-compliant OAuth2 servers for authentication (such as KeyCloak, Microsoft Active Directory Federation Services, etc) and features explicit support for GitHub and GitHub Enterprise. Authentication is done using the `keyboard-interactive` SSH authentication mechanism which is supported by most, but not all, SSH clients.

## Supported clients

We have tested the following clients and know them to work:

- OpenSSH
- PuTTY
- WinSCP
- Filezilla

## Configuration

The configuration structure for OAuth2 authentication looks as follows:

```yaml
auth:
  keyboardInteractive:
    method: oauth2
    oauth2:
      clientId: "client ID string"
      clientSecret: "client secret string"
      provider: oidc|github
      github:
        <GitHub configuration>
      oidc:
        <OIDC configuration>
      qrCodeClients:
        - <Client version string regexps that should be sent an ASCII QR code>
      deviceFlowClients:
        - <Client version string regexps to use the device flow with>
      redirect:
        <configuration for the redirect server>
```

## Client credentials

Both OIDC and GitHub needs a client ID and a client secret in order to verify the identity to the OAuth2 server. These can be provided in the `clientId` and `clientSecret` fields.

## Provider configuration

Currently, we support OIDC and GitHub as providers of OAuth2-based authentication.

### OIDC configuration

OpenID Connect (OIDC) is a popular authentication protocol used for Single-Sign-On. It is supported in popular authentication products such as Keycloak and Microsoft Active Directory Federation Services. The ContainerSSH OIDC provider allows users to authenticate using the same single sign on infrastructure as any web-based service. When a user connects, ContainerSSH will provide the user with the configured OIDC servers authentication url to click on and authenticate. There are two different supported OIDC authentication flows that can be used, the device flow and the authorization flow.

### OIDC Device Flow

```yaml
auth:
  keyboardInteractive:
    method: oauth2
    oauth2:
      clientId: "your-client-id"
      clientSecret: "your-client-secret"
      provider: oidc
      oidc:
        url: https://your-oidc-server.example.com/
        deviceFlow: true|false
        authorizationFlow: true|false
        <other oidc options>
```

The OIDC device flow authentication leverages the SSH Keyboard-interactive authentication method to provide the user with a login URL pointing to the OIDC services device flow page and provides the user with a unique one-time-code to enter into the page in order to be authenticated. Depending on the OIDC implementation used the url that is provided can include the authentication code baked-in the url, in which case the user just has to click 'Authorize' in the SSO page, or in other cases they'd have to enter the provided code in order to be authenticated.

Example user login with OIDC device flow
```
$ ssh username@myssh.example.com
Please click the following link: https://sso.example.com/login/device?code=8B60-2612

Enter the following code: 8B60-2612
root@containerssh-fxsjd:/#
```

### OIDC Authorization Flow

```yaml
auth:
  keyboardInteractive:
    method: oauth2
    oauth2:
      clientId: "your-client-id"
      clientSecret: "your-client-secret"
      provider: oidc
      oidc:
        url: https://your-oidc-server.example.com/
        deviceFlow: true|false
        authorizationCodeFlow: true|false
        <other oidc options>
```

The following configuration options are supported:

| Option | Type | Description |
|--------|------|-------------|
| `deviceFlow` | `bool` | Use device flow when authenticating. Defaults to false. |
| `authorizationCodeFlow` | `bool` | Use authorization code flow when authenticating. Defaults to false. |
| `usernameField` | `string` | The field from the result of the userinfo OIDC endpoint to use as the username. Defaults to `sub` |
| `redirectURI` | `string` | The URI the client is returned to after successful authorization flow authentication. |

The device flow takes precedence over the authorization code flow if enabled.

All further options are described on the [HTTP and TLS](http.md#http-client-configuration) page. The `url` field must be provided with the base URL of the OIDC server.

### GitHub configuration

```yaml
auth:
  oauth2:
    provider: github
    clientId: "your-client-id"
    clientSecret: "your-client-secret"
    github:
      <GitHub-specific options>
```

The following options are available for GitHub:

| Option | Type | Description |
|--------|------|-------------|
| `url`  | `string` | URL for GitHub. Defaults to `https://github.com`. Can be changed for GitHub Enterprise. |
| `apiurl` | `string` | API URL for GitHub. Defaults to `https://api.github.com`. Can be changed for GitHub Enterprise. |
| `enforceUsername` | `bool`| Enforce that the SSH and GitHub username must match. Defaults to `true`. If set to `false` the configuration server must evaluate the `github_username` metadata field to create the correct configuration as the SSH username may be incorrect. |
| `requireOrgMembership` | `string` | If set ContainerSSH will require the user to be in the specified organization. It will also request the `org:read` permission from the user to verify this. Failing to provide the permission or not being a member of the organization results in failed authentication. |
| `require2FA` | `bool` | If enabled ContainerSSH will require to have two factor authentication enabled on GitHub. |
| `extraScopes` | `[]string` | A list of [GitHub scopes](https://docs.github.com/en/developers/apps/building-oauth-apps/scopes-for-oauth-apps) (permissions) to request from the user. |
| `enforceScopes` | `bool`| If set to `true` the authentication will fail if the user doesn't grant the scopes requested in `extraScopes`. |

Further options are described on the [HTTP and TLS](http.md#http-client-configuration) page.

## Metadata

The OAuth2 authenticator exposes the following metadata fields to the configuration server:

- `oauth2_access_token`

The OIDC authenticator additionally exposes all fields from the [UserInfo endpoint](https://openid.net/specs/openid-connect-core-1_0.html#UserInfoResponse) with the `oidc_` prefix.

The GitHub authenticator additionally exposes the following fields:

- `github_username` - Username on GitHub.
- `github_email` - Publicly visible profile e-mail of the user.
- `github_name` - Name the user provided on GitHub.
- `github_company` - Company the user entered on GitHub.
- `github_avatar_url` - URL of the user's GitHub avatar.

!!! tip "Tip"
    If you configure the backend to expose the `oauth2_access_token` as the `GITHUB_TOKEN` environment variable you can use the [GitHub CLI](https://cli.github.com/) and many other GitHub-integrated CLI tools without further configuration.

## QR code authentication

When authenticating using the device flow, it can be easier to log in via a mobile phone. When ContainerSSH knows that the client can display an ASCII-art QR code ContainerSSH can send a QR code for mobile login.

While ContainerSSH has a sane list of defaults, you can configure which clients to send a QR code to. This is a list of [Go regular expressions](https://golang.org/pkg/regexp/syntax/) to match against the SSH client version string.

```yaml
auth:
  oauth2:
    qrCodeClients:
      - "regexp1"
      - "regexp2"
      - "..."
```

## Device flow workarounds

Some clients may not be able to handle the device flow properly since it doesn't show a prompt. ContainerSSH contains a list of clients that the device flow should be attempted on. This is a list of regular expressions that match the SSH client version string:

```yaml
auth:
  oauth2:
    deviceFlowClients:
      - "regexp1"
      - "regexp2"  
```

!!! tip "Tip"
    ContainerSSH may still fall back to the authorization code if the device flow is temporarily not available for the matching clients.

## Redirect server

The redirect server is used when the OAuth2 provider doesn't support or temporarily can't provide device flow authentication (e.g. GitHub rate limiting). It is also used if the client can't handle device flow authentication.

In this case the user returns to a website after successful authentication and is presented with a code they need to copy to their SSH window. For this to work you need to configure the HTTP redirect server as follows.

The configuration structure is as follows:

```yaml
auth:
  oauth2:
    redirect:
      <configuration options>
```

The following configuration options are supported:

| Option | Type | Description |
|--------|------|-------------|
| `webroot` | `string` | Path to customized web directory. Optional. |

Additionally, all options in the HTTP server section on the [HTTP and TLS](http.md#http-server-configuration) page are available. The redirect server defaults to port 8080.

### Customizing the redirect site

You also have the option to customize the redirect page. In order to do that you will have to specify a directory to load the webroot from:

```yaml
auth:
  oauth2:
    redirect:
      webroot: /path/to/webroot/
```

The webroot must at least contain one `index.html` file. This file will be used as a [Go template](https://golang.org/pkg/text/template/) and must contain the `{{ "{{ .Code }}" }}` fragment to insert the code the user must copy to their SSH client. Other files in the webroot will be served as normal static files and not be processed as Go templates. 

