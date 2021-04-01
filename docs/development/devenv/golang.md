title: Installing Golang

<h1>Installing Golang</h1>

While there is an [official doc on installing Golang](https://golang.org/doc/install) it is less than helpful for Linux users. We are attempting to collect the best practices in installing Golang for beginners here.

!!! tip
    If you are using [Goland as an IDE](https://www.jetbrains.com/go/) you can skip this step. Goland downloads the Go compiler for you.

=== "Linux / WSL"

    **Ubuntu 20.04**
    
    On Ubuntu 20.04 you can install Go directly from the package manager:
    ```
    apt update
    apt install golang-1.14
    ```
    
    **RHEL/CentOS**
    ```
    yum install golang-bin
    ```
    
    **Fedora**
    ```
    dnf install golang-bin
    ```
    
    **Gentoo Linux**
    
    ```
    emerge --ask dev-lang/go
    ```
    
    **Other / non-administrator**
    
    1. Download [the Linux .tar.gz](https://golang.org/dl/).
    2. Extract the archive into a directory.
    3. Add the following section to your `~/.profile`, `~/.zshrc`, `~/.bashrc`, or `~/.bash_profile`, depending on your shell, then restart your terminal:
    
    ```bash
    export PATH=$PATH:/usr/local/bin/go
    ```
    
    We also recommend adding `~/go/bin` directory to your `PATH`.

=== "Windows"

    ** Install as administrator **

    Golang offers an [MSI-based installer](https://golang.org/dl/) for Windows that makes it easy to install Golang on your Windows machine. Follow the installation wizzard and the `go` command should start working in the terminal.
    
    We also recommend adding `%USERPROFILE%\go\bin` to your `PATH` environment variable to enable running tools from your home directory.
    
    ** Install as user **
    
    1. Download the `ZIP` archive from the [archive page](https://golang.org/dl/)
    2. Extract the ZIP file to a folder you have access to.
    3. Go to *Control Panel* &rarr; *System and Security* &rarr; *System* &rarr; *Advanced system settings*.
    4. Click on *Environment variables...*
    5. Change the `PATH` environment variable to point to the `bin` directory inside your Goland directory.
    
    We also recommend adding `%USERPROFILE%\go\bin` to your `PATH` environment variable to enable running tools from your home directory.
   
=== "MacOS"

    Golang offers a [PKG installer for MacOS](https://golang.org/dl/). The `go` command will be located in `/usr/local/go/bin`. If the `go` command doesn't work try restarting the terminal.
    
    If it still doesn't work try running the `/usr/local/go/bin/go` command. If that command works edit the `~/.profile`, `~/.zshrc`, or `~/.bash_profile` files and add the following lines then restart your terminal:
    
    ```bash
    export PATH=$PATH:/usr/local/bin/go
    ```
    
    We also recommend adding `~/go/bin` directory to your `PATH`.

