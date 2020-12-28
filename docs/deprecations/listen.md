---
title: Moving the Listen option
image: deprecations/listen.png
---

# Moving the ContainerSSH `listen` option {{ upcoming("0.4") }}

In ContainerSSH 0.4 we are introducing a framework to run multiple services within one daemon. In the future we want to add more services like a web-based interface.

To make this change happen we will stop treating the SSH service as *special*, so we are moving the `listen` option from the configuration root to `ssh` &rarr; `listen`:

```yaml
# Deprecated version
listen: 0.0.0.0:2222
# New version
ssh:
  listen: 0.0.0.0:2222
```

If you use the old option you will receive the following log warning:

> You are using the deprecated 'listen' option for SSH listen socket instead of the new 'ssh -> listen'. Please see https://containerssh.io/deprecations/listen for details.

If you provide both options the new option will take precedence and you will receive the following log message:

> You are using both the deprecated 'listen' and the new 'ssh -> listen' options, the new option takes precedence.  Please see https://containerssh.io/deprecations/listen for details.
