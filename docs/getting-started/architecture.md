---
title: Architecture
---

<h1>Architecture</h1>

ContainerSSH is a modular software that consists of the following main components:

```
+------+      +--------------+  2.  +-------------------+
|      |      |              | ---> |    Auth Server    |
|      |      |              |      +-------------------+
|      |      |              |
|      |  1.  |              |  3.  +-------------------+
| User | ---> | ContainerSSH | ---> |   Config Server   |
|      |      |              |      +-------------------+
|      |      |              |
|      |      |              |  4.  +-------------------+
|      |      |              | ---> | Docker/Kubernetes |
+------+      +--------------+      +-------------------+
```

1. The user connects ContainerSSH using an SSH client (e.g. PuTTY)
2. ContainerSSH performs the handshake and offers the user the authentication methods supported. ContainerSSH will submit the users SSH key or password to the authentication server using HTTP (TLS encryption and authentication possible.) For more details see [the page about the Auth Server](authserver.md).
3. If the authentication is successful ContainerSSH will optionally contact the Config Server to fetch the container backend configuration. The config server can pass anything from container backend credentials to image configuration to ContainerSSH. For more details see [the page about the Config Server](../reference/configserver.md).
4. When the users SSH client requests a shell or program ContainerSSH contacts the backend configured (Docker or Kubernetes) and launches the desired Pod / Container. Currently, each new shell or program request launches a new container. For more details see [the backends page](backends/).

The authentication and configuration servers are not part of ContainerSSH and you will need to provide them.
