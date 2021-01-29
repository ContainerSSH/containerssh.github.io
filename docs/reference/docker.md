<h1>The Docker backend</h1>

The Docker backend should work with any Docker Engine version starting with 1.6 thanks to the version negotiation present. We fix issues starting with Docker version 18.02.

!!! tip
    This is the documentation for the **Docker backend**. For deploying ContainerSSH inside Docker please see the [installation guide](installation.md).

## The base configuration structure

In order to use the Docker backend you must specify the following configuration entries via the configuration file or the configuration server:

```yaml
backend: docker
docker:
  connection:
    <connection configuration here>
  execution:
    <execution configuration here>
  timeouts:
    <timeouts configuration here>
```

## Configuring connection parameters

The Docker backend defaults to connecting to the Docker Engine using the Docker socket. The default location for this is on UNIX systems is `unix:///var/run/docker.sock`, on Windows `npipe:////./pipe/docker_engine`. ContainerSSH must have permissions to access the Docker socket.

The Docker socket location can be changed with the `host` option:

```yaml
docker:
  connection:
    host: 127.0.0.1:2375
```

However, **exposing Docker without certificate authentication is dangerous**. It is recommended to [generate a certificate for authentication](https://docs.docker.com/engine/security/https/) and pass it to ContainerSSH using the following options:

```yaml
docker:
  connection:
    host: <ip and port of the Docker engine>
    cert: |
      -----BEGIN CERTIFICATE-----
      <client certificate here>
      -----END CERTIFICATE-----
    key: |
      -----BEGIN RSA PRIVATE KEY-----
      <client key here>
      -----END RSA PRIVATE KEY-----
    cacert: |
      -----BEGIN CERTIFICATE-----
      <CA certificate here>
      -----END CERTIFICATE-----
```

## Configuring container execution

Container execution options can be specified as follows:

```yaml
docker:
  execution:
    container:
      image: containerssh/containerssh
      <other container options>
    host:
      <host options>
    network:
      <network options>
    platform:
      <platform options>
    containerName: "<container name here>"
    <ContainerSSH-specific options here>
```

The `container`, `host`, `network`, and `platform` options contain settings described in the [Docker API](https://docs.docker.com/engine/api/v1.41/#operation/ContainerCreate).

The `containerName` option contains the name for the container. If the a container already exists with the same name the container creation will fail, so this should be left empty for most use cases.

### Basic container configuration

The basic configuration options are as follows:

```yaml
docker:
  execution:
    container:
      image: containerssh/containerssh
      env:
        - VAR=value
      # cmd is only respected in session mode, see below.
      cmd: 
        - /run/this/command
      user: ubuntu
```

### Mounting volumes

Volumes can be mounted in 3 ways:

1. Using bind mounts
2. Using mounts
2. Using tmpfs

#### Bind mounts

**Bind mounts** mount a directory from the host into the container. The syntax is fairly simple:

```yaml
docker:
  execution:
    host:
      binds:
        - "/path-on-the-host:/path-in-the-container[:options]"
```

Instead of the host path you can also specify a volume name. The following options are suported:

`nocopy`
: If you set this flag Docker will not automatically copy the data that exists in the container image to the volume on mounting.

`ro|rw`
: Set volume to read-only or read-write.

`z`
: Apply the `shared` SELinux label to the volume allowing multiple containers to write the same volume.

`Z`
: Apply the `private unshared` SELinux label to the volume allowing only the current container to use it.

`[r]shared, [r]slave, [r]private`
: Sets the [mount propagation](https://www.kernel.org/doc/Documentation/filesystems/sharedsubtree.txt) behavior of the volume.

#### Mounts

The **mounts** option give you more flexibility to mount something, including using a volume driver. This is especially useful when mounting a volume from an external storage, for example NFS. It can be configured as follows:

```yaml
docker:
  execution:
    host:
      mounts:
        - target: /path/in/container
          source: <volume name, host path, etc>
          type: <bind|volume|tmpfs|npipe>
          readonly: <true|false>
          consistency: <default|consistent|cached|delegated>
          # For bind type only:
          bindoptions:
            propagation: <private|rprivate|shared|rshared|slave|rslave>
            #Disable recursive bind mount
            nonrecursive: <true|false>
          # For volume type only:
          volumeoptions: 
            # Disable copying files from the image to the volume
            nocopy: <true|false> 
            labels:
              - key: value
            driverconfig:
              name: drivername
              options:
                <driveroption>: <drivervalue>
          # For tmpfs type only:
          tmpfsoptions:
            sizebytes: <size in bytes>
            mode: 0755
```

## tmpfs

The tmpfs method provides a temporary filesystem in memory. The contents are deleted when the container is removed.

```yaml
docker:
  execution:
    host:
      tmpfs:
        /container/directory: <options>
```

The detailed options for tmpfs can be found on the [tmpfs man page](https://man7.org/linux/man-pages/man5/tmpfs.5.html).

### Other options

Apart from the `container`, `host`, `network`, `platform` and `containerName` options ContainerSSH has the following options for execution. These should not be changed unless required.

| Name | Type | Description |
|------|------|-------------|
| `mode` | `string` | Specify `connection` to launch one container per SSH connection or `session` to run one container per SSH session (multiple containers per connection). In connection mode the container is started with the `idleCommand` as the first program and every session is launched similar to how `docker exec` runs programs. In session mode the command is launched directly. | 
| `idleCommand` | `[]string` | Specifies the command to run as the first process in the container in `connection` mode. Parameters must be provided as separate items in the array. Has no effect in `session` mode. |
| `shellCommand` | `[]string` | Specifies the command to run as a shell in `connection` mode. Parameters must be provided as separate items in the array. Has no effect in `session` mode. |
| `agentPath` | `string` | Contains the full path to the [ContainerSSH guest agent](https://github.com/containerssh/agent) inside the shell container. The agent must be installed in the guest image. |
| `disableAgent` | `bool` | Disable the ContainerSSH guest agent. This will disable several functions and is *not recommended*. |
| `subsystems | `map[string]string` | Specifies a map of subsystem names to executables. It is recommended to set at least the `sftp` subsystem as many users will want to use it. |
| `imagePullPolicy` | `Never,IfNotPresent,Always` | Specifies when to pull the container image. Defaults to `IfNotPresent`, which pulls the image when it is not locally present *or* if the image has no tag/has the `latest` tag. It is recommended that you provide a custom, versioned image name to prevent pulling the image at every connection. |

## Configuring timeouts

The `timeouts` section has the following options. All options can use time units (e.g. `60s`) and default to nanoseconds without time units.

| Name | Description |
|------|-------------|
| `containerStart` | The time to wait for the container to start. |
| `containerStop` | The time to wait for the container to stop. |
| `commandStart` | The time to wait for the command to start in `connection` mode. |
| `signal` | The time to wait to deliver a signal to a process. |
| `window` | The time to wait to deliver a window size change. |
| `http` | The time to wait for the underlying HTTP calls to complete. |

## Securing Docker

Docker is a hard backend to secure since access to the Docker socket automatically means privileged access to the host machine.

For maximum security Docker should be deployed on a separate host from ContainerSSH. This prevents an attacker that is able to escape a container to extract the ContainerSSH credentials for the authentication and configuration server.

### Securing the Docker socket

Since ContainerSSH should never run as root it is recommended to access the Docker socket over TCP. In order to secure the TCP connection Docker will need certificates. The detailed description of this process is described in the [Docker documentation](https://docs.docker.com/engine/security/https/).

The certificates can be provided for ContainerSSH using the following fields:

```yaml
docker:
  connection:
    host: <ip and port of the Docker engine>
    cert: |
      -----BEGIN CERTIFICATE-----
      <client certificate here>
      -----END CERTIFICATE-----
    key: |
      -----BEGIN RSA PRIVATE KEY-----
      <client key here>
      -----END RSA PRIVATE KEY-----
    cacert: |
      -----BEGIN CERTIFICATE-----
      <CA certificate here>
      -----END CERTIFICATE-----
```

!!! danger
    Never expose the Docker socket on TCP without configuring certificates! 

### Preventing root escalation

Under normal circumstances a user running as root inside a container cannot access resources outside the container. However, in the event of a container escape vulnerability in Docker it is prudent not to run container workloads as root. For example, you can set the container to run at uid `1000` as follows:

```yaml
docker:
  execution:
    container:
      user: 1000
```

If root is required inside the container [user namespace mapping](https://docs.docker.com/engine/security/userns-remap/). There are a few steps required to make this happen:

First, you need to create the files called `/etc/subuid` and `/etc/subgid`. These files have the following format:

```
<username/uid>:<startuid/gid>:<uid/gid count>
```

For example:

```
1000:1000:65536
``` 

In this case the first UID is the UID outside of the container being mapped, the second UID is the starting UID that will map to the root user inside the container, and the third is the number of UIDs inside the container. This is the same for group IDs.

!!! tip
    Using a UID instead of a username in the first field of the mapping will cause a significant performance increase when parsing the file. 

Then you can configure Docker to use this subordinate UID. This can be done by either configuring the Docker daemon or by configuring ContainerSSH to use this mapping.

To configure the Docker daemon you can pass the following parameter to `dockerd`:

```bash
dockerd --userns-remap="<UID>:<GID>"
```

Alternatively, you can configure this per-container in ContainerSSH:

```yaml
docker:
  execution:
    host:
      usernsmode: <UID>:<GID>
```

In both cases the passed UID and GID must map to the entries in `/etc/subuid` and `/etc/subgid`.

!!! warning
    Using a large number of mappings (10k or more) will cause a performance penalty.

### Preventing storage exhaustion

A malicious user could cause the Docker host to run out of disk space with a simple attack:

```bash
cat /dev/zero > ~/zerofill
```

There are two cases here:

If **the directory** the user can write to **is mounted using a volume** the attacker can fill up the storage that is mounted. You can pass per-user mounts from the [configuration server](configserver.md) that mount volumes that are unique to the connecting user. This way the user can only fill up their own disk. The specific implementation depends on your volume driver.

If **the directory** the user can write to **is not mounted** the user can fill up the container image. This is a much more subtle way of filling up the disk and can only be mitigated partially as limiting disk space per-container is not supported in every backend configuration. You can enable storage limits in ContainerSSH like this:

```yaml
docker:
  execution:
    host:
      storageopt:
        size: 524288000
```

However, make sure to test if this works on your Docker configuration. When using `overlayfs2` on an `ext4` filesystem this does not work, you may have to switch to `xfs` or move to `devicemapper` to make use of this option.

Some directories, such as `/tmp` or `/run` can also be put on tmpfs to store in memory. This can be configured as follows:

```yaml
docker:
  execution:
    host:
      tmpfs:
        /tmp: rw,noexec,nosuid,size=65536k
        /run: rw,noexec,nosuid,size=65536k
```

To prevent storage exhaustion it is recommended to set the root FS to be read only:

```yaml
docker:
  execution:
    host:
      readonlyrootfs: true
```

!!! danger
    If you are using the [auditlog](audit.md) make sure you put the local directory on a separate disk than the `/var/lib/docker` directory even if you don't use storage limits to prevent the audit log from getting corrupted.
    
### Preventing memory exhaustion

Users can also try to exhaust the available memory to potentially crash the server. This can be prevented using the following configuration:

```yaml
docker:
  execution:
    host:
      resources:
        memory: 26214400
        # Soft limit
        memoryreservation: 20000000
```

The memory is specified in bytes.

In addition it is recommended to enable [cgroup swap limit support](https://docs.docker.com/engine/install/linux-postinstall/#your-kernel-does-not-support-cgroup-swap-limit-capabilities). This allows for limiting the totoal memory + swap usage:

```yaml
docker:
  execution:
    host:
      resources:
        memoryswap: 26214400
        # Tune how likely the container is to be swapped out
        memoryswappiness: 90
```

If the host still runs out of memory the OOM killer will try to kill a process to free up memory. The OOM killer can be tuned using the following options:

```yaml
docker:
  execution:
    host:
      # Tune how likely the OOM killer is to kill this container
      oomscoreadj: 500
      resources:
          # Disable OOM killer for this container
          oomkilldisable: true
```

### Preventing CPU exhaustion

A malicious user can also exhaust the CPU by running CPU-heavy workloads. This can be prevented by setting the following options:

```yaml
docker:
  execution:
    host:
      resources:
        # Limit which cores the container should run on
        cpusetcpus: 1-3,5
        # Limit which Memory nodes the container should run on (For NUMA systems)
        cpusetmems: 1-3,5
        # CPU scheduling period in microseconds
        cpuperiod: 10000
        # CPU quota to allocate tho the container
        cpuquota: 1000
        # As above, but for realtime tasks (guaranteed CPU time)
        cpurealtimeperiod: 10000
        cpurealtimequota: 1000
```

### Preventing process exhaustion

You can also limit the number of processes that can be launched inside the container:

```yaml
docker:
  execution:
    host:
      resources:
        pidslimit: 1000
```

### Limiting network access

In some use cases you don't want a user to be able to access resources on the network apart from the SSH connection. This can be achieved by disabling network inside the container:

```yaml
docker:
  execution:
    host:
      networkDisabled: true
```

### Limiting disk I/O

Docker has a built-in facility to limit the disk I/O by IOPS and by bytes per second. This can be done using the following configuration structure:

```yaml
docker:
  execution:
    host:
      resources:
        # Set relative weight against other containers
        blkioweight: <weight number> 
        # Set relative weight against other containers
        blkioweightdevice:
          - path: <device path>
            weight: <weight number>
        # Read BPS
        blkiodevicereadbps:
          - path: <device path>
            rate: <bytes per second>
        # Write BPS
        blkiodevicewritebps:
          - path: <device path>
            rate: <bytes per second>
        # Read IOps
        blkiodevicereadiops:
          - path: <device path>
            rate: <IO per second>
        # Write IOps
        blkiodevicewriteiops:
          - path: <device path>
            rate: <IO per second>
```

The **device path** has to be a path to a **block device**, e.g. `/dev/vda`. It does not work on filesystems or character devices.