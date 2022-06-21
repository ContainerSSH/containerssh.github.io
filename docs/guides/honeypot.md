# Creating a honeypot with ContainerSSH

This guide will lead you through the steps of creating an SSH honeypot with ContainerSSH.

!!! danger
    Creating SSH honeypots with a real Linux backend is inherently dangerous. Any local privilege escalation could lead to the attacker taking over your host system. While this tutorial represents the best practices in building a honeypot, the responsibility of securing your installation ultimately rests upon you. **Please do not attempt this unless you are intimately familiar with securing container environments.** [Docker has really good documentation on this topic.](https://docs.docker.com/engine/security/)
    
## Step 1: Infrastructure

In order to set up a honeypot securely you will need at least two hosts: one to run ContainerSSH and the second to run the container infrastructure the attacker is dropped into. We'll call the first host the `gateway` VM and the second one `sacrificial` VM. Ideally, the `sacrificial` VM should run on its own dedicated physical hardware to prevent leakage of secrets due to CPU bugs. Both VMs need sufficient disk space to hold audit logs and containers.

Furthermore, you will need an S3-compatible object storage to upload [audit logs](../reference/audit.md) and we will need a [Prometheus](https://prometheus.io/) installation for monitoring.

We strongly recommend automating the setup with a tool like [Terraform](https://terraform.io) to rapidly apply security updates.

## Step 2: Firewalling the gateway

You should set up the `gateway` host in such a way that it is visible from the Internet. You will need the following firewall rules:

- Port `22` should be open to the Internet.
- Ports `9100` and `9101` should be open from your Prometheus instance. These will be used by the [Prometheus node exporter](https://github.com/prometheus/node_exporter) and the [ContainerSSH metrics server](https://containerssh.io/reference/metrics/) respectively.
- Outbound rules to your S3-compatible object storage.

## Step 3: Firewalling the sacrificial host

The `sacrificial` host should not have any public Internet connectivity, instead it should only be connected to the `gateway` host. In order to keep this host up to date a prebuilt VM image with Docker installed should be used. The update process of this VM image can be automated using tools like [Packer](https://www.packer.io/).

On the firewall side, the sacrificial host should not allow any outbound connections and only allow inbound connections on TCP port 2376 from the `gateway` host.

## Step 4: Creating certificates for authentication on the sacrificial host

The next step involves creating a CA infrastructure so ContainerSSH can authenticate against the Docker daemon on the sacrificial host. This is described in the [Docker manual](https://docs.docker.com/engine/security/protect-access/#use-tls-https-to-protect-the-docker-daemon-socket).

Once your Docker socket is exposed you should test if it can be accessed without certificates. Running the following two commands from the gateway host without configuring the certificates should fail:

```
docker -H tcp://your-sacrificial-host:2375 run -ti ubuntu
docker -H tcp://your-sacrificial-host:2376 run -ti ubuntu
```

If this command does not fail the certificates have not been set up correctly.

## Step 5: Installing the node exporter

On the gateway host you will need to install the [Prometheus node exporter](https://github.com/prometheus/node_exporter) to make metrics such as disk space usage available to your monitoring system. Please read [their readme on how to do this](https://github.com/prometheus/node_exporter/blob/master/README.md).

## Step 6: Building the guest image

Since our sacrificial host will have no internet access you will need to upload the [guest image files](https://github.com/ContainerSSH/guest-image). You can do this by exporting the image using `docker export`, then uploading the tar file to the host and using `docker import` to import it into the Docker daemon.

Optionally, you can build your custom image and create an `ubuntu` user in the image to give the attacker a more realistic system.

## Step 7: Creating the ContainerSSH configuration file

Finally, we can create the ContainerSSH configuration file on the gateway host. Let's create a few directories:

```
mkdir -p /srv/containerssh/config/
mkdir -p /srv/containerssh/audit/
```

Then we generate the host key. This should be written in `/srv/containerssh/ssh_host_rsa_key`.

```
openssl genrsa
```

Then we can create the config file in `/srv/containerssh/config.yaml`

```yaml
log:
  level: warning
ssh:
  banner: |

    ********************************************************************
                               Warning!
    ********************************************************************

    This is a honeypot. All information, including IP address, username,
    password, any commands you type, or files you upload will be visible
    to the honeypot.

    If you do not agree disconnect now.

    ********************************************************************

  hostkeys:
    - /etc/containerssh/ssh_host_rsa_key
backend: docker
docker:
  connection:
    host: tcp://SACRIFICIAL-HOST-IP:2376
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
  execution:
    imagePullPolicy: Never
    container:
      image: containerssh/test-guest
      hostname: bitcoin
      # Disable network in the container
      networkdisabled: true
      # Force running as user 1000
      user: 1000
      # Optionally set working directory
      workingdir: /home/ubuntu
    host:
      # Don't let the attacker write to the root FS.
      readonlyrootfs: true
      resources:
        # 10% of CPU
        cpuperiod: 10000
        cpuquota: 1000
        # 50 MB of memory with swap
        memoryswap: 52428800
        memoryswappiness: 50
        # 25 MB of memory
        memory: 26214400
        # Reserve 20 MB of memory
        memoryreservation: 20000000
        # Max 1000 processes to prevent fork bombs
        pidslimit: 1000
      tmpfs:
        # Create writable directories in memory
        /tmp: rw,noexec,nosuid,size=65536k,uid=1000,gid=1000
        /run: rw,noexec,nosuid,size=65536k,uid=1000,gid=1000
        /home/ubuntu: rw,noexec,nosuid,size=65536k,uid=1000,gid=1000
metrics:
  enable: true
  listen: "0.0.0.0:9101"
  path: "/metrics"
audit:
  enable: true
  format: binary
  storage: s3
  intercept:
    stdin: true
    stdout: true
    stderr: true
    passwords: true
  s3:
    # Local directory to store the audit log temporarily.
    local: /var/log/containerssh/audit/
    accessKey: YOUR-S3-ACCESS-KEY-HERE
    secretKey: YOUR-S3-SECRET-KEY-HERE
    region: YOUR-S3-REGION
    bucket: YOUR-S3-BUCKET-NAME
    # Optional: set your S3 endpoint
    endpoint: https://YOUR-S3-ENDPOINT
    metadata:
      # Which metadata fields to set in the object storage.
      username: true
      ip: false
auth:
  url: "http://127.0.0.1:8080"
configserver:
  url: "http://127.0.0.1:8080/config"
```

## Step 7: Starting ContainerSSH

Now you are ready to start ContainerSSH:

```
docker run -d \
  --restart=always \
  -v /srv/containerssh/:/etc/containerssh/ \
  -v /srv/containerssh/audit/:/var/log/containerssh/audit/ \
  --net=host \
  containerssh/containerssh:0.4.1
```

## Step 8: Starting the auth-config server

Next, we'll need the auth-config server to let the users in:

```
docker run -d \
  --restart=always \
  -p 127.0.0.1:8080:8080 \
  -e CONTAINERSSH_ALLOW_ALL=1 \
  containerssh/containerssh-test-authconfig:0.4.1
```

## Step 9: Redirecting port 22

As a final step we will need to redirect port 22 to port 2222:

```
iptables -t nat -I PREROUTING -p tcp --dport 22 -j REDIRECT --to-port 2222
```

You will need to use the firewall facilities of your OS to make this rule persistent.

## Step 10: Setting up monitoring

Please set up monitoring for both the host metrics (such as disk space usage) and [ContainerSSH itself](https://containerssh.io/reference/metrics/) in your Prometheus instance.

## Further hardening

This creates a honeypot that lets attackers access a container. However, in a real world scenario you may want to integrate micro virtual machines instead of containers for better security, such as [Firecracker](https://firecracker-microvm.github.io/). Alternatively, you may want to investigate tools like [gVisor](https://github.com/google/gvisor) which implement a separate security layer for your container. This is beyond the scope of this guide.
