---
title: The Kubernetes backend
---

{{ outdated() }}

<h1>The KubeRun backend</h1>

The Kubernetes backend runs a pod in a Kubernetes cluster and attaches to a container there.

## Running outside of Kubernetes

If you are running ContainerSSH outside of Kubernetes you will need the following configuration:

```yaml
kubernetes:
  connection:
    host: your-kubernetes-api-server:6443
    cert: |
      -----BEGIN CERTIFICATE-----
      ...
      -----END CERTIFICATE-----
    key: |
      -----BEGIN RSA PRIVATE KEY-----
      ...
      -----END RSA PRIVATE KEY-----
    cacert: |
      -----BEGIN CERTIFICATE-----
      ...
      -----END CERTIFICATE-----
```

Alternatively you can use `cacertFile`, `keyFile` and `certFile` to point to files on the filesystem.

## Running inside a Kubernetes cluster

When you run inside of a Kubernetes cluster you can use the service account token:

```yaml
kubernetes:
  connection:
    certFile: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
    bearerTokenFile: /var/run/secrets/kubernetes.io/serviceaccount/token
```

## Changing the container image

For the `kuberun` backend the container image can be changed by modifying the pod spec:

```yaml
kubernetes:
  pod:
    consoleContainerNumber: 0
    metadata:
      namespace: default
    spec:
      containers:
        - name: shell
          image: containerssh/containerssh-guest-image
```

Note: if you are running multiple containers you should specify the `consoleContainerNumber` parameter to indicate which container you wish to attach to when an SSH session is opened.

You can read more in the [reference manual](../../reference/kubernetes.md)
