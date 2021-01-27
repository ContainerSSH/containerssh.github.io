---
title: The DockerRun backend
---

{{ outdated() }}

<h1>The DockerRun backend</h1>

The `dockerrun` backend launches a container using the Docker API. The default configuration connects the Docker socket on its default path.

## Changing the container image

The container image depends on the backend you are using. For `dockerrun` you can change the image in the config file:

```yaml
dockerrun:
  config:
    container:
      image: your/image
``` 

You can read more in the [reference manual](../../reference/docker.md)