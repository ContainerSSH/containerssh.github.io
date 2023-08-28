# Supported SSH features

This table contains the list of currently supported SSH features in ContainerSSH.

| Feature | Support | RFC |
|---------|---------|-------------|
| Shell execution | :material-check-bold: | [RFC 4254 section 6.5](https://tools.ietf.org/html/rfc4254#section-6.5) |
| Command execution | :material-check-bold: | [RFC 4254 section 6.5](https://tools.ietf.org/html/rfc4254#section-6.5) |
| Subsystem execution | :material-check-bold: | [RFC 4254 section 6.5](https://tools.ietf.org/html/rfc4254#section-6.5) |
| Requesting a Pseudo-Terminal | :material-check-bold: | [RFC 4254 section 6.2](https://tools.ietf.org/html/rfc4254#section-6.2) |
| Setting environment variables | :material-check-bold: | [RFC 4254 section 6.4](https://tools.ietf.org/html/rfc4254#section-6.4) |
| Forwarding signals | :material-check-bold: |  [RFC 4254 section 6.9](https://tools.ietf.org/html/rfc4254#section-6.9) |
| Window dimension change | :material-check-bold: | [RFC 4254 section 6.7](https://tools.ietf.org/html/rfc4254#section-6.7) |
| Return exit statuses | :material-check-bold: | [RFC 4254 section 6.10](https://tools.ietf.org/html/rfc4254#section-6.10) | 
| Return exit signals | :material-check-bold: | [RFC 4254 section 6.10](https://tools.ietf.org/html/rfc4254#section-6.10) | 
| TCP/IP port forwarding | :material-check-bold: | [RFC 4254 section 7](https://tools.ietf.org/html/rfc4254#page-16) |
| X11 forwarding | :material-check-bold: | [RFC 4254 section 6.2](https://tools.ietf.org/html/rfc4254#page-11) |
| SSH agent forwarding (OpenSSH extension: `auth-agent-req@openssh.com`) | :material-close: | [draft-ietf-secsh-agent-02](https://tools.ietf.org/html/draft-ietf-secsh-agent-02) |
| Keepalive (OpenSSH extension: `keepalive@openssh.com`) | :material-check-bold: | |
| No more sessions (OpenSSH extension: `no-more-sessions@openssh.com`) | :material-close: | |