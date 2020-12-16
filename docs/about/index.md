---
title: Who makes ContainerSSH?
---

<h1>Who makes ContainerSSH? Why?</h1>

ContainerSSH is a *fully open source community-driven project*. It is made with ❤️ by the following group of volunteers.

<span class="contributors">{% for contributor in contributors() -%}
<span class="contributor">
    <span class="contributor__image"><img src="{{contributor.avatar_url}}" alt="" /></span>
    <span class="contributor__name">{{contributor.name}}</span>
    {%- if contributor.core_maintainer %}<span class="contributor__role">core maintainer</span>{%else%}<span class="contributor__role">&nbsp;</span>{% endif -%} 
    <span class="contributor__social_wrapper">
        <a class="contributor__social contributor__social--github" target="_blank" href="https://github.com/{{contributor.github}}" title="GitHub">:fontawesome-brands-github:</a>
        {%- if contributor.twitter %}<a class="contributor__social contributor__social--twitter" target="_blank" href="https://twitter.com/{{contributor.twitter}}" title="Twitter">:fontawesome-brands-twitter:</a>{% endif -%}
        {%- if contributor.website %}<a class="contributor__social contributor__social--website" target="_blank" href="{{contributor.website}}" title="Website">:fontawesome-solid-globe:</a>{% endif -%}
        {%- if contributor.linkedin %}<a class="contributor__social contributor__social--linkedin" target="_blank" href="https://linkedin.com/in/{{contributor.linkedin}}" title="LinkedIn">:fontawesome-brands-linkedin:</a>{% endif -%}
    </span>
</span>{% endfor %}</span>

<small>Note: appearance on this list is opt-in for privacy reasons. If you wish to be listed on this page please <a href="https://github.com/ContainerSSH/containerssh.github.io/edit/main/contributors.yaml">add your name here</a>.</small>