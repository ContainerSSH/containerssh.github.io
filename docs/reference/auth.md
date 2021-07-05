title: Authentication

<h1>Authentication</h1>

ContainerSSH does not know your users and their passwords. It has two options to verify them:

1. It calls out to a microservice that you have to provide via a webhook. Your service can verify the users, passwords, and SSH keys.
2. Via OAuth2.

## Configuration

The authentication webhook can be configured in the main configuration using the following structure:

```yaml
auth:
  method: webhook|oauth2
  webhook: 
    <webhook options>
  oauth2:
    <oauth2 options>
```

[Webhook configuration options](auth-webhook.md){: .md-button} [Oauth2 configuration options](auth-oauth2.md){: .md-button}
