---
template: overrides/home.html
title: "ContainerSSH: Launch containers on demand"
hide:
  - navigation
  - toc
---

{{ grid_start(size="3") }}
{{ grid_item_start() }}
<h2>Build a lab</h2>
<p>Building a lab environment can be time-consuming. ContainerSSH solves this by providing dynamic SSH access with APIs, automatic cleanup on logout using ephemeral containers, and persistent volumes for storing data. <strong>Perfect for vendor and student labs.</strong></p>
<p><a href="usecases/lab/" class="md-button">Read more »</a></p>
{{ grid_item_end() }}
{{ grid_item_start() }}
<h2>Debug a production system</h2>
<p>Provide <strong>production access to your developers</strong>, give them their usual tools while logging all changes. Authorize their access and create short-lived credentials for the database using simple webhooks. Clean up the environment on disconnect.</p>
<p><a href="usecases/debugging/" class="md-button">Read more »</a></p>
{{ grid_item_end() }}
{{ grid_item_start() }}
<h2>Run a honeypot</h2>
<p>Study SSH attack patterns up close. Drop attackers safely into network-isolated containers or even virtual machines, and <strong>capture their every move</strong> using the audit logging ContainerSSH provides. The built-in S3 upload ensures you don't lose your data.</p>
<p><a href="usecases/honeypots/" class="md-button">Read more »</a></p>
{{ grid_item_end() }}
{{ grid_end() }}

