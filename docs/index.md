---
template: overrides/home.html
title: "ContainerSSH: Launch containers on demand"
hide:
  - navigation
  - toc
---

<div class="grid grid--4">
<div class="grid__box">
<h2>Offering web hosting?</h2>
<p>ContainerSSH lets you offer <strong>full SSH access</strong> to your users. Clients are dropped in containers where they can only access their own environment. Authenticate against your existing user database and mount directories based on your existing permission matrix.</p>
<p><a href="usecases/webhosting/" class="md-button">Read more »</a></p>
</div>
<div class="grid__box">
<h2>Teaching the cloud?</h2>
<p>With ContainerSSH students can connect to an <strong>on-demand environment</strong> that you can customize with your own tools and credentials. On disconnect the environment is cleaned up. This is perfect for Linux or cloud learning environments.</p>
<p><a href="usecases/learning/" class="md-button">Read more »</a></p>
</div>
<div class="grid__box">
<h2>Building a honeypot?</h2>
<p>If you want to understand what attackers do once they breach SSH you can use ContainerSSH to drop them into an <strong>isolated environment</strong>. You can store their entire audit trail on an S3-compatible storage for later analysis. This includes SFTP file uploads!</p>
<p><a href="usecases/honeypots/" class="md-button">Read more »</a></p>
</div>
<div class="grid__box">
<h2>Building a jump host?</h2>
<p>ContainerSSH is being used to provide dynamic console access to an environment with <strong>sensitive credentials</strong>. Webhooks let you dynamically provision credentials in conjunction with secret management systems such as Hashicorp Vault.</p>
<p><a href="usecases/security/" class="md-button">Read more »</a></p>
</div>
</div>

---

## How does it work?

<div class="grid">
<div class="grid__box">
<ol>
<li>The user opens an <strong>SSH connection</strong> to ContainerSSH.</li>
<li>ContainerSSH calls the <strong>authentication server</strong> with the user's username and password/pubkey to check if it is valid.</li>
<li>ContainerSSH calls the <strong>config server</strong> to obtain backend location and configuration (if configured).</li>
<li>ContainerSSH calls the <strong>container backend</strong> to launch the container with the specified configuration. All input from the user is sent directly to the backend, output from the container is sent to the user.</li>
</ol>   
<p><a href="https://youtu.be/Cs9OrnPi2IM" class="md-button">▶️ Watch as Video</a> <a href="/getting-started/" class="md-button">🚀 Get started »</a></p>
</div>
<div class="grid__box">
<p><img src="/images/architecture.svg" alt="" /></p>
</div>
</div>

---

## Demo

![](/images/ssh-in-action.gif)
