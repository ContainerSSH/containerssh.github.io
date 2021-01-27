from datetime import datetime
import os
import pprint
import yaml
from typing import List

from github import Github
from github.Repository import Repository
from github.Issue import Issue
from github.Milestone import Milestone
from github.Commit import Commit
from github.CheckRun import CheckRun

token = os.getenv("GITHUB_TOKEN")
repos = []
core_maintainers = []
if token:
    gh = Github(token)

    org = gh.get_organization("containerssh")
    members_pages = org.get_members()
    members_page = 0
    while True:
        members = members_pages.get_page(members_page)
        if len(members) == 0:
            break
        for member in members:
            core_maintainers.append(member.login)
        members_page = members_page + 1

    repoPages = org.get_repos()

    main_repo = org.get_repo("containerssh")

    repoIndex = 0
    while True:
        repoList = repoPages.get_page(repoIndex)
        if len(repoList) == 0:
            break
        repos.extend(repoList)
        repoIndex = repoIndex + 1
else:
    main_repo = None
    print("GITHUB_TOKEN not set, skipping development dashboard rendering")

with open(os.path.dirname(__file__) + "/contributors.yaml", "r") as fh:
    public_contributors = yaml.load(fh.read(), Loader=yaml.BaseLoader)


contributions = {}
contributors_dict = {}
for repo in repos:
    contributor_list = repo.get_stats_contributors()
    for contributor in contributor_list:
        if contributor.author not in contributors_dict:
            contributors_dict[contributor.author.login] = contributor.author
            contributions[contributor.author.login] = contributor.total
        else:
            contributions[contributor.author.login] = contributions[contributor.author] + contributor.total

for index, contributor in enumerate(public_contributors):
    try:
        contributor_record = contributors_dict[contributor["github"]]
        if contributor["github"] in core_maintainers:
            public_contributors[index]["core_maintainer"] = True
        else:
            public_contributors[index]["core_maintainer"] = False
        public_contributors[index]["avatar_url"] = contributor_record.avatar_url
        public_contributors[index]["contributions"] = contributions[contributor["github"]]
    except:
        public_contributors[index]["avatar_url"] = ""
        public_contributors[index]["contributions"] = 0
        public_contributors[index]["core_maintainer"] = False

public_contributors = list(reversed(sorted(public_contributors, key=lambda c: c["contributions"])))

public_contributors = sorted(public_contributors, key=lambda c: not c["core_maintainer"])


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
        result = []
        if main_repo is not None:
            milestones = main_repo.get_milestones()
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
        milestone_issues = main_repo.get_issues(milestone=milestone, state="all")
        for issue in milestone_issues:
            if not issue.pull_request and issue.milestone and issue.milestone.number == milestone.number:
                result.append(issue)
        return result

    @macro
    def get_commits_since_last_tag(repo: Repository) -> int:
        tag_pages = repo.get_tags()
        tags = tag_pages.get_page(0)
        tag = None
        if len(tags) == 0:
            commits = repo.get_commits()
        else:
            tag = tags[0]
            commits = repo.get_commits()
        page_number = 0
        count = 0
        while True:
            page = commits.get_page(page_number)
            if len(page) == 0:
                return count
            for commit in page:
                commit: Commit
                if tag is not None and commit.sha == tag.commit.sha:
                    return count
                count = count + 1
            page_number = page_number + 1

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

    @macro
    def github_checks(issue: Issue):
        commits = issue.as_pull_request().get_commits()
        commit: Commit = commits.get_page(0)[0]
        check_runs = commit.get_check_runs()
        page_number = 0
        status = 'success'
        while True:
            page: List[CheckRun] = check_runs.get_page(page_number)
            if len(page) == 0:
                break
            for check in page:
                if check.conclusion == "success":
                    continue
                status = check.conclusion
            page_number = page_number + 1
        return status

    @macro
    def contributors():
        return public_contributors

    @macro
    def outdated():
        return '''
!!! danger "Old manual"
    You are reading the reference manual of an older release. [Read the current manual &raquo;](/reference/)
'''


if __name__ == "__main__":
    pprint.pprint(repos)
