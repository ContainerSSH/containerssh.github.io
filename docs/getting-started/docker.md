---
title: The Docker backend
---

<h1>The <code>Docker</code> backend</h1>

The `docker` backend launches a container using the Docker API. The default configuration connects the Docker socket on its default path.

## Changing the container image

The container image depends on the backend you are using. For `dockerrun` you can change the image in the config file:

```yaml
docker:
  execution:
    container:
      image: your/image
``` 

You can read more in the [reference manual](../reference/docker.md)