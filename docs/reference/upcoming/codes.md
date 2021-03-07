# Message codes

This page contains all message codes logged by ContainerSSH. Some of these are errors, while others only give you status information. Many of these messages are only logged when the [log level is set to `debug`](logging.md).

## Core

## SSH server

## Authentication module

| Code | Decription |
|------|------------|
| `AUTH` | ContainerSSH is trying to contact the authentication backend. |
| `AUTH_BACKEND_ERROR` | The ContainerSSH authentication server responded with a non-200 status code. ContainerSSH will retry the authentication for a few times before giving up. This is most likely a bug in your authentication server, please check your logs. |
| `AUTH_FAILED` | The user has provided invalid credentials and the authentication is rejected. |
| `AUTH_SUCCESSFUL` | The user has provided the correct credentials and the authentication is accepted. |
| `AUTH_INVALID_STATUS` | This message indicates that the authentication server returned an invalid HTTP status code. |

## Configuration module

## Metrics module

## Audit log module

## Backend module

## Security module

## Docker backend

| Code | Explanation |
|------|-------------|
| `DOCKER_AGENT_READ_FAILED` | The ContainerSSH Docker module failed to read from the ContainerSSH agent. This is most likely because the ContainerSSH guest agent is not present in the guest image, but agent support is enabled. |
| `DOCKER_CLOSE_OUTPUT_FAILED` | The ContainerSSH Docker module attempted to close the output (stdout and stderr) for writing but failed to do so. |
| `DOCKER_CLOSE_INPUT_FAILED` | The ContainerSSH Docker module attempted to close the input (stdin) for reading but failed to do so. |
| `DOCKER_CONFIG_ERROR` | The ContainerSSH Docker module detected a configuration error. Please check your configuration. |
| `DOCKER_CONTAINER_ATTACH` | The ContainerSSH Docker module is attaching to a container in session mode. |
| `DOCKER_CONTAINER_ATTACH_FAILED` | The ContainerSSH Docker module has failed to attach to a container in session mode. |
| `DOCKER_CONTAINER_CREATE` | ContainerSSH is creating a container. |
| `DOCKER_CONTAINER_CREATE_FAILED` | ContainerSSH failed to create a container. This may be a temporary and retried or a permanent error message. Check the log message for details. |
| `DOCKER_CONTAINER_START` | ContainerSSH is starting the previously-created container. |
| `DOCKER_CONTAINER_START_FAILED` | Starting the container failed. This message can either be temporary and retried or permanent. Check the log message for details. |
| `DOCKER_CONTAINER_STOP` | ContainerSSH is stopping the container. |
| `DOCKER_CONTAINER_STOP_FAILED` | ContainerSSH failed to stop the container. This message can be either temporary and retried or permanent. Check the log message for details. |
| `DOCKER_CONTAINER_REMOVE` | The ContainerSSH Docker module os removing the container. |
| `DOCKER_CONTAINER_REMOVE_FAILED` | The ContainerSSH Docker module could not remove the container. This message may be temporary and retried or permanent. Check the log message for details. |
| `DOCKER_CONTAINER_REMOVE_SUCCESSFUL` | The ContainerSSH Docker module has successfully removed the container. |
| `DOCKER_CONTAINER_SIGNAL` | The ContainerSSH Docker module is sending a signal to the container. |
| `DOCKER_CONTAINER_SIGNAL_FAILED` | The ContainerSSH Docker module has failed to send a signal to the container. |
| `DOCKER_CONTAINER_SHUTTING_DOWN` | The ContainerSSH Docker module is shutting down a container. |
| `DOCKER_EXEC` | The ContainerSSH Docker module is creating an execution. This may be in connection mode, or it may be the module internally using the exec mechanism to deliver a payload into the container. |
| `DOCKER_EXEC_ATTACH` | The ContainerSSH Docker module is attaching to the previously-created execution. |
| `DOCKER_EXEC_ATTACH_FAILED` | The ContainerSSH Docker module could not attach to the previously-created execution. |
| `DOCKER_EXEC_CREATE` | The ContainerSSH Docker module is creating an execution. |
| `DOCKER_EXEC_CREATE_FAILED` | The ContainerSSH Docker module has failed to create an execution. This can be temporary and retried or permanent. See the error message for details. |
| `DOCKER_EXEC_PID_READ_FAILED` | The ContainerSSH Docker module has failed to read the process ID from the ContainerSSH guest agent. This is most likely because the guest image does not contain the guest agent, but guest agent support has been enabled. |
| `DOCKER_EXEC_RESIZE` | The ContainerSSH Docker module is resizing the console. |
| `DOCKER_EXEC_RESIZE_FAILED` | The ContainerSSH Docker module failed to resize the console. |
| `DOCKER_EXEC_SIGNAL` | The ContainerSSH Docker module is delivering a signal in connection mode. |
| `DOCKER_EXEC_SIGNAL_FAILED` | The ContainerSSH Docker module failed to deliver a signal. |
| `DOCKER_EXEC_SIGNAL_FAILED_NO_AGENT` | The ContainerSSH Docker module failed to deliver a signal because guest agent support is disabled. |
| `DOCKER_EXEC_SIGNAL_SUCCESSFUL` | The ContainerSSH Docker module successfully delivered the requested signal. |
| `DOCKER_EXIT_CODE` | The ContainerSSH Docker module is fetching the exit code from the program. |
| `DOCKER_EXIT_CODE_CONTAINER_RESTARTING` | The ContainerSSH Docker module could not fetch the exit code from the program because the container is restarting. This is typically a misconfiguration as ContainerSSH containers should not automatically restart. |
| `DOCKER_EXIT_CODE_FAILED` | The ContainerSSH Docker module has failed to fetch the exit code of the program. |
| `DOCKER_EXIT_CODE_NEGATIVE` | The ContainerSSH Docker module has received a negative exit code from Docker. This should never happen and is most likely a bug. |
| `DOCKER_EXIT_CODE_STILL_RUNNING` | The ContainerSSH Docker module could not fetch the program exit code because the program is still running. This error may be temporary and retried or permanent. |
| `DOCKER_GUEST_AGENT_DISABLED` | This message indicates that the [ContainerSSH Guest Agent](https://github.com/containerssh/agent) has been disabled, which is strongly discouraged. ContainerSSH requires the guest agent to be installed in the container image to facilitate all SSH features. Disabling the guest agent will result in breaking the expectations a user has towards an SSH server. We provide the ability to disable guest agent support only for cases where the guest agent binary cannot be installed in the image at all. |
| `DOCKER_IMAGE_LISTING` | The ContainerSSH Docker module is listing the locally present container images to determine if the specified container image needs to be pulled. |
| `DOCKER_IMAGE_LISTING_FAILED` | The ContainerSSH Docker module failed to list the images present in the local Docker daemon. This is used to determine if the image needs to be pulled. This can be because the Docker daemon is not reachable, the certificate is invalid, or there is something else interfering with listing the images. |
| `DOCKER_IMAGE_PULL` | The ContainerSSH Docker module is pulling the container image. |
| `DOCKER_IMAGE_PULL_FAILED` | ContainerSSH failed to pull the specified container image. This can be because of connection issues to the Docker daemon, or because the Docker daemon itself can't pull the image. If you don't intend to have the image pulled you should set the `ImagePullPolicy` to `Never`. See the [Docker documentation](https://containerssh.io/reference/upcoming/docker) for details. |
| `DOCKER_IMAGE_PULL_NEEDED_CHECKING` | The ContainerSSH Docker module is checking if an image pull is needed. |
| `DOCKER_PROGRAM_ALREADY_RUNNING` | The ContainerSSH Docker module can't execute the request because the program is already running. This is a client error. |
| `DOCKER_SIGNAL_FAILED_NO_PID` | The ContainerSSH Docker module can't deliver a signal because no PID has been recorded. This is most likely because guest agent support is disabled. |
| `DOCKER_STREAM_INPUT_FAILED` | The ContainerSSH Docker module failed to stream stdin to the Docker engine. |
| `DOCKER_STREAM_OUTPUT_FAILED` | The ContainerSSH Docker module failed to stream stdout and stderr from the Docker engine. |
| `DOCKER_SUBSYSTEM_NOT_SUPPORTED` | The ContainerSSH Docker module is not configured to run the requested subsystem. |

## Kubernetes backend

# Error/message codes

| Code | Explanation |
|------|-------------|
| `KUBERNETES_AGENT_READ_FAILED` | The ContainerSSH Kubernetes module failed to read from the ContainerSSH agent. This is most likely because the ContainerSSH guest agent is not present in the guest image, but agent support is enabled. |
| `KUBERNETES_CLOSE_OUTPUT_FAILED` | The ContainerSSH Kubernetes module attempted to close the output (stdout and stderr) for writing but failed to do so. |
| `KUBERNETES_CLOSE_INPUT_FAILED` | The ContainerSSH Kubernetes module attempted to close the input (stdin) for reading but failed to do so. |
| `KUBERNETES_CONFIG_ERROR` | The ContainerSSH Kubernetes module detected a configuration error. Please check your configuration. |
| `KUBERNETES_POD_ATTACH` | The ContainerSSH Kubernetes module is attaching to a pod in session mode. |
| `KUBERNETES_POD_ATTACH_FAILED` | The ContainerSSH Kubernetes module has failed to attach to a pod in session mode. |
| `KUBERNETES_POD_CREATE` | ContainerSSH is creating a pod. |
| `KUBERNETES_POD_CREATE_FAILED` | ContainerSSH failed to create a pod. This may be a temporary and retried or a permanent error message. Check the log message for details. |
| `KUBERNETES_POD_REMOVE` | The ContainerSSH Kubernetes module os removing the pod. |
| `KUBERNETES_POD_REMOVE_FAILED` | The ContainerSSH Kubernetes module could not remove the pod. This message may be temporary and retried or permanent. Check the log message for details. |
| `KUBERNETES_POD_REMOVE_SUCCESSFUL` | The ContainerSSH Kubernetes module has successfully removed the pod. |
| `KUBERNETES_POD_SIGNAL` | The ContainerSSH Kubernetes module is sending a signal to the pod. |
| `KUBERNETES_POD_SIGNAL_FAILED` | The ContainerSSH Kubernetes module has failed to send a signal to the pod. |
| `KUBERNETES_POD_SHUTTING_DOWN` | The ContainerSSH Kubernetes module is shutting down a pod. |
| `KUBERNETES_EXEC` | The ContainerSSH Kubernetes module is creating an execution. This may be in connection mode, or it may be the module internally using the exec mechanism to deliver a payload into the pod. |
| `KUBERNETES_EXEC_ATTACH` | The ContainerSSH Kubernetes module is attaching to the previously-created execution. |
| `KUBERNETES_EXEC_ATTACH_FAILED` | The ContainerSSH Kubernetes module could not attach to the previously-created execution. |
| `KUBERNETES_EXEC_CREATE` | The ContainerSSH Kubernetes module is creating an execution. |
| `KUBERNETES_EXEC_CREATE_FAILED` | The ContainerSSH Kubernetes module has failed to create an execution. This can be temporary and retried or permanent. See the error message for details. |
| `KUBERNETES_EXEC_PID_READ_FAILED` | The ContainerSSH Kubernetes module has failed to read the process ID from the ContainerSSH guest agent. This is most likely because the guest image does not contain the guest agent, but guest agent support has been enabled. |
| `KUBERNETES_EXEC_RESIZE` | The ContainerSSH Kubernetes module is resizing the console. |
| `KUBERNETES_EXEC_RESIZE_FAILED` | The ContainerSSH Kubernetes module failed to resize the console. |
| `KUBERNETES_EXEC_SIGNAL` | The ContainerSSH Kubernetes module is delivering a signal in connection mode. |
| `KUBERNETES_EXEC_SIGNAL_FAILED` | The ContainerSSH Kubernetes module failed to deliver a signal. |
| `KUBERNETES_EXEC_SIGNAL_FAILED_NO_AGENT` | The ContainerSSH Kubernetes module failed to deliver a signal because guest agent support is disabled. |
| `KUBERNETES_EXEC_SIGNAL_SUCCESSFUL` | The ContainerSSH Kubernetes module successfully delivered the requested signal. |
| `KUBERNETES_EXIT_CODE` | The ContainerSSH Kubernetes module is fetching the exit code from the program. |
| `KUBERNETES_EXIT_CODE_POD_RESTARTING` | The ContainerSSH Kubernetes module could not fetch the exit code from the program because the pod is restarting. This is typically a misconfiguration as ContainerSSH pods should not automatically restart. |
| `KUBERNETES_EXIT_CODE_FAILED` | The ContainerSSH Kubernetes module has failed to fetch the exit code of the program. |
| `KUBERNETES_EXIT_CODE_NEGATIVE` | The ContainerSSH Kubernetes module has received a negative exit code from Kubernetes. This should never happen and is most likely a bug. |
| `KUBERNETES_EXIT_CODE_STILL_RUNNING` | The ContainerSSH Kubernetes module could not fetch the program exit code because the program is still running. This error may be temporary and retried or permanent. |
| `KUBERNETES_GUEST_AGENT_DISABLED` | This message indicates that the [ContainerSSH Guest Agent](https://github.com/podssh/agent) has been disabled, which is strongly discouraged. ContainerSSH requires the guest agent to be installed in the pod image to facilitate all SSH features. Disabling the guest agent will result in breaking the expectations a user has towards an SSH server. We provide the ability to disable guest agent support only for cases where the guest agent binary cannot be installed in the image at all. |
| `KUBERNETES_PROGRAM_ALREADY_RUNNING` | The ContainerSSH Kubernetes module can't execute the request because the program is already running. This is a client error. |
| `KUBERNETES_SIGNAL_FAILED_NO_PID` | The ContainerSSH Kubernetes module can't deliver a signal because no PID has been recorded. This is most likely because guest agent support is disabled. |
| `KUBERNETES_STREAM_INPUT_FAILED` | The ContainerSSH Kubernetes module failed to stream stdin to the Kubernetes engine. |
| `KUBERNETES_STREAM_OUTPUT_FAILED` | The ContainerSSH Kubernetes module failed to stream stdout and stderr from the Kubernetes engine. |
| `KUBERNETES_SUBSYSTEM_NOT_SUPPORTED` | The ContainerSSH Kubernetes module is not configured to run the requested subsystem. |