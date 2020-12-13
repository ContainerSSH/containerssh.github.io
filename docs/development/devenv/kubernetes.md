---
title: Installing Kubernetes
---

<h1>Installing Kubernetes</h1>

If you develop against the `kuberun` backend you will need a working Kubernetes.

=== "Windows / MacOS"

    **Docker Desktop** contains a working Kubernetes. **Please enable it** to have a working Kubernetes setup. You can test it by running:
    
    ```
    kubectl get nodes
    ```
    
=== "Windows / WSL"

    For WSL we recommend setting up **KinD (Kubernetes in Docker)**. Please read the [KinD guide](https://kind.sigs.k8s.io/docs/user/using-wsl2/) for getting it running.
    
    Please create a cluster with the oldest [officially supported Kubernetes](https://kubernetes.io/docs/setup/release/version-skew-policy/) to test against:
    
    ```
    kind create cluster --image=image-url-here
    ```
    
    You can obtain the image URL from the [KinD releases section](https://github.com/kubernetes-sigs/kind/releases).

=== "Linux"

    **We recommend using [KinD](https://kind.sigs.k8s.io/docs/user/quick-start/) (Kubernetes in Docker)** as a reliable way to get a Kubernetes cluster running.
    
    Please create a cluster with the oldest [officially supported Kubernetes](https://kubernetes.io/docs/setup/release/version-skew-policy/) to test against:
    
    ```
    kind create cluster --image=image-url-here
    ```
    
    You can obtain the image URL from the [KinD releases section](https://github.com/kubernetes-sigs/kind/releases).
    
    !!! tip
        Some Linux distributions may support tiny Kubernetes distributions like [k3s](https://k3s.io/) or [microk8s](https://microk8s.io/), but we have managed to get consistently good results only with KinD.
