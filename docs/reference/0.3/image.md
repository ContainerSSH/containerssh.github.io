
{{ reference_outdated() }}

<h1>Building a container image for ContainerSSH</h1>

ContainerSSH can run any Linux container image.

If you wish to use SFTP you have to add an SFTP server (`apt install openssh-sftp-server` on Ubuntu) to the container image and configure the path of the SFTP server correctly in your config.yaml. The sample image `containerssh/containerssh-guest-image` contains an SFTP server.
