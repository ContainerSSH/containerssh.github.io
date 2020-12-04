from datetime import datetime
import os
import pprint
from github import Github
from github.Repository import Repository
from github.Issue import Issue
from github.Milestone import Milestone

token = os.getenv("GITHUB_TOKEN")
gh = Github(token)

org = gh.get_organization("containerssh")
repoPages = org.get_repos()

main_repo = org.get_repo("containerssh")

repoIndex = 0
repos = []
while True:
    repoList = repoPages.get_page(repoIndex)
    if len(repoList) == 0:
        break
    repos.extend(repoList)
    repoIndex = repoIndex + 1


def get_issues():
    issues = []
    for repo in repos:
        issue_pages = repo.get_issues()
        page = 0
        while True:
            issue_list = issue_pages.get_page(page)
            page = page + 1
            if len(issue_list) == 0:
                break
            issues.extend(issue_list)
    return issues


issues = get_issues()


def declare_variables(variables, macro):
    @macro
    def lib(lib, description):
        MD = """
## [%s](https://github.com/containerssh/%s)

%s [Read more »](https://github.com/containerssh/%s)

    go get -u github.com/containerssh/%s

[![GitHub release (latest SemVer including pre-releases)](https://img.shields.io/github/v/release/containerssh/%s?include_prereleases&style=for-the-badge)](https://github.com/ContainerSSH/%s/releases)
[![GitHub last commit](https://img.shields.io/github/last-commit/containerssh/%s?style=for-the-badge)](https://github.com/containerssh/%s)
[![GitHub issues](https://img.shields.io/github/issues/ContainerSSH/%s?style=for-the-badge)](https://github.com/ContainerSSH/%s/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/containerssh/%s?style=for-the-badge)](https://github.com/ContainerSSH/%s/pulls)
[![Lint](https://img.shields.io/github/workflow/status/containerssh/%s/Lint?style=for-the-badge&label=Lint)](https://github.com/ContainerSSH/%s/actions?query=workflow%%3ALint)
[![Tests](https://img.shields.io/github/workflow/status/containerssh/%s/Tests?style=for-the-badge&label=Tests)](https://github.com/ContainerSSH/%s/actions?query=workflow%%3ATests)
[![CodeQL](https://img.shields.io/github/workflow/status/containerssh/%s/CodeQL?style=for-the-badge&label=CodeQL)](https://github.com/ContainerSSH/%s/actions?query=workflow%%3ACodeQL)
[![Go Report Card](https://goreportcard.com/badge/github.com/containerssh/%s?style=for-the-badge)](https://goreportcard.com/report/github.com/containerssh/%s)
[![LGTM Alerts](https://img.shields.io/lgtm/alerts/github/ContainerSSH/%s?style=for-the-badge)](https://lgtm.com/projects/g/ContainerSSH/%s/)
"""
        return MD % (
            lib,
            lib,
            description,
            lib,
            lib,
            lib,
            lib,
            lib,
            lib,
            lib,
            lib,
            lib,
            lib,
            lib,
            lib,
            lib,
            lib,
            lib,
            lib,
            lib,
            lib,
            lib,
            lib,
        )

    @macro
    def since(version):
        "Add a button"
        HTML = """<a href="https://github.com/containerssh/containerssh/releases" target="_blank"><span class="since"><span class="since__hide">(</span><span class="since__text">since</span> <span class="since__value">%s</span><span class="since__hide">)</span></span></a>"""
        return HTML % (version)

    @macro
    def upcoming(version):
        "Upcoming version"
        HTML = """<span class="since"><span class="since__hide">(</span><span class="since__text">upcoming in</span> <span class="since__value">%s</span><span class="since__hide">)</span></span>"""
        return HTML % (version)

    @macro
    def days_ago(date):
        if not date:
            return ""
        delta = datetime.now() - date
        if delta.days == 1:
            return "1 day ago"
        else:
            return "%d days ago" % delta.days

    @macro
    def github_repos():
        return repos

    @macro
    def get_milestones():
        milestones = main_repo.get_milestones()
        result : list[Milestone] = []
        ideas_milestone = None
        future_milestone = None
        for milestone in milestones:
            if milestone.title == "Future":
                future_milestone = milestone
            elif milestone.title == "Ideas":
                ideas_milestone = milestone
            else:
                result.append(milestone)
        result.append(future_milestone)
        result.append(ideas_milestone)
        return result

    @macro
    def get_milestone_issues(milestone: Milestone):
        result = []
        for issue in issues:
            if not issue.pull_request and issue.state == "open" and issue.milestone and issue.milestone.number == milestone.number:
                result.append(issue)
        return result

    @macro
    def get_version(repo: Repository) -> str:
        tag_pages = repo.get_tags()
        tags = tag_pages.get_page(0)
        if len(tags) == 0:
            return ""
        return "[%s](https://github.com/containerssh/%s/releases/tag/%s)" % (tags[0].name, repo.name, tags[0].name)

    @macro
    def github_issues():
        result = []
        for issue in issues:
            if not issue.pull_request and issue.state == "open":
                result.append(issue)
        return result

    @macro
    def github_prs():
        result = []
        for issue in issues:
            if issue.pull_request and issue.state == "open":
                result.append(issue)
        return result


if __name__ == "__main__":
    pprint.pprint(repos)
