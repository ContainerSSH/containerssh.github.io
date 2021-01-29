---
title: The Kubernetes backend
---

{{ outdated() }}

<h1>The KubeRun backend</h1>

The KubeRun backend runs and is tested against all [currently actively maintained Kubernetes versions](https://kubernetes.io/docs/setup/release/version-skew-policy/). For ContainerSSH version 0.3 these are: 1.19, and 1.18.

## The base configuration structure

In order to use the Kubernetes backend you must specify the following configuration entries via the configuration file or the configuration server:

```yaml
backend: kuberun
kuberun:
  connection:
    <connection configuration here>
  pod:
    <pod configuration here>
``` 

## Configuring connection parameters

In order to use Kubernetes you must provide the credentials to authenticate with the Kubernetes cluster. There are several supported authentication methods:

- Username and password (HTTP basic auth).
- x509 client certificates.
- Bearer token.

These options should be specified like this:

```yaml
kuberun:
  connection:
    host: <...>
    <...>
```

### Base configuration

| Name | Type | Description |
|------|------|-------------|
| `host` | `string` | The hostname or ip + the port of the Kubernetes API server. Set this to `kubernetes.default.svc` to run inside a Kubernetes cluster, otherwise set it to the host name of your Kubernetes API. |
| `path` | `string` | This is the API path of the Kubernetes API. Defaults to `/api` and you will typically not need to change this. |
| `cacertFile` | `string` | Points to the file that contains the CA certificate in PEM format that signed the server certificate. |
| `cacert` | `string` | Directly contains the CA certificate in PEM format that signed the server certificate. |
| `serverName` | `string` | Sets the hostname of the server that should be sent to the Kuberentes API in the TLS SNI. This is useful when the Kubernetes API has a hostname that is not resolvable from the server ContainerSSH is running on. |
| `insecure` | `bool` | Disable certificate verification on the Kubernetes API. **This is a very bad idea** as anyone on the network will be able to intercept your credentials. |
| `qps` | float32` | Indicates a maximum queries per second from this client. |
| `burst` | `int` | Indicates the maximum burst for query throttling. |
| `timeout` | `string` | Timeout for pod operations in nanoseconds. Time units can be used. |

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

The pod configuration contains the information which pod to run.

```yaml
kuberun:
  pod:
    namespace: <namespace name>
    podSpec:
      <pod spec here>
    <ContainerSSH-specific options here>
```

!!! tip
    Did you know? You can get a full description of the Pod type by running `kubectl explain pod.spec`.
    
### Basic pod configuration

ContainerSSH defaults to running pods in the `default` namespace with the `containerssh/containerssh-guest-image` container image. You can change these settings with the following options:

```yaml
kuberun:
  pod:
    namespace: default
    podSpec:
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
kuberun:
  pod:
    namespace: default
    consoleContainerNumber: 1
    podSpec:
      containers:
        - name: container1
          image: ...
        - name: container2
          image: ...
```

### Mounting volumes

In Kubernetes volumes of various types can be mounted into pods. This is done as follows:

```yaml
kuberun:
  pod:
    consoleContainerNumber: 1
    podSpec:
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
kuberun:
  pod:
    consoleContainerNumber: 1
    podSpec:
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
kuberun:
  pod:
    podSpec:
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
| `enableAgent` | `bool` | Enable the ContainerSSH guest agent. This enables the ContainerSSH guest agent. |
| `subsystems` | `map[string]string` | Specifies a map of subsystem names to executables. It is recommended to set at least the `sftp` subsystem as many users will want to use it. |
| `disableCommand` | `bool` | Disable command execution. |