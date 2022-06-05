title: About ContainerSSH

<h1>About ContainerSSH</h1>

ContainerSSH is a *fully open source community-driven project*. It is made with ❤️ by the following group of volunteers.

## Core maintainers

<span class="contributors">{% for contributor in contributors() -%}{%- if contributor.core %}
<span class="contributor">
    <span class="contributor__image"><img src="{{contributor.avatar_url}}" alt="" /></span>
    <span class="contributor__name">{{contributor.name}}</span>
    <span class="contributor__social_wrapper">
        <a class="contributor__social contributor__social--github" target="_blank" href="https://github.com/{{contributor.github}}" title="GitHub">:fontawesome-brands-github:</a>
        {%- if contributor.twitter %}<a class="contributor__social contributor__social--twitter" target="_blank" href="https://twitter.com/{{contributor.twitter}}" title="Twitter">:fontawesome-brands-twitter:</a>{% endif -%}
        {%- if contributor.website %}<a class="contributor__social contributor__social--website" target="_blank" href="{{contributor.website}}" title="Website">:fontawesome-solid-globe:</a>{% endif -%}
        {%- if contributor.linkedin %}<a class="contributor__social contributor__social--linkedin" target="_blank" href="https://linkedin.com/in/{{contributor.linkedin}}" title="LinkedIn">:fontawesome-brands-linkedin:</a>{% endif -%}
    </span>
</span>{% endif %}{% endfor %}</span>

## Contributors

<span class="contributors">{% for contributor in contributors() -%}{%- if not contributor.core %}
<span class="contributor">
    <span class="contributor__image"><img src="{{contributor.avatar_url}}" alt="" /></span>
    <span class="contributor__name">{{contributor.name}}</span>
    <span class="contributor__social_wrapper">
        <a class="contributor__social contributor__social--github" target="_blank" href="https://github.com/{{contributor.github}}" title="GitHub">:fontawesome-brands-github:</a>
        {%- if contributor.twitter %}<a class="contributor__social contributor__social--twitter" target="_blank" href="https://twitter.com/{{contributor.twitter}}" title="Twitter">:fontawesome-brands-twitter:</a>{% endif -%}
        {%- if contributor.website %}<a class="contributor__social contributor__social--website" target="_blank" href="{{contributor.website}}" title="Website">:fontawesome-solid-globe:</a>{% endif -%}
        {%- if contributor.linkedin %}<a class="contributor__social contributor__social--linkedin" target="_blank" href="https://linkedin.com/in/{{contributor.linkedin}}" title="LinkedIn">:fontawesome-brands-linkedin:</a>{% endif -%}
    </span>
</span>{% endif %}{% endfor %}</span>


<small>Note: this list is opt-in for privacy reasons. If you wish to be listed on this page please <a href="https://github.com/ContainerSSH/containerssh.github.io/edit/main/contributors.yaml">add your name here</a>.</small>

## Companies

We use services and tools from the following companies for free:

<table class="companies">
<tr class="company">
<td class="logo"><a href="https://hub.docker.com/orgs/containerssh" target="_blank"><img src="/images/logos/docker.png" alt="Docker" /></a></td>
<td>
<h3><a href="https://hub.docker.com/orgs/containerssh" target="_blank">Docker</a></h3>
<p>Docker has accepted ContainerSSH into their <a href="https://www.docker.com/community/open-source/application" target="_blank">Docker Open Source Program</a>. The open source program exempts ContainerSSH from the <a href="https://www.docker.com/increase-rate-limits" target="_blank">Docker Hub rate limits</a>, which is important to us because we are using it to host the <a href="https://hub.docker.com/repository/docker/containerssh/containerssh-guest-image" target="_blank">default guest image</a>.</p>
</td>
</tr>
<tr class="company">
<td class="logo"><a href="https://github.com/ContainerSSH/" target="_blank"><img src="/images/logos/github.png" alt="GitHub" /></a></td>
<td>
<h3><a href="https://github.com/ContainerSSH/" target="_blank">GitHub</a></h3>
<p>GitHub provides the <a href="https://github.com/containerssh/" target="_blank">core development infrastructure for ContainerSSH</a>, as well as the continuous integration system and the hosting for this website.</p>
</td>
</tr>
<tr class="company">
<td class="logo"><a href="https://github.com/ContainerSSH/" target="_blank"><img src="/images/logos/snyk.png" alt="Snyk" /></a></td>
<td>
<h3><a href="https://app.snyk.io/org/containerssh/projects" target="_blank">Snyk</a></h3>
<p>Snyk monitors our Go dependencies and container root images for known security vulnerabilities and alerts us when we need to rebuild any of them.</p>
</td>
</tr>
<tr class="company">
<td class="logo"><a href="https://www.hashicorp.com/products/terraform" target="_blank"><img src="/images/logos/terraform.png" alt="HashiCorp Terraform" /></a></td>
<td>
<h3><a href="https://www.hashicorp.com/products/terraform" target="_blank">Terraform Cloud</a></h3>
<p>We use the <a href="https://www.hashicorp.com/products/terraform" target="_blank">Terraform Cloud</a> by <a href="https://www.hashicorp.com/">HashiCorp</a> to <a href="https://github.com/containerssh/github-terraform">automate the configuration</a> of our GitHub organization.</p>
</td>
</tr>
</table>
