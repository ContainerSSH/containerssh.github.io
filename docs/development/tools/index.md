# External tools we use

This guide runs you through the external tools we use and how we use them. This will give you a better idea on how ContainerSSH is managed.

<div class="grid">
<div class="grid__box">
<h2>GitHub</h2>
<p>GitHub provides a large chunk of our infrastructure, ranging from Git hosting, CI system to hosting this very website.</p>
<p><a href="/development/tools/github/" class="md-button">Read more »</a></p>
</div>
<div class="grid__box">
<h2>Terraform</h2>
<p>Since we have a <a href="https://github.com/containerssh">large number of repositories</a> we use the <a href="https://terraform.io">Terraform Cloud</a> to create and configure most of the settings in our GitHub organization. This also enables non-privileged users to request new repositories or changes to existing ones.</p>
<p><a href="/development/tools/terraform/" class="md-button">Read more »</a></p>
</div>
<div class="grid__box">
<h2>Snyk</h2>
<p>Snyk is our tool of choice to keep an eye on security updates we need to apply to Go dependencies, as well as container images.</p>
<p><a href="/development/tools/snyk/" class="md-button">Read more »</a></p>
</div>
<div class="grid__box">
<h2>Docker Hub</h2>
<p>Docker Hub is the primary source for our container images. Docker has graciously weaved rate limits for our organization.</p>
<p><a href="/development/tools/docker/" class="md-button">Read more »</a></p>
</div>
</div>