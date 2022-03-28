title: Dynamic lab environment

## Problem

In a lab environment you want to give SSH access to several people: students, contractors, etc. There are several requirements:

1. **Authentication:** Each user should be able to log in with their own username and password or SSH key, and only get access to their own environment.
2. **Resource restriction:** The environment should be resource-restricted, one user should not be able to use up all system resources.
3. **Cleanup:** When a user logs out the environment should be cleaned up.
4. **Monitoring:** The activities of the user should be monitored.

## How a traditional setup looks like

1. **Authentication:** Authentication is done by creating system users, either directly or via a PAM integration. SSH key-based authentication is difficult or impossible to manage, depending on the requirements.
2. **Resource restriction:** Resource restrictions are difficult or even impossible to implement.
3. **Cleanup:** The environment is not cleaned up after a user, the servers need to be reinstalled frequently.
4. **Monitoring:** Basic login monitoring is provided by the system, more advanced logging is difficult.

## How ContainerSSH helps

1. **Authentication:** ContainerSSH natively talks to an external authentication provider via webhooks.
2. **Resource restriction:** Each user container can be configured with resource restrictions for CPU, memory, disk IO, and network, depending on the capabilities of the backend (Docker, Kubernetes, etc).
3. **Cleanup:** ContainerSSH launches ephemeral containers that are removed when the user logs out. Persistent volumes can be mounted for each user dynamically.
4. **Monitoring:** ContainerSSH has a detailed audit log that is able to record everything that goes on via SSH, including file transfers.

## How to build it

As a first step, decide on a backend: Kubernetes is more scalable, but requires more work to get going. Docker is less scalable, but provides more capabilities for resource restriction out of the box.

Next, you will need to build an authentication server. This server is a simple webhook that authenticates your users. The simplest method is using [Open Policy Agent](https://www.openpolicyagent.org/), but  you can roll your own too. Check the [OPA example](https://github.com/ContainerSSH/examples/tree/main/opa) for an example on how to set this up. We have a full [reference manual](../reference/auth.md) on building and configuring the authentication webhook.

Finally, you will have to build a configuration server. This is also a webhook, and lets you configure the container for each user. You can also do this with OPA, or write your own. Most importantly, you will want to **mount the home directory of each user** for persistent data storage. Optionally, you may also want to create a container image and add your own tools. See the [config webook](../reference/configserver.md) and [building your own image](../reference/image.md) reference manuals for details.

You may also want to add resource restrictions to the configuration webhook. See the [Kubernetes](../reference/kubernetes.md#securing-kubernetes) and [Docker](../reference/docker.md#securing-docker) reference manuals for detailed security guides.

Once you have all components, please follow the [installation reference manual](../reference/installation.md) on deploying ContainerSSH.
