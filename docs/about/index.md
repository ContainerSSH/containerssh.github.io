title: About ContainerSSH

<h1>About ContainerSSH</h1>

ContainerSSH is a *fully open source community-driven project*. If you would like to know more about our contribution and decision making process, check out the [ContainerSSH Working Group Charter](https://github.com/ContainerSSH/community/blob/main/CHARTER.md). This project is made with ❤️ by the following group of volunteers.

## Working Group

### Chairs

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

### Members

If you would like to join the WG, please check out the [charter](https://github.com/ContainerSSH/community/blob/main/CHARTER.md), [code of conduct](https://github.com/ContainerSSH/community/blob/main/CODE_OF_CONDUCT.md), and [contribution guide](https://github.com/ContainerSSH/community/blob/main/CONTRIBUTING.md).

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

<small>Note: The contributors list is opt-in for privacy reasons. If you wish to be listed on this page please <a href="https://github.com/ContainerSSH/containerssh.github.io/edit/main/contributors.yaml">add your name here</a>.</small>
