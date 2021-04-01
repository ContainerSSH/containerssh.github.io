<h1>Deprecating the sessionId field in the authentication and configuration server protocol {{ since("0.4") }}</h1>

Before ContainerSSH 0.4 both the [authentication server protocol](../reference/auth.md) and the [configuration server protocol](../reference/configserver.md) contained a field called `sessionId` which would include a self-generated ID for the session.

In ContainerSSH 0.4 we are introducing a new ID called `connectionId` which uniquely identifies the SSH connection across all ContainerSSH-related platforms (auth/config/audit log/etc).

The `sessionId` field is now deprecated and mirrors the contents of `connectionId`. The field will be removed in the future and auth / config server implementers should no longer rely on it.
