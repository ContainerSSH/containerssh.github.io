---
title: The road to ContainerSSH 0.4: modularized structure, audit logging, and more
description: What happened to ContainerSSH 0.4? Why is it not released yet?
image: images/blog/the-road-to-0-4/preview.png
---

# The road to ContainerSSH 0.4: modularized structure, audit logging, and more
<div class="blog-meta"><small>November 25, 2020</small></div>

After a rapid rush of releases this summer we have announced that version 0.4.0 would have a long-awaited feature: [detailed audit logging](/reference/audit.md). This feature would allow for a forensic reconstruction of an SSH session. The use cases for this are diverse: from building honeypots to securing a corporate environment. We even published a [preview release](https://github.com/ContainerSSH/ContainerSSH/releases/tag/0.4.0-PR1) for test driving this feature. We even implemented an automatic upload for the audit logs to an S3-compatible object storage. So, what happened? **Why isn't 0.4.0 released yet?**

The delay has everything to do with *maintainability*. The PR-1 implementation of the audit logging was built right into ContainerSSH causing a deluge of code changes. While it technically worked, it blew up the code in size and made features extremely hard to test. Look at [this code, for example](https://github.com/ContainerSSH/ContainerSSH/blob/0.4.0-PR1/ssh/server/server.go#L231). The actual authentication code dwarfs in comparison to the audit logging parts. You could say, the code violates the [Single Responsibility Principle](https://en.wikipedia.org/wiki/Single-responsibility_principle). There is no way we could retrofit component-level tests into this.

When we began work on ContainerSSH we knew that the code quality was prototype-level at best and we'd have to overhaul large parts before the `1.0` release. In essence, **version `0.4` became the release to make that overhaul happen.** We started pulling out large parts of the codebase into [independent libraries](/contributing/libraries/) and started retrofitting them with unittests. Needless to say, moving from only having a few integration tests to writing unittests for each component unearthed a slew of bugs, which were promptly fixed.

Starting ContainerSSH with a prototyping approach wasn't a bad decision, though: it helped us getting something working fairly quickly and kept motivation high. This is especially important with a purely open source project.

Pulling everything apart into separate libraries also gave us a couple of additional advantages. We created **developer documentation for each library**, and we now also have the ability to extend ContainerSSH in a significant way.

ContainerSSH now has [clean APIs to handle SSH events](https://github.com/containerssh/sshserver). These clean APIs allow developers to plug in *additional functionality* without breaking any existing features. For example, the audit log functionality is [integrated in a separate repository with this approach](https://github.com/containerssh/auditlogintegration).

Using a layered approach gives us quite a few options. One idea we are toying with is to create [an SSH proxy](https://github.com/ContainerSSH/ContainerSSH/issues/65) that forwards connections to a backend SSH server. This would allow users to deploy ContainerSSH as a pure audit logging facility.

Another idea is to build in [PAM authentication](https://github.com/ContainerSSH/ContainerSSH/issues/64) and [enable a direct shell on the host](https://github.com/ContainerSSH/ContainerSSH/issues/66), which would enable ContainerSSH to function as a replacement for OpenSSH with the added functionality of audit logging.

If you like these ideas please comment on the issues linked above and [let us know about your use case](https://github.com/ContainerSSH/ContainerSSH/issues).

**So, when is `0.4` coming out?** We don't know yet. Our *plan is early next year*, but our focus in this release is stability.