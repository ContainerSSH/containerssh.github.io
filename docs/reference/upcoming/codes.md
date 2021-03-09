# Message codes

This page contains all message codes logged by ContainerSSH. Some of these are errors, while others only give you status information. Many of these messages are only logged when the [log level is set to `debug`](logging.md).

## Core

| Code | Explanation |
|------|-------------|
| `CORE_CONFIG_CANNOT_WRITE_FILE` | ContainerSSH cannot update the configuration file with the new host keys and will only use the host key for the current run. |
| `CORE_CONFIG_ERROR` | ContainerSSH encountered an error in the configuration. |
| `CORE_CONFIG_FILE` | ContainerSSH is reading the configuration file |
| `CORE_HOST_KEY_GENERATION_FAILED` | ContainerSSH could not generate host keys and is aborting the run. |
| `CORE_NO_HOST_KEYS` | The configuration does not contain host keys. ContainerSSH will attempt to generate host keys and update the configuration file. |

## Auditlog

| Code | Explanation |
|------|-------------|
| `AUDIT_S3_CANNOT_CLOSE_METADATA_FILE_HANDLE` | ContainerSSH could not close the metadata file in the local folder. This typically happens when the local folder is on an NFS share. (This is NOT supported.) |
| `AUDIT_S3_CLOSE_FAILED` | ContainerSSH failed to close an audit log file in the local directory. This usually happens when the local directory is on an NFS share. (This is NOT supported.) |
| `AUDIT_S3_FAILED_CREATING_METADATA_FILE` | ContainerSSH failed to create the metadata file for the S3 upload in the local temporary directory. Check if the local directory specified is writable and has enough disk space. |
| `AUDIT_S3_FAILED_METADATA_JSON_ENCODING` | ContainerSSH failed to encode the metadata file. This is a bug, please report it. |
| `AUDIT_S3_FAILED_READING_METADATA_FILE` | ContainerSSH failed to read the metadata file for the S3 upload in the local temporary directory. Check if the local directory specified is readable and the files have not been corrupted. |
| `AUDIT_S3_FAILED_STAT_QUEUE_ENTRY` | ContainerSSH failed to stat the queue file. This usually happens when the local directory is being manually manipulated. |
| `AUDIT_S3_FAILED_WRITING_METADATA_FILE` | ContainerSSH failed to write the local metadata file. Please check if your disk has enough disk space. |
| `AUDIT_S3_MULTIPART_ABORTING` | ContainerSSH is aborting a multipart upload. Check the log message for details. |
| `AUDIT_S3_MULTIPART_FAILED_ABORT` | ContainerSSH failed aborting a multipart upload from a previously crashed ContainerSSH run. |
| `AUDIT_S3_MULTIPART_FAILED_LIST` | ContainerSSH failed to list multipart uploads on the object storage bucket. This is needed to abort uploads from a previously crashed ContainerSSH run. |
| `AUDIT_S3_MULTIPART_PART_UPLOADING` | ContainerSSH is uploading a part of an audit log to the S3-compatible object storage. |
| `AUDIT_S3_MULTIPART_PART_UPLOAD_COMPLETE` | ContainerSSH completed the upload of an audit log part to the S3-compatible object storage. |
| `AUDIT_S3_MULTIPART_PART_UPLOAD_FAILED` | ContainerSSH failed to upload a part to the S3-compatible object storage. Check the message for details. |
| `AUDIT_S3_MULTIPART_UPLOAD` | ContainerSSH is starting a new S3 multipart upload. |
| `AUDIT_S3_MULTIPART_UPLOAD_FINALIZATION_FAILED` | ContainerSSH has uploaded all audit log parts, but could not finalize the multipart upload. |
| `AUDIT_S3_MULTIPART_UPLOAD_FINALIZED` | ContainerSSH has uploaded all audit log parts and has successfully finalized the upload. |
| `AUDIT_S3_MULTIPART_UPLOAD_FINALIZING` | ContainerSSH has uploaded all audit log parts and is now finalizing the multipart upload. |
| `AUDIT_S3_MULTIPART_UPLOAD_INITIALIZATION_FAILED` | ContainerSSH failed to initialize a new multipart upload to the S3-compatible object storage. Check if the S3 configuration is correct and the provided S3 access key and secrets have permissions to start a multipart upload. |
| `AUDIT_S3_NO_SUCH_QUEUE_ENTRY` | ContainerSSH was trying to upload an audit log from the metadata file, but the audit log does not exist. |
| `AUDIT_S3_RECOVERING` | ContainerSSH found a previously aborted multipart upload locally and is now attempting to recover the upload. |
| `AUDIT_S3_REMOVE_FAILED` | ContainerSSH failed to remove an uploaded audit log from the local directory. This usually happens on Windows when a different process has the audit log open. (This is not a supported setup.) |
| `AUDIT_S3_SINGLE_UPLOAD` | ContainerSSH is uploading the full audit log in a single upload to the S3-compatible object storage. This happens when the audit log size is below the minimum size for a multi-part upload. |
| `AUDIT_S3_SINGLE_UPLOAD_COMPLETE` | ContainerSSH successfully uploaded the audit log as a single upload. |
| `AUDIT_S3_SINGLE_UPLOAD_FAILED` | ContainerSSH failed to upload the audit log as a single upload. |

