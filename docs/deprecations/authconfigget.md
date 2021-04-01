title: Moving from GET to POST in webhooks

# Moving from GET to POST in webhooks

In ContainerSSH version 0.3.1 and before the authentication and configuration webhooks used the `GET` HTTP method for sending webhooks due to a mistake. This has been changed to a `POST` request in ContainerSSH 0.4. If your authentication or configuration server only supports `GET` please add support for the `POST` method.
