from __future__ import annotations
import re
from datetime import datetime, timezone
import os
import pprint
import requests
import yaml
from typing import List, Dict, Optional


class Contributor:
    name: str
    github: str
    website: str
    linkedin: str
    staff: bool
    contributions: int
    avatar_url: str


class GitHubUser:
    login: str
    name: str
    avatar_url: str


class GitHubContributor(GitHubUser):
    contributions: int


class GitHubOrg:
    id: str
    members: List[GitHubUser]


class GitHubPR:
    author: str
    number: int
    title: str
    open: bool
    url: str
    can_merge: bool
    checks_status: str
    created_at: str
    repo: GitHubRepo


class GitHubRepo:
    name: str
    description: str
    url: str
    last_version: str


class GitHubIssue:
    number: int
    title: str
    open: bool
    url: str
    repo: GitHubRepo
    milestone: Optional[GitHubMilestone]
    created_at: datetime


class GitHubMilestone:
    number: int
    title: str
    repo: GitHubRepo
    url: str
    issues: List[GitHubIssue]


class GitHubClient:
    def __init__(self, token: str, org_name: str, main_repo: str):
        self._token = token
        self._org_name = org_name
        self._main_repo_name = main_repo
        self._org: Optional[GitHubOrg] = None
        self._contributors: Dict[str, GitHubContributor] = {}
        self._milestones: List[GitHubMilestone] = []
        self._repos: List[GitHubRepo] = []
        self._issues: Dict[str, List[GitHubIssue]] = {}
        self._prs: Dict[str, List[GitHubPR]] = {}

        self.get_repos()
        self.get_main_repo()

    def query(self, query: str, variables: Dict):
        headers = {"Authorization": "Bearer " + self._token}
        request = requests.post("https://api.github.com/graphql", json={'query': query, 'variables': variables},
                                headers=headers)
        if request.status_code == 200:
            return request.json()
        else:
            raise Exception("Failed to run GitHub query")

    def query_rest(self, endpoint: str):
        headers = {"Authorization": "Bearer " + self._token, "Accept": "application/vnd.github.v3+json"}
        request = requests.post("https://api.github.com" + endpoint, headers=headers)
        if request.status_code == 200:
            return request.json()
        else:
            pprint.pprint(request)
            raise Exception("Failed to run GitHub query")

    def is_staff(self, github_login: str) -> bool:
        if not self._token:
            return False
        for member in self.get_org(self._org_name).members:
            if member.login == github_login:
                return True
        return False

    def get_org(self, org_login: str) -> GitHubOrg:
        if not self._token:
            org = GitHubOrg()
            org.id = "fake"
            org.members = []
            return org
        if self._org is not None:
            return self._org
        org = GitHubOrg()
        org.members = []
        after = None
        finished = False
        while not finished:
            org_data = self.query("""
            query($orgLogin: String!, $after: String) {
              organization(login: $orgLogin) {
                id
                membersWithRole(first: 100, after: $after) {
                  nodes {
                    login
                    name
                    avatarUrl
                  }
                  pageInfo {
                    hasNextPage
                    endCursor
                  }
                }
              }
            }
            """, {"orgLogin": org_login, "after": after})

            org.id = org_data["data"]["organization"]["id"]
            for memberData in org_data["data"]["organization"]["membersWithRole"]["nodes"]:
                member = GitHubUser()
                member.login = memberData["login"]
                member.name = memberData["name"]
                member.avatar_url = memberData["avatarUrl"]
                org.members.append(member)
            finished = not org_data["data"]["organization"]["membersWithRole"]["pageInfo"]["hasNextPage"]
            after = org_data["data"]["organization"]["membersWithRole"]["pageInfo"]["endCursor"]
        self._org = org
        return org

    def get_contributor(self, username: str) -> GitHubContributor:
        if not self._token:
            contributor = GitHubContributor()
            contributor.name = "Fake Contributor"
            contributor.login = username
            contributor.contributions = 0
            return contributor
        if username in self._contributors:
            return self._contributors[username]
        finished = False
        after = None
        contributor = GitHubContributor()
        while not finished:
            contributorData = self.query("""
                query($login: String!, $orgId: ID, $after: String) {
                  user(login: $login) {
                    name
                    login
                    avatarUrl
                    contributionsCollection (organizationID: $orgId) {
                      commitContributionsByRepository(maxRepositories: 100) {
                        contributions (first: 100, after: $after) {
                          pageInfo {
                            hasNextPage
                            endCursor
                          }
                          nodes {
                            repository {
                              name
                            }
                            commitCount
                          }
                        }
                      }
                    }
                  }
                }
                """, {'login': username, 'orgId': self._org.id, 'after': after})
            contributor.name = contributorData["data"]["user"]["name"]
            contributor.login = contributorData["data"]["user"]["login"]
            contributor.avatar_url = contributorData["data"]["user"]["avatarUrl"]
            contributions = 0
            for contribution in contributorData["data"]["user"]["contributionsCollection"][
                "commitContributionsByRepository"]:

                for node in contribution["contributions"]["nodes"]:
                    contributions = contributions + node["commitCount"]
            contributor.contributions = contributions
            # TODO: handle case where there are more than 100 contributions
            finished = True
        self._contributors[username] = contributor
        return contributor

    def get_repos(self) -> List[GitHubRepo]:
        if not self._token:
            repo = GitHubRepo()
            repo.description = "Main repo"
            repo.name = self._main_repo_name
            repo.url = "https://github.com/" + self._org_name + "/" + self._main_repo_name
            return [
                repo
            ]
        if len(self._repos):
            return self._repos
        finished = False
        after = None
        repos: List[GitHubRepo] = []
        while not finished:
            repoRecords = self.query("""
                query($orgLogin: String!, $after: String) {
                  organization(login: $orgLogin) { 
                    repositories(first: 100, after: $after) {
                      pageInfo {
                        hasNextPage
                        endCursor
                      }
                      nodes {
                        name
                        description
                        url
                        refs(refPrefix: "refs/tags/",last:1) {
                          nodes {
                            name
                          }
                        }
                      }
                    }
                  }
                }
                """, {'orgLogin': self._org_name, 'after': after})
            for repoData in repoRecords["data"]["organization"]["repositories"]["nodes"]:
                repo = GitHubRepo()
                repo.name = repoData["name"]
                repo.description = repoData["description"]
                repo.url = repoData["url"]
                repo.last_version = None
                try:
                    repo.last_version = repoData["refs"]["nodes"][0]["name"]
                except KeyError:
                    pass
                except IndexError:
                    pass
                repos.append(repo)
            finished = not repoRecords["data"]["organization"]["repositories"]["pageInfo"]["hasNextPage"]
            after = not repoRecords["data"]["organization"]["repositories"]["pageInfo"]["endCursor"]
        self._repos = repos
        return repos

    def get_main_repo(self) -> GitHubRepo:
        repos = self.get_repos()
        for repo in repos:
            if repo.name == self._main_repo_name:
                return repo
        raise Exception("No main repository found")

    def get_milestones(self) -> List[GitHubMilestone]:
        if not self._token:
            return []
        if len(self._milestones):
            return self._milestones
        after = None
        finished = False
        milestones = []
        while not finished:
            milestoneData = self.query("""
            query ($orgName: String!, $repoName: String!, $after: String) { 
              organization(login:$orgName) {
                repository(name: $repoName) {
                  milestones(first: 100, after: $after, states: [OPEN]) {
                    pageInfo {
                      hasNextPage
                      endCursor
                    }
                    nodes {
                      number
                      title
                      url
                    }
                  }
                }
              }
            }
            """, {"orgName": self._org_name, "repoName": self._main_repo_name, 'after': after})
            for milestoneEntry in milestoneData["data"]["organization"]["repository"]["milestones"]["nodes"]:
                milestone = GitHubMilestone()
                milestone.number = milestoneEntry["number"]
                milestone.title = milestoneEntry["title"]
                milestone.url = milestoneEntry["url"]
                milestone.repo = self.get_main_repo()
                milestone.issues = self._get_milestone_issues(self._main_repo_name, milestone)
                milestones.append(milestone)
            after = milestoneData["data"]["organization"]["repository"]["milestones"]["pageInfo"]["endCursor"]
            finished = not milestoneData["data"]["organization"]["repository"]["milestones"]["pageInfo"]["hasNextPage"]

        versionRe = re.compile('^[0-9]+')

        def sort_key(m: GitHubMilestone) -> int:
            match = versionRe.match(m.title)
            if not match:
                return 999999999
            return 0

        milestones = list(sorted(milestones, key=sort_key))

        self._milestones = milestones
        return milestones

    def _get_milestone_issues(self, repo: str, milestone: GitHubMilestone) -> List[GitHubIssue]:
        finished = False
        after = None
        issues = []
        while not finished:
            issueData = self.query("""
            query ($orgName: String!, $repoName: String!, $milestone: Int!, $after: String) { 
              organization(login:$orgName) {
                repository(name: $repoName) {
                  milestone(number: $milestone) {
                    issues(
                      first: 100,
                      after: $after
                      states: [OPEN,CLOSED]
                    ) {
                      pageInfo {
                        hasNextPage
                        endCursor
                      }
                      nodes{
                        number
                        title
                        state
                        url
                        createdAt
                      }
                    }
                  }
                }
              }
            }
            """, {"orgName": self._org_name, "repoName": repo, 'milestone': milestone.number, 'after': after})
            for issueEntry in issueData["data"]["organization"]["repository"]["milestone"]["issues"]["nodes"]:
                issue = GitHubIssue()
                issue.number = issueEntry["number"]
                issue.title = issueEntry["title"]
                issue.open = issueEntry["state"] == "OPEN"
                issue.url = issueEntry["url"]
                issue.created_at = issueEntry["createdAt"]
                issue.milestone = milestone
                issues.append(issue)
            finished = not issueData["data"]["organization"]["repository"]["milestone"]["issues"]["pageInfo"][
                "hasNextPage"]
            after = not issueData["data"]["organization"]["repository"]["milestone"]["issues"]["pageInfo"][
                "endCursor"]
        return issues

    def _get_repo_by_name(self, repo_name: str) -> GitHubRepo:
        for repo in self.get_repos():
            if repo.name == repo_name:
                return repo
        raise Exception("No such repo")

    def get_repo_open_issues(self, repo: str) -> List[GitHubIssue]:
        if not self._token:
            issue = GitHubIssue()
            issue.number = 1
            issue.open = True
            issue.url = "http://github.com"
            issue.title = "Test issue"
            return [issue]
        if repo in self._issues:
            return self._issues[repo]
        issues = []
        milestones = self.get_milestones()
        finished = False
        after = None
        while not finished:
            issueData = self.query("""
            query ($orgName: String!, $repoName: String!, $after: String) { 
              organization(login:$orgName) {
                repository(name: $repoName) {
                  issues(
                    first: 100,
                    after: $after
                    states: [OPEN]
                  ) {
                    pageInfo {
                      hasNextPage
                      endCursor
                    }
                    nodes{
                      number
                      title
                      state
                      url
                      createdAt
                    }
                  }
                }
              }
            }
            """, {"orgName": self._org_name, "repoName": repo, 'after': after})
            for issueEntry in issueData["data"]["organization"]["repository"]["issues"]["nodes"]:
                issue = GitHubIssue()
                issue.number = issueEntry["number"]
                issue.title = issueEntry["title"]
                issue.open = True
                issue.url = issueEntry["url"]
                issue.created_at = datetime.strptime(issueEntry["createdAt"], "%Y-%m-%dT%H:%M:%S%z")
                issue.repo = self._get_repo_by_name(repo)
                issue.milestone = None
                if repo == self._main_repo_name:
                    for milestone in milestones:
                        for milestone_issue in milestone.issues:
                            if milestone_issue.number == issue.number:
                                issue.milestone = milestone
                issues.append(issue)
            finished = not issueData["data"]["organization"]["repository"]["issues"]["pageInfo"][
                "hasNextPage"]
            after = not issueData["data"]["organization"]["repository"]["issues"]["pageInfo"][
                "endCursor"]
        self._issues[repo] = issues
        return issues

    def get_repo_prs(self, repo: str) -> List[GitHubPR]:
        if not self._token:
            return []
        if repo in self._prs:
            return self._prs[repo]
        finished = False
        after = None
        prs = []
        while not finished:
            issueData = self.query("""
            query ($orgName: String!, $repoName: String!, $after: String) { 
              organization(login:$orgName) {
                repository(name: $repoName) {
                  pullRequests(
                    first: 100,
                    states: [OPEN],
                    after:$after
                  ) {
                    pageInfo {
                      hasNextPage
                      endCursor
                    }
                    nodes{
                      number
                      title
                      url
                      mergeable
                      createdAt
                      author {
                        login
                      }
                      commits(last: 1) {
                        nodes {
                          commit {
                            statusCheckRollup {
                              state
                            }
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
            """, {"orgName": self._org_name, "repoName": repo, 'after': after})
            for prEntry in issueData["data"]["organization"]["repository"]["pullRequests"]["nodes"]:
                pr = GitHubPR()
                pr.number = prEntry["number"]
                pr.title = prEntry["title"]
                pr.open = True
                pr.url = prEntry["url"]
                pr.author = prEntry["author"]["login"]
                pr.can_merge = prEntry["mergeable"]
                pr.created_at = datetime.strptime(prEntry["createdAt"], "%Y-%m-%dT%H:%M:%S%z")
                pr.repo = self._get_repo_by_name(repo)
                try:
                    pr.checks_status = prEntry["commits"]["nodes"][0]["commit"]["statusCheckRollup"]["state"]
                except KeyError:
                    pr.checks_status = "UNKNOWN"
                prs.append(pr)
            finished = not issueData["data"]["organization"]["repository"]["pullRequests"]["pageInfo"][
                "hasNextPage"]
            after = not issueData["data"]["organization"]["repository"]["pullRequests"]["pageInfo"][
                "endCursor"]
        self._prs[repo] = prs
        return prs


