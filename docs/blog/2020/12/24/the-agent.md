---
title: Announcing the ContainerSSH Guest Agent
description: The new ContainerSSH guest agent will level the playing field across container backends.
image: images/blog/the-agent/preview.png
---

ContainerSSH is an integration project between the SSH library and the Docker and Kubernetes API. However, neither the Docker nor the Kubernetes API have been designed to host some of the more intricate SSH specific features.

For example, the Kubernetes "attach" API does not allow for retrieving the output of the command running in the container that happened before attaching reliably,and neither Docker nor Kubernetes allow sending signals to commands running in an "exec", etc.

We won't go into details on these various issues, suffice it to say, some of them break the expectations you would have for a classic SSH server. There are two paths ahead of us: either try to send pull requests to the Docker and Kubernetes projects to patch these features in, or add a guest agent to the container images that enable these extra features.

Sending in patches to enable all the functionality would be a very long process and chances are that our patches wouldn't be accepted as they add additional functionality that is, admittedly, fringe for most users. Therefore, we opted to [build a guest agent](https://github.com/containerssh/agent).

The ContainerSSH guest agent is a binary containing only minimal functionality and no external dependencies that can easily be added to any container image as a single binary. We have already added it to the default `containerssh/containerssh-guest-image` and **we encourage users who built their own image to include the agent as well** and keep it updated. Please see [github.com/containerssh/agent](https://github.com/containerssh/agent) for details.

That being said, the guest image is and will be optional. It will be a feature that needs to be explicitly enabled in the configuration. **Guest agent support will arrive in ContainerSSH 0.4** after the holidays.

Merry Christmas and Happy Holidays!
