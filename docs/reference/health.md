<h1>Health check endpoint</h1>

The health check endpoint is an HTTP server that returns `ok` and a 200 status code only if all ContainerSSH services are running. This can be used to integrate ContainerSSH with a load balancer.

The health check endpoint has the following options:

```yaml
health:
  enable: true
  listen: 0.0.0.0:7000
```

By default, the health check endpoint is disabled. The default listen port is 7000. Further configuration options can be found on the [HTTP and TLS page](http.md#http-server-configuration).