## Authentication

| Code | Explanation |
|------|-------------|
| `AUTH` | ContainerSSH is trying to contact the authentication backend to verify the user credentials. |
| `AUTH_BACKEND_ERROR` | The ContainerSSH authentication server responded with a non-200 status code. ContainerSSH will retry the authentication for a few times before giving up. This is most likely a bug in your authentication server, please check your logs. |
| `AUTH_FAILED` | The user has provided invalid credentials and the authentication is rejected. |
| `AUTH_INVALID_STATUS` | This message indicates that the authentication server returned an invalid HTTP status code. |
| `AUTH_NOT_SUPPORTED` | The authentication method the client requested is not supported by ContainerSSH. |
| `AUTH_SUCCESSFUL` | The user has provided the correct credentials and the authentication is accepted. |

## Backend

| Code | Explanation |
|------|-------------|
| `BACKEND_CONFIG_ERROR` | The backend retreived from the configuration server is invalid. See the error message for details. |

## Configuration

| Code | Explanation |
|------|-------------|
| `CONFIG_BACKEND_ERROR` | ContainerSSH has received an invalid response from the configuration server or the network connection broke. ContainerSSH will retry fetching the user-specific configuration until the timeout. If this error persists check the connectivity to the configuration server, or the logs of the configuration server itself to find out of there may be a specific error. |
| `CONFIG_INVALID_STATUS_CODE` | ContainerSSH has received a non-200 response code when calling a per-user backend configuration from the configuration server. |
| `CONFIG_REQUEST` | ContainerSSH is sending a quest to the configuration server to obtain a per-user backend configuration. |
| `CONFIG_RESPONSE` | ContainerSSH has received a per-user backend configuration from the configuration server. |
| `CONFIG_SERVER_AVAILABLE` | The ContainerSSH configuration server is now available at the specified address. |

## Docker

