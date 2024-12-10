---
title: Configuring ContainerSSH
---

<h1>Configuring ContainerSSH</h1>

Before you can run ContainerSSH, you will need to create a configuration file. In this page you will find some quick-start configuration snippets that will work for the most common use-cases but does not give a full overview of all the features and possible configuration combinations. For more a more in-depth configuration guide you can consult [reference manual](../reference/index.md).

In order to have a working ContainerSSH installation you need to define at a minimum 3 sections in your configuration file.
```yaml
ssh:
  <SSH Configuration options>
auth:
  <Authentication options>
backend: docker|kubernetes|sshproxy
docker:
  <docker options>
...
```

1. `ssh`: Details about your ssh server

2. `auth`: How the users will authenticate to your server

3. `backend` + the associated backend configuration: How the backing container that will be used by the user will be created and with what configuration (mounts etc)

The config file must end in `.yml`, `.yaml`, or `.json`. You can dump the entire configuration file using
`./containerssh --dump-config`

## SSH Server configuration

In the `ssh` section the only mandatory field is `hostkeys` which defines the private keys to be used for the server to authenticate itself to the clients.

```yaml
ssh:
  hostkeys:
    - /path/to/your/host/key
```

## Authentication

=== "Webhook"

    The webhook authentication backend authenticates users by consulting an external authentication server implementing the [ContainerSSH authentication API](../reference/api/authconfig/index.html).

    ```yaml
    auth:
      password:
        method: webhook
        webhook:
          url: https://myauthserver.example.com:8080
      publicKey:
        method: webhook
        webhook:
          url: https://myauthserver.example.com:8080
    ```

    [Read more »](../reference/auth-webhook.md){: .md-button}

=== "OAuth2"
    !!! warning "Feature Preview"
        OAuth2 support is considered as a feature preview as it doesn't have adequate test coverage

    The OAuth2 authentication backend authenticates users using any OIDC-compliant OAuth2 servers for authentication (such as KeyCloak, Microsoft Active Directory Federation Services, etc) and features explicit support for GitHub and GitHub Enterprise.

    === "Generic OIDC provider"

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
                deviceFlow: true
        ```

        [Read more »](../reference/auth-oauth2.md){: .md-button}

    === "GitHub provider"

        ```yaml
        auth:
          keyboardInteractive:
            method: oauth2
            oauth2:
              clientId: "your-client-id"
              clientSecret: "your-client-secret"
              provider: github
        ```

        [Read more »](../reference/auth-oauth2.md#github-configuration){: .md-button}

=== "Kerberos"

    The Kerberos authentication backend authenticates users using any authentication server that implements the Kerberos protocol (such as Microsoft Active-Directory, FreeIPA etc). It supports the GSSAPI authentication method which allows  users to log in without providing a password provided that a valid kerberos ticket is available on the users device. It additionally supports password authentication in case the user does not have or cannot provide a valid ticket.

    ```yaml
    auth:
      method: kerberos
      kerberos:
        keytab: '/etc/krb5.keytab'
    ```

    [Read more »](../reference/auth-kerberos.md){: .md-button}

## Backend

!!! note "Further customization"
    All users will be logged in separate, but identical, containers (equivalent of `docker exec` and `kubectl exec` for the respective backend), in order to customize the resulting container on a per-user basis you'll need to use a [configuration server](./../reference/configserver.md)

=== "Docker"

    The Docker backend creates containers on the specified docker daemon. You can consult the [Docker guide](./docker.md) for more examples.

    ```yaml
    backend: docker
    docker:
      connection:
        host: unix:///var/run/docker.sock
    ```
  
    [Read more »](../reference/docker.md){: .md-button}

=== "Kubernetes"

    The Kubernetes backend creates pods inside a Kubernetes cluster. Please note the following configuration snippet assumes that ContainerSSH is running in the same Kubernetes cluster under a service account with all the required privileges. You can consult the [Kubernetes guide](./kubernetes.md) for more examples.

    ```yaml
    backend: kubernetes
    kubernetes:
      connection:
        host: kubernetes.default.svc
        cacertFile: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
        bearerTokenFile: /var/run/secrets/kubernetes.io/serviceaccount/token
      pod:
        spec:
          containers:
            - name: containerssh-user
              image: busybox
    ```

    [Read more »](../reference/kubernetes.md){: .md-button}

=== "SSH Proxy"

    The SSH proxy backend does not launch containers, instead it connects to a second SSH server and forwards the connections to that backend. This allows for using the [audit log](../reference/audit.md) to inspect SSH traffic, or to dynamically forwarding connections using the [configuration server](../reference/configserver.md).

    ```yaml
    backend: sshproxy
    sshproxy:
      # Add the backend server here
      server: 127.0.0.1
      # Set the following option to true to reuse the connecting user's username.
      usernamePassThrough: true
      # Or specify a username manually
      username: root
      # Specify the password
      password: changeme
      # Or the private key. This can reference a file or be added directly.
      privateKey: |
        -----BEGIN OPENSSH PRIVATE KEY-----
        ...
      # Provide all fingerprints of the backing SSH server's host keys:
      allowedHostKeyFingerprints:
    - SHA256:...
    ```
    
    [Read more »](../reference/sshproxy.md){: .md-button}
