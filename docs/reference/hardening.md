<h1>Hardening ContainerSSH</h1>

ContainerSSH is built to secure its inner workings as much as possible. You can take several steps to secure it further.

## Running ContainerSSH

ContainerSSH should be run as an unprivileged user (e.g. root) as it does not need access to any privileged resources. When running it from the default container image `containerssh/containerssh` this is the default.

When running it outside a container you should keep the default bind port of 2222. On Linux you can then use iptables to redirect port 22 to the unprivileged port:

```
iptables -t nat -I PREROUTING -p tcp --dport 22 -j REDIRECT --to-port 2222
```

Don't forget to add this rule to your persistent firewall configuration.

## Securing authentication

### Authentication server connection

ContainerSSH talks to an authentication server over HTTP. There are two potential attacks here:

1. If an attacker can intercept the connection between ContainerSSH and the authentication server the attacker can read the passwords for password authentication.
2. If an attacker can send requests to the authentication server they can brute force SSH passwords.

Therefore, the connection between ContainerSSH and the authentication server should be secured in the following 3 ways:

1. Implement firewalls such that only ContainerSSH can access the authentication server.
2. Only use HTTPS with certificate verification to access the authentication server and disable the HTTP port.
3. Deploy client certificates to prevent unauthorized access to the authentication server.

To maximize security it is recommended that you deploy a custom CA for the server and client certificates. The details of deploying a CA infrastructure with cfssl are described in the [authentication chapter](auth.md).

### Rate limiting

ContainerSSH contains no rate limiting for authentication across connections, this is the job of the authentication server. The number of authentication attempts within a connection is limited to 6.

The authentication server must take care to do rate limiting right: within a single connection multiple authentication attempts may be made and if the authentication server returns a non-200 response code ContainerSSH will retry connections.

It is recommended that the authentication server use the `connectionId` field to distinguish between SSH connections as this field is guaranteed to be unique for a connection.

### Client credential security

Passwords are vulnerable to being stolen and cannot be transferred to hardware keys. For the most security it is recommended to disable password authentication and only use SSH keys.

When storing SSH keys on the client computer they should be protected by a passphrase and limited permissions on the key file. 

If possible, however, SSH keys should be transferred to a hardware token like the [Yubikey](https://developers.yubico.com/PGP/SSH_authentication/). The Yubikey should be configured to require a physical touch on every authentication and should be unlocked with a passcode to prevent unauthorized applications on the client accessing the key for connections.

## Securing the configuration server

ContainerSSH can optionally reach out to a configuration server to fetch dynamic backend configuration based on the username. The backend configuration may contain secrets, such as certificates for accessing Docker and Kubernetes, or application-specific secrets. Therefore, if an attacker can access the configuration server they can extract secrets from the returned configuration.

This can be mitigated similar to the authentication server:

1. Implement firewalls such that only ContainerSSH can access the configuration server.
2. Only use HTTPS with certificate verification to access the configuration server and disable the HTTP port.
3. Deploy client certificates to prevent unauthorized access to the configuration server.

To maximize security it is recommended that you deploy a custom CA for the server and client certificates. The details of deploying a CA infrastructure with cfssl are described in the [configuration server chapter](configserver.md).

## Limiting SSH requests

The [security module](security.md) provides the ability to limit which requests are allowed from a client. As ContainerSSH is upgraded the default is to allow new features that will come in with future releases (e.g. TCP port forwarding).

In order to secure ContainerSSH for future releases it is recommended 

## Securing Docker

Docker is a hard backend to secure since access to the Docker socket automatically means privileged access to the host machine.

For maximum security Docker should be deployed on a separate host from ContainerSSH. This prevents an attacker that is able to escape a container to extract the ContainerSSH credentials for the authentication and configuration server.

### Securing the Docker socket

Since ContainerSSH should never run as root it is recommended to access the Docker socket over TCP. In order to secure the TCP connection Docker will need certificates. The detailed description of this process is described in the [Docker documentation](https://docs.docker.com/engine/security/https/)

!!! danger
    Never expose the Docker socket on TCP without configuring certificates! 

### Preventing root escalation

In order to prevent a user to become root on the host we recommend not running workloads in the container as root.

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
      readonlyRootfs: true
```

!!! danger
    If you are using the [auditlog](audit.md) make sure you put the local directory on a separate disk than the `/var/lib/docker` directory even if you don't use storage limits to prevent the audit log from getting corrupted.
    
### Preventing memory exhaustion

Users can also try to exhaust the available memory to crash the server. This can be prevented using the following configuration:

```yaml
docker:
  execution:
    host:
      resources:
        memory: 26214400
        # Soft limit
        memoryReservation: 20000000
```

The memory is specified in bytes.

In addition it is recommended to enable [cgroup swap limit support](https://docs.docker.com/engine/install/linux-postinstall/#your-kernel-does-not-support-cgroup-swap-limit-capabilities). This allows for limiting the totoal memory + swap usage:

```yaml
docker:
  execution:
    host:
      resources:
        memorySwap: 26214400
        # Tune how likely the container is to be swapped out
        memorySwappiness: 90
```

If the host still runs out of memory the OOM killer will try to kill a process to free up memory. The OOM killer can be tuned using the following options:

```yaml
docker:
  execution:
    host:
      # Disable OOM killer for this container
      oomKillDisable: true
      # Tune how likely the OOM killer is to kill this container
      oomScoreAdj: 500
```

### Preventing CPU exhaustion

A malicious user can also exhaust the CPU by running CPU-heavy workloads. This can be prevented by setting the following options:

```yaml
docker:
  execution:
    host:
      resources:
        # Limit which cores the container should run on
        cpusetCpus: 1-3,5
        # Limit which Memory nodes the container should run on (For NUMA systems)
        cpusetMems: 1-3,5
        # CPU scheduling period in microseconds
        cpuPeriod: 10000
        # CPU quota to allocate tho the container
        cpuQuota: 1000
        # As above, but for realtime tasks (guaranteed CPU time)
        cpuRealtimePeriod: 10000
        cpuRealtimeQuota: 1000
```

### Preventing process exhaustion

You can also limit the number of processes that can be launched inside the container:

```yaml
docker:
  execution:
    host:
      resources:
        pidsLimit: 1000
```

### Limiting network access

In some use cases you don't want a user to be able to access resources on the network apart from the SSH connection. This can be achieved by disabling network inside the container:

```yaml
docker:
  execution:
    host:
      networkDisabled: true
```

## Securing Kubernetes
