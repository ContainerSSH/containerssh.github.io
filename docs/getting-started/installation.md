title: Installing ContainerSSH

<h1>Installing ContainerSSH</h1>

ContainerSSH is provided on the [Downloads page](../downloads/index.md). You can install it in a containerized environment or as a standalone software on Windows, Linux, and MacOS.

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
    
    You can then run ContainerSSH with the following command line:
    
    ```bash
    docker run -d \
      -v /srv/containerssh/config.yaml:/etc/containerssh/config.yaml \
      -v /srv/containerssh/host.key:/var/run/secrets/host.key \
      -p 2222:2222 \
      containerssh/containerssh:0.4
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
            image: containerssh/containerssh:0.4
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
