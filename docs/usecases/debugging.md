title: Debugging a production environment

## Problem

Granting developer access to a production system is often problematic or even impossible if accurate record-keeping is required.

1. Access to production systems should be restricted on an as-needed basis, not all developers should have access to it.
2. Auditing changes to a production system is a must.

## What a traditional setup looks like

1. Only a limited number of system administrators have access.
2. Changes can only be made using a CI system.
3. Debugging involves several people.
4. Audit logging is limited or non-existent.
5. Sometimes, PAM is used for dynamic user databases, which increases complexity.

## How ContainerSSH helps

1. Dynamically allow users access based on automation from your ticketing system or web interface.
2. Audit log every SSH command and file uploads accurately.
3. Create narrowly-scoped containers with read only access.
4. No PAM modifications needed, no access to the host operating system.

## How to build it

The goal is that developers get time-limited access to the production environment. In our case, we will configure ContainerSSH to authenticate against [OpenPolicyAgent](https://www.openpolicyagent.org/) or your [custom authentication server](../reference/auth.md). 

First, [install ContainerSSH with a base setup](../reference/installation.md). Configure the backend to [Docker](../reference/docker.md) or [Kubernetes](../reference/kubernetes.md) as desired. Please read the "Securing Docker" or "Securing Kubernetes" sections for your environment.

When a developer requests access via a ticket or web interface, use automation to create a user entry in the OPA JSON file, or a database for the current access. (You can use [external data](https://www.openpolicyagent.org/docs/latest/external-data/) with OPA to use an external database.) Now, [configure ContainerSSH](../reference/auth.md) to send authentication requests to your OPA instance or custom server.

Now, make sure that the container image contains all the debugging tools you need for your system, such as a database client. See [the image creation reference manual for details](../reference/image.md).

Next, [configure audit logging in ContainerSSH](../reference/audit.md). This will record every interaction your developers make.

Optionally, you can also add a [dynamic configuration server](../reference/configserver.md) to provision dynamic user credentials for the current access, or create a per-user container configuration, such as mounting their home volume.
