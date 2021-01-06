---
title: ContainerSSH packages
---

ContainerSSH maintains a package repository at `packages.containerssh.io`. This page describes how to add the repository to your operating system.

=== "Debian/Ubuntu"

    First, you need to add the tools needed for adding a custom repository:
    
    ```bash
    sudo apt-get update
    sudo apt-get install \
        apt-transport-https \
        ca-certificates \
        curl \
        gnupg-agent \
        software-properties-common
    ```
    
    Next, you should add our GnuPG key as a trusted key for packages:
    
    ```bash
    curl -fsSL https://packages.containerssh.io/debian/gpg | sudo apt-key add -
    ```
    
    Verify that you now have the correct fingerprint:
    
    ```bash
    sudo apt-key fingerprint F358FABA
    ```
    
    Add our repository:
    
    ```bash
    sudo add-apt-repository \
       "deb [arch=amd64] https://packages.containerssh.io/debian main stable"
    ```
    
    Finally, refresh the package list:
    
    ```bash
    sudo apt-get update
    ```
    
    Now you can install the ContainerSSH packages.