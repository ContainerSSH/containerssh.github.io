---
title: Frequently Asked Questions
---

<h1>FAQ</h1>

## Is ContainerSSH secure?

ContainerSSH depends on a number of libraries to achieve what it does. A security hole in any of the critical ones could mean a compromise of your container environment, especially if you are using the `dockerrun` backend. (Docker has no access control so a compromise means your whole host is compromised.)

Please read the [hardening guide](../reference/hardening.md) if you intend to use ContainerSSH in production.

## Is ContainerSSH production-ready?

ContainerSSH is in use by several companies in production and has caused no issues or crashes. That being said, it is very early in its development and the API and configuration file format may still change.

If you intend to use ContainerSSH in production please read the [hardening guide](../reference/hardening.md) and [feel free to reach out](https://pasztor.at/discord/).

## Does ContainerSSH delete containers after it is done?

ContainerSSH does its best to delete containers it creates. However, at this time there is no cleanup mechanism in case it crashes.

## Do I need to run ContainerSSH as root?

No! In fact, you shouldn't! ContainerSSH is perfectly fine running as non-root as long as it has access to Kubernetes or Docker. (Granted, access to the Docker socket means it could easily launch a root process on the host.)

## Does ContainerSSH support SFTP?

Yes, but your container image must contain an SFTP server binary and your config.yaml or config server must contain the correct path for the server.

## Does ContainerSSH support SCP?

Not at this time.

## Does ContainerSSH support TCP port forwarding?

No, but it is planned.

## Does ContainerSSH support SSH agent forwarding?

No, but it is planned.

## Does ContainerSSH support X11 forwarding?

No, and X11 is a rarely used feature, so we are not planning on supporting it in the near future.

## Does ContainerSSH support forwarding signals?

Yes, as of version 0.4 all backends support signal forwarding using the ContainerSSH agent.

## Does ContainerSSH support window resizing?

Yes.

## Does ContainerSSH support environment variable passing?

Yes.

## Does ContainerSSH support returning the exit status?

Yes.

## Can ContainerSSH run exec into existing containers?

No, all containers are started for a connection or session and are removed at the end. This will be a future feature.

## Can ContainerSSH deploy additional services, such as sidecar containers, etc?

ContainerSSH supports the entire Kubernetes pod specification so you can launch as many containers as you want in a single pod. The Docker backend, however, does not support sidecar containers.

## Can I use my normal kubeconfig files?

Unfortunately, no. Kubeconfig files are parsed by kubectl and the code is quite elaborate. At this time, adding it to ContainerSSH is not planned.
