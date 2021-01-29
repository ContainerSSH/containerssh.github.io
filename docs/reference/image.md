<h1>Building a container image for ContainerSSH</h1>

ContainerSSH can run any Linux container image. However, it is strongly recommended that you install the [ContainerSSH guest agent](https://github.com/containerssh/agent) into the image to make all features available.

If you wish to use SFTP you have to add an SFTP server (`apt install openssh-sftp-server` on Ubuntu) to the container image and configure the path of the SFTP server correctly in your config.yaml. The sample image `containerssh/containerssh-guest-image` contains an SFTP server.

## Integrating the guest agent

=== "Using the base image (recommended)"

    This method uses the `containerssh/agent` container image as part of a multistage build:
    
    ```
    FROM containerssh/agent AS agent
    
    FROM your-base-image
    COPY --from=agent /usr/bin/containerssh-agent /usr/bin/containerssh-agent
    # Your other build commands here
    ```

=== "Installing on Debian/Ubuntu"

    We have a [Debian repository](https://packages.containerssh.io) containing the agent package. Once you have set up the repository you can install the agent like this:
    
    ```bash
    apt-get install containerssh-agent
    ```

=== "Installing the binaries"

    To use this method go to the [latest release from the releases section](https://github.com/ContainerSSH/agent/releases) and verify it against our [https://containerssh.io/gpg.txt](https://containerssh.io/gpg.txt) key (`3EE5B012FA7B400CD952601E4689F1F0F358FABA`).
    
    On an Ubuntu image build this would involve the following steps:
    
    ```Dockerfile
    ARG AGENT_GPG_FINGERPRINT=3EE5B012FA7B400CD952601E4689F1F0F358FABA
    ARG AGENT_GPG_SOURCE=https://containerssh.io/gpg.txt
    
    RUN echo "\e[1;32mInstalling ContainerSSH guest agent...\e[0m" && \
        DEBIAN_FRONTEND=noninteractive apt-get -o Dpkg::Options::='--force-confold' update && \
        DEBIAN_FRONTEND=noninteractive apt-get -o Dpkg::Options::='--force-confold' -fuy --allow-downgrades --allow-remove-essential --allow-change-held-packages install gpg && \
        wget -q -O - https://api.github.com/repos/containerssh/agent/releases/latest | grep browser_download_url | grep -e "agent_.*_linux_amd64.deb" | awk ' { print $2 } ' | sed -e 's/"//g' > /tmp/assets.txt && \
        wget -q -O /tmp/agent.deb $(cat /tmp/assets.txt |grep -v .sig) && \
        wget -q -O /tmp/agent.deb.sig $(cat /tmp/assets.txt |grep .sig) && \
        wget -q -O - $AGENT_GPG_SOURCE | gpg --import && \
        echo -e "5\ny\n" | gpg --command-fd 0 --batch --expert --edit-key $AGENT_GPG_FINGERPRINT trust && \
        test $(gpg --status-fd=1 --verify /tmp/agent.deb.sig /tmp/agent.deb | grep VALIDSIG | grep $AGENT_GPG_FINGERPRINT | wc -l) -eq 1 && \
        dpkg -i /tmp/agent.deb && \
        rm -rf /tmp/* && \
        rm -rf ~/.gnupg && \
        DEBIAN_FRONTEND=noninteractive apt-get -o Dpkg::Options::='--force-confold' -fuy --allow-downgrades --allow-remove-essential --allow-change-held-packages remove gpg && \
        DEBIAN_FRONTEND=noninteractive apt-get -o Dpkg::Options::='--force-confold' -y clean && \
        /usr/bin/containerssh-agent -h
    ```
    
    You can look at the default [guest image Dockerfile](https://github.com/containerssh/guest-image) for an example on Ubuntu.