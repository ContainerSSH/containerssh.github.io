<h1>The Kubernetes backend</h1>

The Kubernetes backend runs and is tested against all [currently actively maintained Kubernetes versions](https://kubernetes.io/docs/setup/release/version-skew-policy/).
For ContainerSSH version 0.4 these are: 1.20, 1.19, and 1.18.

!!! tip
    This is the documentation for the **Kubernetes backend**. For deploying ContainerSSH inside Kubernetes please see the [installation guide](installation.md).

## The base configuration structure

In order to use the Kubernetes backend you must specify the following configuration entries via the configuration file or the configuration server:

```yaml
backend: kubernetes
kubernetes:
  connection:
    <connection configuration here>
  pod:
    <pod configuration here>
  timeouts:
    <timeouts configuration here>
``` 

## Configuring connection parameters

In order to use Kubernetes you must provide the credentials to authenticate with the Kubernetes cluster. There are several supported authentication methods:

- Username and password (HTTP basic auth).
- x509 client certificates.
- Bearer token.

These options should be specified like this:

```yaml
kubernetes:
  connection:
    host: <...>
    <...>
```

!!! tip
    See the [Securing Kubernetes section below](#securing-kubernetes) for a detailed walkthrough for provisioning limited service accounts for ContainerSSH.

### Base configuration

| Name | Type | Description |
|------|------|-------------|
| `host` | `string` | The hostname or ip + the port of the Kubernetes API server. Set this to `kubernetes.default.svc` to run inside a Kubernetes cluster, otherwise set it to the host name of your Kubernetes API. |
| `path` | `string` | This is the API path of the Kubernetes API. Defaults to `/api` and you will typically not need to change this. |
| `cacertFile` | `string` | Points to the file that contains the CA certificate in PEM format that signed the server certificate. |
| `cacert` | `string` | Directly contains the CA certificate in PEM format that signed the server certificate. |
| `serverName` | `string` | Sets the hostname of the server that should be sent to the Kuberentes API in the TLS SNI. This is useful when the Kubernetes API has a hostname that is not resolvable from the server ContainerSSH is running on. |
| `insecure` | `bool` | Disable certificate verification on the Kubernetes API. **This is a very bad idea** as anyone on the network will be able to intercept your credentials. |
| `qps` | `float32` | Indicates a maximum queries per second from this client. |
| `burst` | `int` | Indicates the maximum burst for query throttling. |

### HTTP basic authentication (username and password)

| Name | Type | Description |
|------|------|-------------|
| `username` | `string` | Username for authenticating against the Kubernetes API. This is only used for HTTP basic auth and does not work with other authentication methods (e.g. OAuth2) |
| `password` | `string` | Password for authenticating against the Kubernetes API. This is only used for HTTP basic auth and does not work with other authentication methods (e.g. OAuth2) |

### x509 certificate authentication

| Name | Type | Description |
|------|------|-------------|
| `certFile` | `string` | Points to a file that contains the client certificate for x509 authentication against the Kubernetes API in PEM format. |
| `cert` | `string` | Directly contains the certificate for x509 authentication against the Kubernetes API in PEM format. |  
| `keyFile` | `string` | Points to a file that contains the client key for x509 authentication against the Kubernetes API in PEM format. |
| `key` | `string` | Directly contains the client key for x509 authentication against the Kubernetes API in PEM format. |  

### Bearer token authentication

This authentication method is primarily used with [service accounts](https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/).

| Name | Type | Description |
|------|------|-------------|
| `bearerTokenFile` | `string` | Points to the file that contains the bearer token for authenticating against the Kubernetes API. Set to `/var/run/secrets/kubernetes.io/serviceaccount` to use the service account when running ContainerSSH inside a Kubernetes cluster. |
| `bearerToken` | `string` | Directly contains the bearer token for authenticating against the Kubernetes API. |

## Pod configuration

The pod configuration contains the information which pod to run. The structure is very similar to the `Pod` object in Kubernetes, and we add a few extra options:

```yaml
kubernetes:
  pod:
    metadata:
      <metadata configuration here>
    spec:
      <pod spec here>
    <ContainerSSH-specific options here>
```

!!! note
    Do not include the `apiVersion`, `kind`, or `status` types from the Kubernetes structure.
    
!!! tip
    Did you know? You can get a full description of the Pod type by running `kubectl explain pod`, `kubectl explain pod.spec`, and `kubectl explain pod.metadata`.
    
### Basic pod configuration

ContainerSSH defaults to running pods in the `default` namespace with the `containerssh/containerssh-guest-image` container image. You can change these settings with the following options:

```yaml
kubernetes:
  pod:
    metadata:
      namespace: default
    spec:
      containers:
        - name: shell
          image: containerssh/containerssh-guest-image
          env:
           - name: VAR
             value: Hello world!
```

### Running multiple containers

When running multiple containers ContainerSSH defaults to attaching to the first container. You can change this behavior by specifying the `consoleContainerNumber` option. This number is 0-indexed.

```
kubernetes:
  pod:
    consoleContainerNumber: 1
    spec:
      containers:
        - name: container1
          image: ...
        - name: container2
          image: ...
```

### Mounting volumes

In Kubernetes volumes of various types can be mounted into pods. This is done as follows:

```yaml
kubernetes:
  pod:
    consoleContainerNumber: 1
    spec:
      volumes:
        - name: <volume name here>
          <mount type here>:
            <mount options here>
      containers:
        - name: shell
          image: <image name here>
          volumeMounts:
            - name: <volume name here>
              mountPath: <where to mount>
```

For example, mounting a path from the host machine can be done as follows:

```yaml
kubernetes:
  pod:
    consoleContainerNumber: 1
    spec:
      volumes:
        - name: home
          hostPath:
            path: /home/ubuntu
            type: Directory
      containers:
        - name: shell
          image: containerssh/containerssh-guest-image
          volumeMounts:
            - name: home
              mountPath: /home/ubuntu
```

!!! tip
    Use `kubectl explain pod.spec.volumes` for details on how to configure the volume driver for your storage.
    
### Forcing the pod to run on a specific node

In Kubernetes pod scheduling can be influenced either by [node affinity](https://kubernetes.io/docs/tasks/configure-pod-container/assign-pods-nodes-using-node-affinity/) or by [explicitly binding a pod to a node](https://kubernetes.io/docs/tasks/configure-pod-container/assign-pods-nodes/).

Node affinity lets you schedule pods based on various features of the node, e.g. the presence of a GPU, a disk type, etc. As the configuration can be quite complex we will not discuss it here, please [read the Kubernetes manual](https://kubernetes.io/docs/tasks/configure-pod-container/assign-pods-nodes-using-node-affinity/).

Binding a pod to a specific node on the other hand is rather simple:

```yaml
kubernetes:
  pod:
    spec:
      nodeName: <insert node name here>
```

### Other options

Apart from the `metadata` and `spec` options ContainerSSH has the following options on a Pod-level. These should not be changed unless required.

| Name | Type | Description |
|------|------|-------------|
| `consoleContainerNumber` | `uint` | Specifies the number of the container to attach to. Defaults to the first container. |
| `mode` | `string` | Specify `connection` to launch one pod per SSH connection or `session` to run one pod per SSH session (multiple pods per connection). In connection mode the container is started with the `idleCommand` as the first program and every session is launched similar to how `kubectl exec` runs programs. In session mode the command is launched directly. | 
| `idleCommand` | `[]string` | Specifies the command to run as the first process in the container in `connection` mode. Parameters must be provided as separate items in the array. Has no effect in `session` mode. |
| `shellCommand` | `[]string` | Specifies the command to run as a shell in `connection` mode. Parameters must be provided as separate items in the array. Has no effect in `session` mode. |
| `agentPath` | `string` | Contains the full path to the [ContainerSSH guest agent](https://github.com/containerssh/agent) inside the shell container. The agent must be installed in the guest image. |
| `disableAgent` | `bool` | Disable the ContainerSSH guest agent. This will disable several functions and is *not recommended*. |
| `subsystems` | `map[string]string` | Specifies a map of subsystem names to executables. It is recommended to set at least the `sftp` subsystem as many users will want to use it. |

### Configuration restrictions

- In `connection` mode the `idleCommand` and `shellCommand` options are required.
- In `session` mode the restart policy must be empty or `Never`.

## Configuring timeouts

The `timeouts` section has the following options. All options can use time units (e.g. `60s`) and default to nanoseconds without time units.

| Name | Description |
|------|-------------|
| `podStart` | The time to wait for the pod to start. |
| `podStop` | The time to wait for the pod to stop. |
| `commandStart` | The time to wait for the command to start in `connection` mode. |
| `signal` | The time to wait to deliver a signal to a process. |
| `window` | The time to wait to deliver a window size change. |
| `http` | The time to wait for the underlying HTTP calls to complete. |

## Securing Kubernetes

Securing the Kubernetes installation is beyond the scope of this document. We will describe how to deploy and configure ContainerSSH for security in a Kubernetes environment

### Creating a service account

When deploying ContainerSSH with a Kubernetes backend you should never an admin account for interacting with a Kubernetes cluster. ContainerSSH can run inside the same Kubernetes cluster or it can run as a standalone. When deploying inside the same Kubernetes cluster it is strongly recommended that ContainerSSH runs in a different namespace as the guest pods ContainerSSH launches.

The setup below assumes you are creating a service account in the `default` namespace and the ContainerSSH pods will run in the `containerssh-guests` namespace

First, we need to create the service account. The following fragment can be applied with `kubectl apply -f`:

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: containerssh
automountServiceAccountToken: false
```

Then we create the `role` and `rolebinding` resources in the `containerssh-guests` namespace to allow the service accounts to create pods:

```bash
kubectl create role containerssh \
  -n containerssh-guests \
  --verb=* \
  --resource=pods \
  --resource=pods/logs \
  --resource=pods/exec
kubectl create rolebinding containerssh \
  -n containerssh-guests \
  --serviceaccount=containerssh
```

#### Deploying inside of Kubernetes

When deploying ContainerSSH inside the same Kubernetes cluster you can simply use the service account when making your deployment:

```
kubernetes:
  connection:
    host: ...
    cacertFile: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
    bearerTokenFile: /var/run/secrets/kubernetes.io/serviceaccount/token
```

#### Deploying outside of Kubernetes

Now, if you are running ContainerSSH outside of the Kubernetes cluster you can fetch the secret belonging to the service account by first looking at the service account itself:

```
kubectl describe serviceaccount containerssh
```

This command will output the name of the secret for this service account, which can then be extracted:

```
kubectl get secret containerssh-token-2jrnc -o yaml
```

The output will look as follows:

```yaml
apiVersion: v1
data:
  ca.crt: <base64-encoded CA certificate here>
  namespace: ZGVmYXVsdA==
  token: <base64-encoded bearer token here>
kind: Secret
```

Base64-decode both the `ca.crt` and the `token` fields and insert them into your ContainerSSH config as follows:

```yaml
kubernetes:
  connection:
    bearerToken: <insert token here>
    cacert: |
      <insert ca.crt here>
```

### Preventing root escalation

Under normal circumstances a user running as root inside a container cannot access resources outside the container. However, in the event of a container escape vulnerability in Kubernetes it is prudent not to run container workloads as root. You can prevent forcibly prevent any container from running as root by configuring the following setting:

```yaml
kubernetes:
  pod:
    spec:
      securityContext:
        runAsNonRoot: true
```

However, this will fail starting any container image that wants to run as root. In addition to the option above, you can also force the container to a specific UID:

```yaml
kubernetes:
  pod:
    spec:
      securityContext:
        runAsUser: 1000
```

### Preventing storage exhaustion

A malicious user could cause the Kubernetes host to run out of disk space with a simple attack:

```bash
cat /dev/zero > ~/zerofill
```

There are two cases here:

If **the directory** the user can write to **is mounted using a volume** the attacker can fill up the storage that is mounted. You can pass per-user mounts from the [configuration server](configserver.md) that mount volumes that are unique to the connecting user. This way the user can only fill up their own disk. The specific implementation depends on your volume driver.

If **the directory** the user can write to **is not mounted** the user can fill up the container image. This is a much more subtle way of filling up the disk. Current Kubernetes does not support preventing this kind of attack, so it is recommended to only allow users to write to paths mounted as volumes. The  [`readOnlyRootFilesystem` PodSecurityPolicy](https://kubernetes.io/docs/concepts/policy/pod-security-policy/#volumes-and-file-systems) can be applied to the namespace or the whole cluster preventing writes to the container root filesystem filling up the disk.

### Preventing memory exhaustion

Users can also try to exhaust the available memory to potentially crash the server. This can be prevented using the following configuration:

```yaml
kubernetes:
  pod:
    spec:
      resources:
        limits:
          memory: "128Mi"
```

You can read more about memory requests and limits in the [Kubernetes documentation](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/).

### Preventing CPU exhaustion

A malicious user can also exhaust the CPU by running CPU-heavy workloads. This can be prevented by setting the following options:

```yaml
kubernetes:
  pod:
    spec:
      resources:
        limits:
          cpu: "500m"
```

In this setting `1000m` corresponds to a full core or vCPU of the host. You can read more about memory requests and limits in the [Kubernetes documentation](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/).

### Limiting network access

Depending on which Container Network Interface is installed on the Kubernetes cluster you may have access to [Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/). These work very similar to how traditional Linux firewalling works. The following network policy disables all network access within a namespace:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: containerssh-guest-policy
  namespace: containerssh-guests
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
  ingress: []
  egress: []
```

