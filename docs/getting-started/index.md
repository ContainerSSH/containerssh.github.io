---
title: ContainerSSH Quick start
---

<h1>Quick start</h1>

This is a quick start guide to get a test server up and running in less than 5 minutes with [docker-compose](https://docs.docker.com/compose/).

!!! warning
    This setup will let any password authenticate. Only use it for testing.

## Step 1: Set up a Dockerized environment

To run this quick start please make sure you have a working [Docker environment](https://docs.docker.com/get-docker/) and a working [docker-compose](https://docs.docker.com/compose/).

## Step 2: Download the sample files

Please download the contents of the [example directory](https://github.com/ContainerSSH/examples/tree/main/quick-start) from the source code repository.

## Step 3: Launch ContainerSSH

In the downloaded directory run `docker-compose build` and then `docker-compose up -d`. This is you server.

## Step 4: Logging in

Run `ssh foo@localhost -p 2222` on the same machine via a new terminal window. This is your test client. You should be able to log in with any password.

Alternatively you can also try the user `busybox` to land in a Busybox container.

## Step 5: Cleaning up

Once you're done, you can shut down the server using the `docker-compose down`, then remove the images using `docker-compose rm`.

Finally, you can also remove the guest image:

```
docker image rm containerssh/containerssh-guest-image
```

## Step 6: Making it productive

The authentication and configuration server included in the example is a dummy server and lets any password in. To actually use ContainerSSH, you will have to write [your own authentication server](authserver.md). We recommend reading the [architecture overview](architecture.md) before proceeding.

!!! tip
    You can pass the `CONTAINERSSH_ALLOW_ALL` environment variable to the demo auth-config server to build a honeypot.
