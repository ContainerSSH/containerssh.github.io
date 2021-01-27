{{ outdated() }}

<h1>Building a container image for ContainerSSH</h1>

ContainerSSH can run any Linux container image. However, it is strongly recommended that you install the [ContainerSSH guest agent](https://github.com/containerssh/agent) into the image to make all features available.

If you wish to use SFTP you have to add an SFTP server (`apt install openssh-sftp-server` on Ubuntu) to the container
image and configure the path of the SFTP server correctly in your config.yaml. The sample image
`containerssh/containerssh-guest-image` contains an SFTP server.
