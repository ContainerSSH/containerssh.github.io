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
        return MD % (lib, lib, description, lib, lib, lib, lib, lib, lib, lib, lib, lib, lib, lib, lib, lib, lib, lib, lib, lib, lib, lib, lib)

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