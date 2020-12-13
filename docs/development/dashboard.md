---
title: Development Dashboard
---

<h1>Development Dashboard</h1>

=== "Roadmap"
    {% for milestone in get_milestones() %}
    ## [{{ milestone.title }}](https://github.com/ContainerSSH/ContainerSSH/milestones/{{ milestone.number }})
    
    {{ milestone.description}}
    
    | Title | Created |
    | ----- | ------- |{% for issue in get_milestone_issues(milestone) %}
    | [{{issue.title}}](https://github.com/containerssh/{{issue.repository.name}}/issues/{{ issue.number }}) | {{ days_ago(issue.created_at) }} |{% endfor %}
    {% endfor %}

=== "Repositories"
    | Repository | Description | Version |
    | ---------- | ----------- | ------- |{% for repo in github_repos() %}
    | [{{ repo.name }}](https://github.com/containerssh/{{ repo.name }}) | {{ repo.description }} | {{ get_version(repo) }} |{% endfor %}

=== "Issues"
    | Repository | Title | Milestone | Created |
    | ---------- | ----- | --------- | ------- |{% for issue in github_issues() %}
    | [{{issue.repository.name}}](https://github.com/containerssh/{{issue.repository.name}}/issues) | [{{issue.title}}](https://github.com/containerssh/{{issue.repository.name}}/issues/{{ issue.number }}) | [{{ issue.milestone.title }}](https://github.com/ContainerSSH/{{ issue.repository.name }}/milestone/{{ issue.milestone.number }}) | {{ days_ago(issue.created_at) }} |{% endfor %}
    
=== "Pull Requests"
    | Repository | Title | Milestone | Created | Can be merged |
    | ---------- | ----- | --------- | ------- | ------------- |{% for issue in github_prs() %}
    | [{{issue.repository.name}}](https://github.com/containerssh/{{issue.repository.name}}/pulls) | [{{issue.title}}](https://github.com/containerssh/{{issue.repository.name}}/pull/{{ issue.number }}) | [{{ issue.milestone.title }}](https://github.com/ContainerSSH/{{ issue.repository.name }}/milestone/{{ issue.milestone.number }}) | {{ days_ago(issue.created_at) }} | {% if issue.as_pull_request().mergeable_state == "clean" %}✅{% else %}❌{% endif %} |{% endfor %}
