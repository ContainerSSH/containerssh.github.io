# How we use Snyk

[Snyk](https://snyk.io) is a wonderful service and program to monitor dependencies that have security issues. While not all dependencies are high profile enough to make this a replacement for vetting dependencies, it helps tremendously with keeping up with container image updates.

Snyk monitors both our container images on [Docker Hub](docker.md) as well as our Go dependencies from the `go.mod` files.

!!! tip
    The Go monitoring in Snyk is a bit finicky, so when a vulnerable library is discovered we add a `replace` section to the `go.mod` file as follows:
    
    ```
    // Fixes CVE-2020-9283
    replace (
        golang.org/x/crypto v0.0.0-20190308221718-c2843e01d9a2 => golang.org/x/crypto v0.0.0-20210220033148-5ea612d1eb83
        golang.org/x/crypto v0.0.0-20191011191535-87dc89f01550 => golang.org/x/crypto v0.0.0-20210220033148-5ea612d1eb83
        golang.org/x/crypto v0.0.0-20200220183623-bac4c82f6975 => golang.org/x/crypto v0.0.0-20210220033148-5ea612d1eb83
        golang.org/x/crypto v0.0.0-20200622213623-75b288015ac9 => golang.org/x/crypto v0.0.0-20210220033148-5ea612d1eb83
    )
    ```
    
    This is done even if the vulnerable library is not ultimately used. The reason for this is part added safety, and in other part to satisfy Snyk.

When vulnerable container images are discovered we update our appropriate repositories, while in case of Go library vulnerabilities we release a new version.