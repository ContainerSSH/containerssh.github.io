---
title: Development Dashboard
---

<h1>Development Dashboard</h1>

=== "Roadmap"
    {% for milestone in get_milestones() %}
    ## [{{ milestone.title }}]({{ milestone.url }})
    
    {{ milestone.description}}
    
    {% for issue in milestone.issues %}- [{% if not issue.open %}X{% else %} {% endif %}] [{{issue.title}}]({{ issue.url }})
    {% endfor %}{% endfor %}

=== "Repositories"
    | Repository | Description | Version |
    | ---------- | ----------- | ------- |{% for repo in github_repos() %}
    | [{{ repo.name }}]({{ repo.url }}) | {{ repo.description }} | {{ get_version(repo) }} |{% endfor %}

=== "Issues"
    | Repository | Title | Milestone | Created |
    | ---------- | ----- | --------- | ------- |{% for issue in github_issues() %}
    | [{{issue.repo.name}}]({{ issue.repo.url }}/issues/) | [{{issue.title}}]({{ issue.url }}) | [{{ issue.milestone.title }}]({{ issue.milestone.url }}) | {{ days_ago(issue.created_at) }} |{% endfor %}
    
=== "Pull Requests"
    | Repository | Title | Created | Mergeable | Checks |
    | ---------- | ----- | ------- | ----------| ------ |{% for pr in github_prs() if pr.author != "dependabot" %}
    | [{{pr.repo.name}}]({{ pr.repo.url }}/pulls/) | [{{pr.title}}]({{ pr.url }}) | {{ days_ago(pr.created_at) }} | {% if pr.can_merge %}✅{% else %}❌{% endif %} | {% if pr.checks_status == "SUCCESS" %}✅{% else %}❌{% endif %} |{% else %}
    | *No pull requests open.* |{% endfor %}
    
=== "Dependency updates"
    | Repository | Title | Created | Mergeable | Checks |
    | ---------- | ----- | ------- | ----------| ------ |{% for pr in github_prs() if pr.author == "dependabot" %}
    | [{{pr.repo.name}}]({{ pr.repo.url }}/pulls/) | [{{pr.title}}]({{ pr.url }}) | {{ days_ago(pr.created_at) }} | {% if pr.can_merge %}✅{% else %}❌{% endif %} | {% if pr.checks_status == "SUCCESS" %}✅{% else %}❌{% endif %} |{% else %}
    | *No dependency updates open.* |{% endfor %}
