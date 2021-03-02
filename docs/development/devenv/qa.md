---
title: Installing the QA tools
---

<h1>Installing the QA tools</h1>

## Installing golangci-lint

We are using [golangci-lint](https://golangci-lint.run/) as a way to lint the code for problematic practices. We use golangci-li using the following command line:

```
golangci-lint run -E asciicheck -E bodyclose -E dupl -E errorlint -E exportloopref -E funlen
```

Please follow the instructions below:

=== "Linux / WSL"

    1. Go to the [GitHub releases of golangci-lint](https://github.com/golangci/golangci-lint/releases) and download the latest Linux `.tar.gz`.
    2. Extract the file to a directory in your path (e.g. `~/bin/go`).
    3. Add executable rights to the file (e.g. `chmod +x ~/bin/go/golangci-lint`).

=== "Windows"
    
    1. Go to the [GitHub releases of golangci-lint](https://github.com/golangci/golangci-lint/releases) and download the latest Windows ZIP.
    2. Extract the `golangci-lint.exe` to your `%USERPROFILE%/go/bin` directory. 

=== "Brew (MacOS)"
    ```
    brew install golangci-lint
    ```

=== "MacPorts (MacOS)"
    ```
    sudo port install golangci-lint
    ```

=== "Manual (All platforms)"
    
    1. Go to the [GitHub releases of golangci-lint](https://github.com/golangci/golangci-lint/releases) and download the latest archive for your platform.
    2. Extract the `golangci-lint` to the `go/bin` directory in your home directory.
