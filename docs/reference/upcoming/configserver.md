title: Configuration server

<h1>Configuration Server</h1>

{{ reference_upcoming() }}

ContainerSSH has the ability to configure the backend, and the launched container dynamically based on the username and/or IP address. To do this ContainerSSH calls out to a configuration server if configured.

## Configuration

The configserver webhook can be configured in the main configuration using the following structure:

```yaml
configuration:
  <options>
```

The options here are described on the [HTTP and TLS](http.md#http-client-configuration) page. If no `url` is provided the configuration webhook is disabled.

## The configuration webhook

The configuration webhook is a simple JSON `POST` request to which the server must respond with a JSON response.

!!! note
    We have an [OpenAPI document](../api/authconfig) available for the authentication and configuration server. You can check the exact values available there, or use the OpenAPI document to generate parts of your server code.

!!! tip
    We provide a [Go library](https://github.com/ContainerSSH/configuration) to create a configuration server.
    
The config server will receive a request in following format:

```json
{
  "username":"ssh username",
  "connectionId": "ssh session ID"
}
```

The configuration server will have to respond with the following response accompanied with the content type of `application/json`. 

```json
{
  "config": {
    // Provide a partial configuration here 
  }
}
```

The configuration JSON structure is identical to the YAML described in this reference manual and the full configuration can be dumped by running `./containerssh --dump-config`. The server is free to return only partial options that it wants to set. Any options that are sent overwrite the ones from the configuration file.

Currently only the following options can be set from the configuration server:

- [Backend](backends.md)
- [Docker](docker.md)
- [Kubernetes](kubernetes.md)
- [Security](security.md)

!!! tip
    We provide a [Go library to implement a config server](https://github.com/containerssh/configuration).
