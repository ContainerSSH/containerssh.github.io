<h1>Setting up your development environment</h1>

Welcome! This guide will help you set up your development environment for writing ContainerSSH code. We recommend to following this guide step by step, even when you have already set up some of them yourself.

## Step 1: Create a GitHub account

ContainerSSH development is exclusively handled on GitHub. In order to send code or website contributions you will need to [create a GitHub account](https://github.com/join). Once you have an account we also recommend [setting up two-factor authentication](https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/about-two-factor-authentication).

## Step 2: Installing Git

Unless you plan to develop exclusively on the GitHub web interface you will also need to install Git on your computer. We support development on Windows, Linux, and MacOS, feel free to use any of those operating systems. Please follow [the GitHub guide to install Git](https://github.com/git-guides/install-git) on your operating system.

## Step 3: Creating a GPG key

Git is a distributed versioning system and you can make commits in the name of others. In order to verify committer identity (for both security and licencing purposes) we require all commits to be signed using GPG.

Please follow our [GPG for Git guide](gpg.md) to enable code signing on your machine..

## Step 4: Installing Golang

To compile the code you will need Golang. We have a [guide to install Golang](golang.md) on various platforms.

## Step 5: Installing the QA tools

To make sure there are no latent errors are creeping in we are using some [QA tools you will need](qa.md).

## Step 6: Installing Docker

The `dockerrun` backend requires Docker to be installed. [Please install Docker](docker.md) to develop against.

## Step 7: Installing Kubernetes

The `kuberun` backend requires Kubernetes to be installed. [Please install a lightweight Kubernetes](kubernetes.md) to develop against.

## Step 8: Setting up your IDE

We have a [guide to set up VSCode and Goland](ide.md) as your IDE.

## Step 9: Website

This website requires a [Python to run locally](website.md). [This guide](website.md) explains the details of setting it up.