class ContributorsFileReader:
    def __init__(self, file: str, client: GitHubClient):
        self.file = file
        self.client = client

    def get_sorted_contributors(self) -> List[Contributor]:
        contributors: List[Contributor] = []
        with open(self.file, "r") as fh:
            public_contributors = yaml.load(fh.read(), Loader=yaml.BaseLoader)
        for public_contributor in public_contributors:
            contributor = Contributor()
            contributor.name = public_contributor["name"]
            contributor.github = public_contributor["github"]
            try:
                contributor.twitter = public_contributor["twitter"]
            except KeyError:
                contributor.twitter = None
            try:
                contributor.website = public_contributor["website"]
            except KeyError:
                contributor.website = None
            try:
                contributor.linkedin = public_contributor["linkedin"]
            except KeyError:
                contributor.linkedin = None
            contributor.staff = self.client.is_staff(contributor.github)
            github_contributor = self.client.get_contributor(contributor.github)
            contributor.avatar_url = github_contributor.avatar_url
            contributor.contributions = github_contributor.contributions
            contributors.append(contributor)
        contributors = list(reversed(sorted(contributors, key=lambda c: c.contributions)))
        contributors = sorted(contributors, key=lambda c: not c.staff)
        return contributors


gh_client = GitHubClient(os.getenv("GITHUB_TOKEN"), "ContainerSSH", "ContainerSSH")
contributorsReader = ContributorsFileReader(os.path.join(os.getcwd(), "contributors.yaml"), gh_client)


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
        delta = datetime.now(timezone.utc) - date
        if delta.days == 1:
            return "1 day ago"
        else:
            return "%d days ago" % delta.days

    @macro
    def github_repos() -> List[GitHubRepo]:
        return gh_client.get_repos()

    @macro
    def get_milestones():
        return gh_client.get_milestones()

    @macro
    def get_version(repo: GitHubRepo) -> str:
        if not repo.last_version:
            return ""
        return "[%s](%s/releases/tag/%s)" % (repo.last_version, repo.url, repo.last_version)

    @macro
    def github_issues() -> List[GitHubIssue]:
        result = []
        for repo in gh_client.get_repos():
            for issue in gh_client.get_repo_open_issues(repo.name):
                result.append(issue)
        return result

    @macro
    def github_prs() -> List[GitHubPR]:
        result = []
        for repo in gh_client.get_repos():
            for pr in gh_client.get_repo_prs(repo.name):
                result.append(pr)
        return result

    @macro
    def contributors() -> List[Contributor]:
        return contributorsReader.get_sorted_contributors()

    @macro
    def reference_outdated():
        return '''
!!! danger "Old manual"
    You are reading the reference manual of an older release. [Read the current manual &raquo;](/reference/)
'''

    @macro
    def reference_upcoming():
        return '''
!!! danger "Upcoming release"
    You are reading the reference manual of an upcoming release. [Read the current manual &raquo;](/reference/)
'''

