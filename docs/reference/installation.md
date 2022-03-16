
<h1>Installation</h1>

=== "Standalone"

    ContainerSSH can be deployed outside of a container. On our [downloads page](../downloads/index.md) we provide binaries for Linux, Windows, and MacOS. We also provide DEB and RPM packages.
    
    Before running ContainerSSH you will need to create a `config.yaml` file that tells ContainerSSH where to find the SSH host key and the [authentication server](authserver.md). The minimum configuration file looks like this:
    
    ```yaml
    ssh:
      hostkeys:
        - /path/to/your/host.key
    auth:
      url: http://your-auth-server/
    ```

    Please generate your host key by running `openssl genrsa > /path/to/your/host.key`.
    
    ContainerSSH can then be started by running `./containerssh --config /path/to/your/config.yaml`

=== "Docker"

    When deploying in Docker you must first prepare a configuration file that tells ContainerSSH where to find the SSH host key and the [authentication server](authserver.md). The minimum configuration file looks like this:
    
    ```yaml
    ssh:
      hostkeys:
        - /var/run/secrets/host.key
    auth:
      url: http://your-auth-server/
    ```
    
    Please generate your host key by running `openssl genrsa > /path/to/your/host.key`. You can then run ContainerSSH with the following command line:
    
    ```bash
    docker run -d \
      -v /srv/containerssh/config.yaml:/etc/containerssh/config.yaml \
      -v /srv/containerssh/host.key:/var/run/secrets/host.key \
      -p 2222:2222 \
      containerssh/containerssh:0.4
    ```

=== "Kubernetes"

    In this example we will deploy ContainerSSH into the `containerssh` namespace, and the pods for the connections in
    the `containerssh-guests` namespace. To do that we will first create the `containerssh` namespace:

    ```bash
    kubectl create ns containerssh
    ```
    
    We will then create a secret containing the host key:
    
    ```bash
    openssl genrsa | kubectl create secret generic -n  containerssh-hostkey --from-file=host.key=/dev/stdin
    ```

    Finally, we will deploy ContainerSSH. Please customize as needed, especially the ContainerSSH configuration.

    ```yaml
    # Create a namespace to put ContainerSSH guest pods in
    apiVersion: v1
    kind: Namespace
    metadata:
      name: containerssh-guests
    ---
    # Create a service account ContainerSSH can use
    apiVersion: v1
    kind: ServiceAccount
    automountServiceAccountToken: true
    metadata:
      name: containerssh
      namespace: containerssh
    ---
    # Create a role ContainerSSH can use
    apiVersion: rbac.authorization.k8s.io/v1
    kind: Role
    metadata:
      name: containerssh
      namespace: containerssh-guests
    rules:
    - apiGroups:
      - ""
      resources:
      - pods
      - pods/logs
      - pods/exec
      verbs:
      - '*'
    ---
    # Bind the role to the service account
    apiVersion: rbac.authorization.k8s.io/v1
    kind: RoleBinding
    metadata:
      name: containerssh
      namespace: containerssh-guests
    roleRef:
      apiGroup: rbac.authorization.k8s.io
      kind: Role
      name: containerssh
    subjects:
    - kind: ServiceAccount
      name: containerssh
      namespace: containerssh
    ---
    # Create a ContainerSSH config to use the service account in the pod itself.
    apiVersion: v1
    data:
      config.yaml: |
        ssh:
          hostkeys:
            - /etc/containerssh/host.key
        auth:
          url: http://authconfig:8080
        log:
          level: debug
        backend: kubernetes
        kubernetes:
          connection:
            host: kubernetes.default.svc
            cacertFile: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
            bearerTokenFile: /var/run/secrets/kubernetes.io/serviceaccount/token
          pod:
            metadata:
              namespace: containerssh
            spec:
              containers:
                - name: shell
                  image: containerssh/containerssh-guest-image
    kind: ConfigMap
    metadata:
      name: containerssh-config
      namespace: containerssh
    ---
    # Deploy ContainerSSH with the service account and configmap applied.
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      labels:
        app: containerssh
      name: containerssh
      namespace: containerssh
    spec:
      replicas: 1
      selector:
        matchLabels:
          app: containerssh
      template:
        metadata:
          labels:
            app: containerssh
        spec:
          automountServiceAccountToken: true
          securityContext:
            runAsNonRoot: true
            readOnlyRootFilesystem: true
          containers:
          - image: containerssh/containerssh:0.4.1
            imagePullPolicy: IfNotPresent
            name: containerssh
            ports:
            - containerPort: 2222
              protocol: TCP
            volumeMounts:
            - mountPath: /etc/containerssh/host.key
              name: hostkey
              readOnly: true
              subPath: host.key
            - mountPath: /etc/containerssh/config.yaml
              name: config
              readOnly: true
              subPath: config.yaml
          restartPolicy: Always
          serviceAccount: containerssh
          serviceAccountName: containerssh
          volumes:
          - name: hostkey
            secret:
              secretName: containerssh-hostkey
          - configMap:
              name: containerssh-config
            name: config
    ```

    Finally, you will want to expose the ContainerSSH service to the outside world. You can do this either with a NodePort or a Loadbalancer-type resource:

    ```yaml
    apiVersion: v1
    kind: Service
    metadata:
      labels:
        app: containerssh
      name: containerssh
      namespace: containerssh
    spec:
      ipFamilies:
      - IPv4
      - IPv6
      ipFamilyPolicy: PreferDualStack
      ports:
      - port: 2222
        protocol: TCP
        targetPort: 2222
      selector:
        app: containerssh
      type: NodePort
    ```

    !!! warning "Note"
        This still does not configure ContainerSSH to use Kubernetes as a container backend. This is described in detail in the [Kubernetes backend section](kubernetes.md).