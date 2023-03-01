title: Kerberos authentication

<h1>Kerberos authentication</h1>

{{ reference_upcoming() }}

This page details setting up Kerberos authentication for ContainerSSH. The ContainerSSH kerberos backend can utilize your existing Kerberos/Active-Directory infrastructure to provide authentication for ContainerSSH. The Kerberos backend supports the standard kerberos authentication protocol (GSSAPI) which provides passwordless authentication given that a valid user principal is available on the users device. Failing that, the Kerberos backend can also perform password based authentication. If a correct password is provided ContainerSSH will generate a principal for the user and place it inside the container at a configurable location. This allows users to authenticate to other services without retyping their passwords.

To use the kerberos backend you'll need two things:
 1) A service keytab
 2) A valid kerberos config file (krb5.conf) for your infrastructure

## Configuration 

The configuration for Kerberos authentication looks as follows:

```
auth:
  password:
    method: kerberos
    kerberos:
      keytab: ./internal/test/krb/krb5.keytab
      configPath: krb5.conf
  gssapi:
    method: kerberos
    kerberos:
      keytab: ./internal/test/krb/krb5.keytab
      configPath: krb5.conf
```

This will allow logging in either via passwordless login using kerberos tickets (GSS-Api authentication) or by typing the users password.

An example `krb5.conf` file looks like this:
```
[logging]
 default = FILE:/var/log/krb5libs.log
 kdc = FILE:/var/log/krb5kdc.log
 admin_server = FILE:/var/log/kadmind.log

[libdefaults]
 default_realm = TESTING.CONTAINERSSH.IO
 dns_lookup_realm = false
 dns_lookup_kdc = false
 ticket_lifetime = 24h
 renew_lifetime = 7d
 forwardable = true

[realms]
TESTING.CONTAINERSSH.IO = {
	kdc = 127.0.0.1
}

[domain_realm]

```

The `ticket_lifetime`, `renew_lifetime` and `forwardable` flags take effect when generating an initial ticket for the user when they logged in via password authentication. They control the lifetime of the users credentials, the amount of time the user can renew those credentials and if these credentials can be forwarded to other services the user logs into.

### Additional configuration

Furthermore, inside the `kerberos` section the following options are supported (and can be customized per-authentication method).

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `keytab` | string | `/etc/krb5.keytab` | The location of the keytab file for the SSH service |
| `acceptor` | string | `any` | The keytab entry (acceptor) that will be used to verify the users tickets when using GSS-Api authentication. The special value `any` will check all acceptors. |
| `configPath` | string | `/etc/krb5.conf` | The location of the kerberos configuration file, used only for password-based authentication, a valid realm must be configured |
| `enforceUsername` | boolean | `true` | Whether to ensure that the authenticated username matches the requested username. **⚠ DANGER if set to false: See the Authorization section ⚠** |
| `credentialCachePath` | string | `/tmp/krb5cc` | The path to store the users credentials inside the container. |
| `clockSkew` | time duration | `5m` | The maximum allowed clock skew for Kerberos messages. Any messages with an older timestamp will be rejected. This is used to prevent replay attacks. |

### Authorization and username matching

The setting `enforceUsername` controls whether to make sure that users can only log in to their own account. When a user connects to an SSH server via kerberos there are 2 different usernames in force, first is the principal username, this is the username present in the kerberos credentials and the real username of the user. The second username is the username that the user requests to log in as.

As an example, if my username is `nikos` and I run the following ssh command:
```
ssh root@myfancykerberosserver.example.org
```
The principal (authenticated) username is `nikos`, my username, and the username that I request to log in as is `root`.

In other words, `enforceUsername` makes sure that `authenticatedUsername == requestedUsername` and as a result, with the default value of this setting, the aforementioned ssh command would fail as `nikos` is not allowed to log into the `root` account (only `root` can).

In cases where it is desirable for some users to be able to log in with a different username than their own, this setting can be disabled. In this mode, it is **strongly advised** to use an authorization webhook to control the autnorization. In the authorization webhook both the authenticated username and the requested username are provided so any custom logic can be implemented.

!!! danger Do not disable enforceUsername without an authorization webhook configured
By disabling `enforceUsername` you are disabling a very important security mechanism that ensures that each user can only access his own account. By disabling this setting without an authorization server guarding logins means that **any user can log in as any username including root**.