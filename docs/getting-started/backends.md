title: Backend selection

<h1>Backend selection</h1>

ContainerSSH is built to support multiple backends. The backend can be changed in the configuration file:

```yaml
# change to `kubernetes` to talk to Kubernetes
backend: docker
```

ContainerSSH currently supports the following backends:

| Backend | Description |
|---------|-------------|
| [`docker`](docker.md) | Runs Docker containers. |
| [`kubernetes`](kubernetes.md) | Runs Kubernetes containers. |
| [`sshproxy`](sshproxy.md) | Forwards SSH connections to a backend server. |

Read more in the [SSH proxy reference manual &raquo;](../reference/backends.md)