| Code | Explanation |
|------|-------------|
| `DOCKER_AGENT_READ_FAILED` | The ContainerSSH Docker module failed to read from the ContainerSSH agent. This is most likely because the ContainerSSH guest agent is not present in the guest image, but agent support is enabled. |
| `DOCKER_CLOSE_INPUT_FAILED` | The ContainerSSH Docker module attempted to close the input (stdin) for reading but failed to do so. |
| `DOCKER_CLOSE_OUTPUT_FAILED` | The ContainerSSH Docker module attempted to close the output (stdout and stderr) for writing but failed to do so. |
| `DOCKER_CONFIG_ERROR` | The ContainerSSH Docker module detected a configuration error. Please check your configuration. |
| `DOCKER_CONTAINER_ATTACH` | The ContainerSSH Docker module is attaching to a container in session mode. |
| `DOCKER_CONTAINER_ATTACH_FAILED` | The ContainerSSH Docker module has failed to attach to a container in session mode. |
| `DOCKER_CONTAINER_CREATE` | The ContainerSSH Docker module is creating a container. |
| `DOCKER_CONTAINER_CREATE_FAILED` | The ContainerSSH Docker module failed to create a container. This may be a temporary and retried or a permanent error message. Check the log message for details. |
| `DOCKER_CONTAINER_REMOVE` | The ContainerSSH Docker module os removing the container. |
| `DOCKER_CONTAINER_REMOVE_FAILED` | The ContainerSSH Docker module could not remove the container. This message may be temporary and retried or permanent. Check the log message for details. |
| `DOCKER_CONTAINER_REMOVE_SUCCESSFUL` | The ContainerSSH Docker module has successfully removed the container. |
| `DOCKER_CONTAINER_SHUTTING_DOWN` | The ContainerSSH Docker module is shutting down a container. |
| `DOCKER_CONTAINER_SIGNAL` | The ContainerSSH Docker module is sending a signal to the container. |
| `DOCKER_CONTAINER_SIGNAL_FAILED` | The ContainerSSH Docker module has failed to send a signal to the container. |
| `DOCKER_CONTAINER_START` | The ContainerSSH Docker module is starting the previously-created container. |
| `DOCKER_CONTAINER_START_FAILED` | The ContainerSSH docker module failed to start the container. This message can either be temporary and retried or permanent. Check the log message for details. |
| `DOCKER_CONTAINER_STOP` | The ContainerSSH Docker module is stopping the container. |
| `DOCKER_CONTAINER_STOP_FAILED` | The ContainerSSH Docker module failed to stop the container. This message can be either temporary and retried or permanent. Check the log message for details. |
| `DOCKER_EXEC` | The ContainerSSH Docker module is creating an execution. This may be in connection mode, or it may be the module internally using the exec mechanism to deliver a payload into the container. |
| `DOCKER_EXEC_ATTACH` | The ContainerSSH Docker module is attaching to the previously-created execution. |
| `DOCKER_EXEC_ATTACH_FAILED` | The ContainerSSH Docker module could not attach to the previously-created execution. |
| `DOCKER_EXEC_CREATE` | The ContainerSSH Docker module is creating an execution. |
| `DOCKER_EXEC_CREATE_FAILED` | The ContainerSSH Docker module has failed to create an execution. This can be temporary and retried or permanent. See the error message for details. |
| `DOCKER_EXEC_PID_READ_FAILED` | The ContainerSSH Docker module has failed to read the process ID from the [ContainerSSH Guest Agent](https://github.com/containerssh/agent). This is most likely because the guest image does not contain the guest agent, but guest agent support has been enabled. |
| `DOCKER_EXEC_RESIZE` | The ContainerSSH Docker module is resizing the console. |
| `DOCKER_EXEC_RESIZE_FAILED` | The ContainerSSH Docker module failed to resize the console. |
| `DOCKER_EXEC_SIGNAL` | The ContainerSSH Docker module is delivering a signal in container mode. |
| `DOCKER_EXEC_SIGNAL_FAILED` | The ContainerSSH Docker module failed to deliver a signal. |
| `DOCKER_EXEC_SIGNAL_FAILED_NO_AGENT` | The ContainerSSH Docker module failed to deliver a signal because [ContainerSSH Guest Agent](https://github.com/containerssh/agent) support is disabled. |
| `DOCKER_EXEC_SIGNAL_SUCCESSFUL` | The ContainerSSH Docker module successfully delivered the requested signal. |
| `DOCKER_EXIT_CODE` | The ContainerSSH Docker module is fetching the exit code from the program. |
| `DOCKER_EXIT_CODE_CONTAINER_RESTARTING` | The ContainerSSH Docker module could not fetch the exit code from the program because the container is restarting. This is typically a misconfiguration as ContainerSSH containers should not automatically restart. |
| `DOCKER_EXIT_CODE_FAILED` | The ContainerSSH Docker module has failed to fetch the exit code of the program. |
| `DOCKER_EXIT_CODE_NEGATIVE` | The ContainerSSH Docker module has received a negative exit code from Docker. This should never happen and is most likely a bug. |
| `DOCKER_EXIT_CODE_STILL_RUNNING` | The ContainerSSH Docker module could not fetch the program exit code because the program is still running. This error may be temporary and retried or permanent. |
| `DOCKER_GUEST_AGENT_DISABLED` | The [ContainerSSH Guest Agent](https://github.com/containerssh/agent) has been disabled, which is strongly discouraged. ContainerSSH requires the guest agent to be installed in the container image to facilitate all SSH features. Disabling the guest agent will result in breaking the expectations a user has towards an SSH server. We provide the ability to disable guest agent support only for cases where the guest agent binary cannot be installed in the image at all. |
| `DOCKER_IMAGE_LISTING` | The ContainerSSH Docker module is listing the locally present container images to determine if the specified container image needs to be pulled. |
| `DOCKER_IMAGE_LISTING_FAILED` | The ContainerSSH Docker module failed to list the images present in the local Docker daemon. This is used to determine if the image needs to be pulled. This can be because the Docker daemon is not reachable, the certificate is invalid, or there is something else interfering with listing the images. |
| `DOCKER_IMAGE_PULL` | The ContainerSSH Docker module is pulling the container image. |
| `DOCKER_IMAGE_PULL_FAILED` | The ContainerSSH Docker module failed to pull the specified container image. This can be because of connection issues to the Docker daemon, or because the Docker daemon itself can't pull the image. If you don't intend to have the image pulled you should set the `ImagePullPolicy` to `Never`. See the [Docker documentation](https://containerssh.io/reference/upcoming/docker) for details. |
| `DOCKER_IMAGE_PULL_NEEDED_CHECKING` | The ContainerSSH Docker module is checking if an image pull is needed. |
| `DOCKER_PROGRAM_ALREADY_RUNNING` | The ContainerSSH Docker module can't execute the request because the program is already running. This is a client error. |
| `DOCKER_SIGNAL_FAILED_NO_PID` | The ContainerSSH Docker module can't deliver a signal because no PID has been recorded. This is most likely because guest agent support is disabled. |
| `DOCKER_STREAM_INPUT_FAILED` | The ContainerSSH Docker module failed to stream stdin to the Docker engine. |
| `DOCKER_STREAM_OUTPUT_FAILED` | The ContainerSSH Docker module failed to stream stdout and stderr from the Docker engine. |
| `DOCKER_SUBSYSTEM_NOT_SUPPORTED` | The ContainerSSH Docker module is not configured to run the requested subsystem. |

## HTTP

| Code | Explanation |
|------|-------------|
| `HTTP_CLIENT_CONNECTION_FAILED` | This message indicates a connection failure on the network level. |
| `HTTP_CLIENT_DECODE_FAILED` | This message indicates that decoding the JSON response has failed. The status code is set for this code. |
| `HTTP_CLIENT_ENCODE_FAILED` | This message indicates that JSON encoding the request failed. This is usually a bug. |
| `HTTP_CLIENT_REDIRECT` | This message indicates that the server responded with a HTTP redirect. |
| `HTTP_CLIENT_REDIRECTS_DISABLED` | This message indicates that ContainerSSH is not following a HTTP redirect sent by the server. Use the allowRedirects option to allow following HTTP redirects. |
| `HTTP_CLIENT_REQUEST` | This message indicates that a HTTP request is being sent from ContainerSSH |
| `HTTP_CLIENT_RESPONSE` | This message indicates that ContainerSSH received a HTTP response from a server. |
| `HTTP_SERVER_ENCODE_FAILED` | The HTTP server failed to encode the response object. This is a bug, please report it. |
| `HTTP_SERVER_RESPONSE_WRITE_FAILED` | The HTTP server failed to write the response. |

## Kubernetes 

| Code | Explanation |
|------|-------------|
| `KUBERNETES_CLOSE_OUTPUT_FAILED` | The ContainerSSH Kubernetes module attempted to close the output (stdout and stderr) for writing but failed to do so. |
| `KUBERNETES_CONFIG_ERROR` | The ContainerSSH Kubernetes module detected a configuration error. Please check your configuration. |
| `KUBERNETES_EXEC` | The ContainerSSH Kubernetes module is creating an execution. This may be in connection mode, or it may be the module internally using the exec mechanism to deliver a payload into the pod. |
| `KUBERNETES_EXEC_RESIZE` | The ContainerSSH Kubernetes module is resizing the terminal window. |
| `KUBERNETES_EXEC_RESIZE_FAILED` | The ContainerSSH Kubernetes module failed to resize the console. |
| `KUBERNETES_EXEC_SIGNAL` | The ContainerSSH Kubernetes module is delivering a signal. |
| `KUBERNETES_EXEC_SIGNAL_FAILED` | The ContainerSSH Kubernetes module failed to deliver a signal. |
| `KUBERNETES_EXEC_SIGNAL_FAILED_NO_AGENT` | The ContainerSSH Kubernetes module failed to deliver a signal because guest agent support is disabled. |
| `KUBERNETES_EXEC_SIGNAL_SUCCESSFUL` | The ContainerSSH Kubernetes module successfully delivered the requested signal. |
| `KUBERNETES_EXIT_CODE_FAILED` | The ContainerSSH Kubernetes module has failed to fetch the exit code of the program. |
| `KUBERNETES_GUEST_AGENT_DISABLED` | The [ContainerSSH Guest Agent](https://github.com/podssh/agent) has been disabled, which is strongly discouraged. ContainerSSH requires the guest agent to be installed in the pod image to facilitate all SSH features. Disabling the guest agent will result in breaking the expectations a user has towards an SSH server. We provide the ability to disable guest agent support only for cases where the guest agent binary cannot be installed in the image at all. |
| `KUBERNETES_PID_RECEIVED` | The ContainerSSH Kubernetes module has received a PID from the Kubernetes guest agent. |
| `KUBERNETES_POD_ATTACH` | The ContainerSSH Kubernetes module is attaching to a pod in session mode. |
| `KUBERNETES_POD_CREATE` | The ContainerSSH Kubernetes module is creating a pod. |
| `KUBERNETES_POD_CREATE_FAILED` | The ContainerSSH Kubernetes module failed to create a pod. This may be a temporary and retried or a permanent error message. Check the log message for details. |
| `KUBERNETES_POD_REMOVE` | The ContainerSSH Kubernetes module is removing a pod. |
| `KUBERNETES_POD_REMOVE_FAILED` | The ContainerSSH Kubernetes module could not remove the pod. This message may be temporary and retried or permanent. Check the log message for details. |
| `KUBERNETES_POD_REMOVE_SUCCESSFUL` | The ContainerSSH Kubernetes module has successfully removed the pod. |
| `KUBERNETES_POD_SHUTTING_DOWN` | The ContainerSSH Kubernetes module is shutting down a pod. |
| `KUBERNETES_POD_WAIT` | The ContainerSSH Kubernetes module is waiting for the pod to come up. |
| `KUBERNETES_POD_WAIT_FAILED` | The ContainerSSH Kubernetes module failed to wait for the pod to come up. Check the error message for details. |
| `KUBERNETES_PROGRAM_ALREADY_RUNNING` | The ContainerSSH Kubernetes module can't execute the request because the program is already running. This is a client error. |
| `KUBERNETES_PROGRAM_NOT_RUNNING` | This message indicates that the user requested an action that can only be performed when a program is running, but there is currently no program running. |
| `KUBERNETES_SIGNAL_FAILED_EXITED` | The ContainerSSH Kubernetes module can't deliver a signal because the program already exited. |
| `KUBERNETES_SIGNAL_FAILED_NO_PID` | The ContainerSSH Kubernetes module can't deliver a signal because no PID has been recorded. This is most likely because guest agent support is disabled. |
| `KUBERNETES_SUBSYSTEM_NOT_SUPPORTED` | The ContainerSSH Kubernetes module is not configured to run the requested subsystem. |
| `KUBERUN_DEPRECATED` | This message indicates that you are still using the deprecated KubeRun backend. This backend doesn't support all safety and functionality improvements and will be removed in the future. Please read the [deprecation notice for a migration guide](https://containerssh.io/deprecations/kuberun) |
| `KUBERUN_EXEC_DISABLED` | This message indicates that the user tried to execute a program, but program execution is disabled in the legacy KubeRun configuration. |
| `KUBERUN_INSECURE` | This message indicates that you are using Kubernetes in the "insecure" mode where certificate verification is disabled. This is a major security flaw, has been deprecated and is removed in the new Kubernetes backend. Please change your configuration to properly validates the server certificates. |

## Log

| Code | Explanation |
|------|-------------|
| `LOG_FILE_OPEN_FAILED` | ContainerSSH failed to open the specified log file. |
| `LOG_ROTATE_FAILED` | ContainerSSH cannot rotate the logs as requested because of an underlying error. |
| `LOG_WRITE_FAILED` | ContainerSSH cannot write to the specified log file. This usually happens because the underlying filesystem is full or the log is located on a non-local storage (e.g. NFS), which is not supported. |
| `TEST` | This is message that should only be seen in unit and component tests, never in production. |
| `UNKNOWN_ERROR` | This is an untyped error. If you see this in a log that is a bug and should be reported. |

## Metrics

| Code | Explanation |
|------|-------------|
| `METRICS_AVAILABLE` | The metrics service is now online and ready for service. |

## Security

| Code | Explanation |
|------|-------------|
| `SECURITY_ENV_REJECTED` | ContainerSSH rejected setting the environment variable because it does not pass the security settings. |
| `SECURITY_EXEC_FAILED_SETENV` | Program execution failed in conjunction with the forceCommand option because ContainerSSH could not set the `SSH_ORIGINAL_COMMAND` environment variable on the backend. |
| `SECURITY_EXEC_FORCING_COMMAND` | ContainerSSH is replacing the command passed from the client (if any) to the specified command and is setting the `SSH_ORIGINAL_COMMAND` environment variable. |
| `SECURITY_EXEC_REJECTED` | A program execution request has been rejected because it doesn't conform to the security settings. |
| `SECURITY_SHELL_REJECTED` | ContainerSSH rejected launching a shell due to the security settings. |
| `SECURITY_SIGNAL_REJECTED` | ContainerSSH rejected delivering a signal because it does not pass the security settings. |
| `SECURITY_SUBSYSTEM_REJECTED` | ContainerSSH rejected the subsystem because it does pass the security settings. |
| `SECURITY_TTY_REJECTED` | ContainerSSH rejected the pseudoterminal request because of the security settings. |

## Service

| Code | Explanation |
|------|-------------|
| `SERVICE_CRASHED` | A ContainerSSH has stopped improperly. |
| `SERVICE_POOL_RUNNING` | All ContainerSSH services are now running. |
| `SERVICE_POOL_STARTING` | All ContainerSSH services are starting. |
| `SERVICE_POOL_STOPPED` | ContainerSSH has stopped all services. |
| `SERVICE_POOL_STOPPING` | ContainerSSH is stopping all services. |
| `SERVICE_RUNNING` | A ContainerSSH service is now running |
| `SERVICE_STARTING` | ContainerSSH is starting a component service |
| `SERVICE_STOPPED` | A ContainerSSH service has stopped. |
| `SERVICE_STOPPING` | A ContainerSSH service is now stopping. |

## SSH

| Code | Explanation |
|------|-------------|
| `SSH_ALREADY_RUNNING` | The SSH server is already running and has been started again. This is a bug, please report it. |
| `SSH_AUTH_FAILED` | The user has provided invalid credentials. |
| `SSH_AUTH_SUCCESSFUL` | The user has provided valid credentials and is now authenticated. |
| `SSH_AUTH_UNAVAILABLE` | The user has requested an authentication method that is currently unavailable. |
| `SSH_AVAILABLE` | The SSH service is now online and ready for service. |
| `SSH_BACKEND_REJECTED_HANDSHAKE` | The backend has rejected the connecting user after successful authentication. |
| `SSH_CHANNEL_REQUEST` | The user has send a new channel-specific request. |
| `SSH_CHANNEL_REQUEST_FAILED` | ContainerSSH couldn't fulfil the channel-specific request. |
| `SSH_CHANNEL_REQUEST_SUCCESSFUL` | ContainerSSH has successfully processed the channel-specific request. |
| `SSH_CONNECTED` | A user has connected over SSH. |
| `SSH_DECODE_FAILED` | ContainerSSH failed to decode something from the user. This is either a bug in ContainerSSH or in the connecting client. |
| `SSH_DISCONNECTED` | An SSH connection has been severed. |
| `SSH_EXIT` | ContainerSSH is sending the exit code of the program to the user. |
| `SSH_EXIT_CODE_FAILED` | ContainerSSH failed to obtain and send the exit code of the program to the user. |
| `SSH_EXIT_SIGNAL` | ContainerSSH is sending the exit signal from an abnormally exited program to the user. |
| `SSH_HANDSHAKE_FAILED` | The connecting party failed to establish a secure SSH connection. This is most likely due to invalid credentials or a backend error. |
| `SSH_HANDSHAKE_SUCCESSFUL` | The user has provided valid credentials and has now established an SSH connection. |
| `SSH_LISTEN_CLOSE_FAILED` | ContainerSSH failed to close the listen socket. |
| `SSH_NEW_CHANNEL` | A user has established a new SSH channel. (Not connection!) |
| `SSH_NEW_CHANNEL_REJECTED` | The user has requested a new channel to be opened, but was rejected. |
| `SSH_REPLY_SEND_FAILED` | ContainerSSH couldn't send the reply to a request to the user. This is usually the case if the user suddenly disconnects. |
| `SSH_START_FAILED` | ContainerSSH failed to start the SSH service. This is usually because of invalid configuration. |
| `SSH_UNSUPPORTED_CHANNEL_TYPE` | The user requested a channel type that ContainerSSH doesn't support (e.g. TCP/IP forwarding). |
| `SSH_UNSUPPORTED_GLOBAL_REQUEST` | The users client has send a global request ContainerSSH does not support. This is nothing to worry about. |
