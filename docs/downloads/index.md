<h1>Downloads</h1>

## Latest release (0.4.0, released Apr 1, 2021)

<a href="/reference/" class="md-button">Read the reference manual &raquo;</a>

=== "Container"

    ContainerSSH can be installed in a containerized system (Kubernetes, Docker, Podman) by referencing the following image names:
    
    ```
    containerssh/containerssh:0.4
    containerssh/containerssh:0.4.0

    quay.io/containerssh/containerssh:0.4
    quay.io/containerssh/containerssh:0.4.0
    ```
    
    Our container images are built on **Alpine Linux (x86, 64 bit)**.
    
    !!! tip "Note about container image versioning"
        We provide the images with multiple version tags. `latest` will always reference the latest image build of the latest stable version. `0.4` will always reference the latest image build of the latest 0.4 version, and `0.4.0` will always reference the latest image build of 0.4.0.
        
        Each of these tags will see updates as we update the base Alpine Linux image to apply security fixes. If you need to roll back to an exact previous image you can reference the image by build date, e.g. `0.4.0-20210401`. The list of images can be found on the [Docker Hub](https://hub.docker.com/r/containerssh/containerssh/tags?page=1&ordering=last_updated&name=0.4).

=== "Linux"
    
    <a href="https://github.com/ContainerSSH/ContainerSSH/releases/download/0.4.0/containerssh_0.4.0_linux_amd64.tar.gz" class="md-button">x86 (.tar.gz)</a> <a href="https://github.com/ContainerSSH/ContainerSSH/releases/download/0.4.0/containerssh_0.4.0_linux_amd64.deb" class="md-button">x86 (.deb)</a> <a href="https://github.com/ContainerSSH/ContainerSSH/releases/download/0.4.0/containerssh_0.4.0_linux_amd64.rpm" class="md-button">x86 (.rpm)</a>

=== "MacOS"

    <a href="https://github.com/ContainerSSH/ContainerSSH/releases/download/0.4.0/containerssh_0.4.0_darwin_amd64.tar.gz" class="md-button">Intel (.tar.gz)</a>

=== "Windows"
    
    <a href="https://github.com/ContainerSSH/ContainerSSH/releases/download/0.4.0/containerssh_0.4.0_windows_amd64.zip" class="md-button">.zip</a>
    
---

## Older releases

| Version | Released | Container | Linux | Windows | MacOS |
|---------|----------|-----------|-------|---------|-------|
| 0.3.1   | Oct 23, 2020 | `containerssh/containerssh:0.3.1` | [.tar.gz](https://github.com/ContainerSSH/ContainerSSH/releases/download/0.3.1/containerssh_0.3.1_linux_amd64.tar.gz)<br />[.deb](https://github.com/ContainerSSH/ContainerSSH/releases/download/0.3.1/containerssh_0.3.1_linux_amd64.deb)<br />[.rpm](https://github.com/ContainerSSH/ContainerSSH/releases/download/0.3.1/containerssh_0.3.1_linux_amd64.rpm) | [.zip](https://github.com/ContainerSSH/ContainerSSH/releases/download/0.3.1/containerssh_0.3.1_windows_amd64.zip) | [.tar.gz](https://github.com/ContainerSSH/ContainerSSH/releases/download/0.3.1/containerssh_0.3.1_darwin_amd64.tar.gz) |
| 0.3.0   | Oct 21, 2020 | `containerssh/containerssh:0.3.0` | [.tar.gz](https://github.com/ContainerSSH/ContainerSSH/releases/download/0.3.0/containerssh_0.3.0_linux_amd64.tar.gz)<br />[.deb](https://github.com/ContainerSSH/ContainerSSH/releases/download/0.3.0/containerssh_0.3.0_linux_amd64.deb)<br />[.rpm](https://github.com/ContainerSSH/ContainerSSH/releases/download/0.3.0/containerssh_0.3.0_linux_amd64.rpm) | [.zip](https://github.com/ContainerSSH/ContainerSSH/releases/download/0.3.0/containerssh_0.3.0_windows_amd64.zip) | [.tar.gz](https://github.com/ContainerSSH/ContainerSSH/releases/download/0.3.0/containerssh_0.3.0_darwin_amd64.tar.gz) |
| 0.2.2   | Aug 2, 2020 | | [.tar.gz](https://github.com/ContainerSSH/ContainerSSH/releases/download/0.2.2/containerssh_0.2.2_linux_amd64.tar.gz)<br />[.deb](https://github.com/ContainerSSH/ContainerSSH/releases/download/0.2.2/containerssh_0.2.2_linux_amd64.deb)<br />[.rpm](https://github.com/ContainerSSH/ContainerSSH/releases/download/0.2.2/containerssh_0.2.2_linux_amd64.rpm) | [.zip](https://github.com/ContainerSSH/ContainerSSH/releases/download/0.2.2/containerssh_0.2.2_windows_amd64.zip) | [.tar.gz](https://github.com/ContainerSSH/ContainerSSH/releases/download/0.2.2/containerssh_0.2.2_darwin_amd64.tar.gz) |
| 0.2.1   | Jul 30, 2020 | | [.tar.gz](https://github.com/ContainerSSH/ContainerSSH/releases/download/0.2.1/containerssh_0.2.1_linux_amd64.tar.gz)<br />[.deb](https://github.com/ContainerSSH/ContainerSSH/releases/download/0.2.1/containerssh_0.2.1_linux_amd64.deb)<br />[.rpm](https://github.com/ContainerSSH/ContainerSSH/releases/download/0.2.1/containerssh_0.2.1_linux_amd64.rpm) | [.zip](https://github.com/ContainerSSH/ContainerSSH/releases/download/0.2.1/containerssh_0.2.1_windows_amd64.zip) | [.tar.gz](https://github.com/ContainerSSH/ContainerSSH/releases/download/0.2.1/containerssh_0.2.1_darwin_amd64.tar.gz) |
| 0.2.0   | Jul 9, 2020 | | [.tar.gz](https://github.com/ContainerSSH/ContainerSSH/releases/download/0.2.0/containerssh_0.2.0_linux_amd64.tar.gz)<br />[.deb](https://github.com/ContainerSSH/ContainerSSH/releases/download/0.2.0/containerssh_0.2.0_linux_amd64.deb)<br />[.rpm](https://github.com/ContainerSSH/ContainerSSH/releases/download/0.2.0/containerssh_0.2.0_linux_amd64.rpm) | [.zip](https://github.com/ContainerSSH/ContainerSSH/releases/download/0.2.0/containerssh_0.2.0_windows_amd64.zip) | [.tar.gz](https://github.com/ContainerSSH/ContainerSSH/releases/download/0.2.0/containerssh_0.2.0_darwin_amd64.tar.gz) |
| 0.1.1   | Jul 9, 2020 | | [.tar.gz](https://github.com/ContainerSSH/ContainerSSH/releases/download/0.1.1/containerssh_0.1.1_linux_amd64.tar.gz)<br />[.deb](https://github.com/ContainerSSH/ContainerSSH/releases/download/0.1.1/containerssh_0.1.1_linux_amd64.deb)<br />[.rpm](https://github.com/ContainerSSH/ContainerSSH/releases/download/0.1.1/containerssh_0.1.1_linux_amd64.rpm) | [.zip](https://github.com/ContainerSSH/ContainerSSH/releases/download/0.1.1/containerssh_0.1.1_windows_amd64.zip) | [.tar.gz](https://github.com/ContainerSSH/ContainerSSH/releases/download/0.1.1/containerssh_0.1.1_darwin_amd64.tar.gz) |
| 0.1.0   | Jun 18, 2020 | | [.tar.gz](https://github.com/ContainerSSH/ContainerSSH/releases/download/0.1.0/containerssh_0.1.0_linux_amd64.tar.gz)<br />[.deb](https://github.com/ContainerSSH/ContainerSSH/releases/download/0.1.0/containerssh_0.1.0_linux_amd64.deb)<br />[.rpm](https://github.com/ContainerSSH/ContainerSSH/releases/download/0.1.0/containerssh_0.1.0_linux_amd64.rpm) | [.zip](https://github.com/ContainerSSH/ContainerSSH/releases/download/0.1.0/containerssh_0.1.0_windows_amd64.zip) | [.tar.gz](https://github.com/ContainerSSH/ContainerSSH/releases/download/0.1.0/containerssh_0.1.0_darwin_amd64.tar.gz) |

!!! note
    Container images that no longer have pulls have been removed to conserve resources.