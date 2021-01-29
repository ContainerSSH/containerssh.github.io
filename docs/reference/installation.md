<h1>Installation</h1>

=== "Standalone"

    ContainerSSH can be deployed outside of a container. On our [releases page](https://github.com/ContainerSSH/ContainerSSH/releases) we provide binaries for Linux, Windows, and MacOS. We also provide DEB, RPM and APK (Alpine Linux) packages.
    
    Before running ContainerSSH you will need to create a `config.yaml` file that tells ContainerSSH where to find the SSH host key and the [authentication server](auth.md). The minimum configuration file looks like this:
    
    ```yaml
    ssh:
      hostkeys:
        - /path/to/your/host.key
    auth:
      url: http://your-auth-server/
    ```
    
    !!! tip
        You can generate a new host key using `openssl genrsa`
        
    !!! tip
        Details about the authentication server are described in the [Authentication section](auth.md).

    ContainerSSH can then be started by running `./containerssh --config /path/to/your/config.yaml`

=== "Docker"

    When deploying in Docker you must first prepare a configuration file that tells ContainerSSH where to find the SSH host key and the [authentication server](auth.md). The minimum configuration file looks like this:
    
    ```yaml
    ssh:
      hostkeys:
        - /var/run/secrets/host.key
    auth:
      url: http://your-auth-server/
    ```
    
    !!! tip
        You can generate a new host key using `openssl genrsa`

    !!! tip
        Details about the authentication server are described in the [Authentication section](auth.md).

    You can then run ContainerSSH with the following command line:
    
    ```bash
    docker run -d \
      -v /srv/containerssh/config.yaml:/etc/containerssh/config.yaml \
      -v /srv/containerssh/host.key:/var/run/secrets/host.key \
      -p 2222:2222 \
      containerssh/containerssh:0.4.0
    ```

=== "Kubernetes"

    When running ContainerSSH inside a Kubernetes cluster you must furst create a `Secret` that contains the host key.
    
    ```bash
    openssl genrsa | kubectl create secret generic containerssh-hostkey --from-file=host.key=/dev/stdin
    ```
        
    Next, you can create a ConfigMap to hold the ContainerSSH configuration:
    
    ```bash
    ( cat << EOF 
    ssh:
      hostkeys:
        - /etc/containerssh/host.key
    auth:
      url: http://your-auth-server/
    EOF
    ) | kubectl create configmap containerssh-config --from-file=config.yaml=/dev/stdin
    ```
    
    !!! tip
        Details about the authentication server are described in the [Authentication section](auth.md).
    
    Then you can create a deployment to run ContainerSSH:
    
    ```bash
    ( cat << EOF 
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: containerssh
      labels:
        app: containerssh
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
          containers:
          - name: containerssh
            image: containerssh/containerssh:0.4.0-PR3
            ports:
            - containerPort: 2222
            volumeMounts:
            - name: hostkey
              mountPath: /etc/containerssh/host.key
              subPath: host.key
              readOnly: true
            - name: config
              mountPath: /etc/containerssh/config.yaml
              subPath: config.yaml
              readOnly: true
          volumes:
          - name: hostkey
            secret:
              secretName: containerssh-hostkey
          - name: config
            configMap:
              name: containerssh-config
    EOF
    ) | kubectl apply -f -
    ```
    
    Finally, you can create a service to expose the SSH port. You can customize this to create a loadbalancer or nodeport to make SSH publicly available. See `kubectl expose --help` for details.  
    
    ```bash
    kubectl expose deployment containerssh \
        --port=2222 --target-port=2222 \
        --name=containerssh
    ```

    !!! warning "Note"
        This still does not configure ContainerSSH to use Kubernetes as a container backend. This is described in detail in the [Kubernetes backend section](kubernetes.md).