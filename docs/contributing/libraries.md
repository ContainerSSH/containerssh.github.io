<h1>ContainerSSH libraries</h1>

ContainerSSH consists of several independent libraries. These libraries are developed, tested, and developed separately to ensure each component meets the quality requirements of a reusable library.

{{lib("auditlog", "Audit logger for SSH events recording in great detail.")}}
{{lib("auditlogintegration", "Overlay integrating the auditlog library with the sshserver library.")}}
{{lib("auth", "This library externalizes the authentication process to an external service. It contains both the client and the server components.")}}
{{lib("authintegration", "Integrate the auth library with the sshserver.")}}
{{lib("configuration", "Configuration structure, server, and client.")}}
{{lib("backend", "Backend selector library.")}}
{{lib("dockerrun", "Run SSH connections in Docker containers.")}}
{{lib("http", "Simplified HTTP server and client.")}}
{{lib("kuberun", "Run SSH connections in Kubernetes pods.")}}
{{lib("log", "Common multi-level logging interface.")}}
{{lib("logintegration", "Integrate logging into ContainerSSH.")}}
{{lib("metrics", "Metrics collection and exposure.")}}
{{lib("service", "Centralized library to run multiple services in the same daemon.")}}
{{lib("sshserver", "SSH server abstraction library.")}}
