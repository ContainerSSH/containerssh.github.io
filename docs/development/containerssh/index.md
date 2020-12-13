---
title: Understanding ContainerSSH
---

<h1>Understanding ContainerSSH</h1>

ContainerSSH is an SSH server that talks to external APIs such as Docker or Kubernetes. This section will explain how ContainerSSH is built.

## Understanding SSH

We don't really think about SSH all that much. Open PuTTY, or your terminal, SSH into a server, and merrily type commands issued to a server running a distance away. *Except if you need to write an SSH server.* This section will discuss the concepts you need to work on ContainerSSH.

<p><a href="ssh/" class="md-button">Read more »</a></p>

## Your first SSH server

ContainerSSH may be complex, so let's start simple: let's implement a very simple SSH server in Go that talks to the Docker backend.

<p><a href="first-ssh-server/" class="md-button">Read more »</a></p>

## Internal Architecture

ContainerSSH is a project of several thousand lines of code so overview is critical. Our internal architecture document describes what the moving parts of ContainerSSH are.

<p><a href="internal-architecture/" class="md-button">Read more »</a></p>
