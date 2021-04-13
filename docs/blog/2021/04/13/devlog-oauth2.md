title: DevLog: SSH authentication via OAuth2
description: Authenticating an SSH session over OAuth2 sounds crazy? Not as much as you'd think!

# DevLog: SSH authentication via OAuth2
<div class="blog-meta"><small>April 13, 2021</small></div>

Traditionally, SSH supports authentication via a number of methods. Typically, you'd use passwords or SSH keys to log in. However, other methods are also possible: keyboard-interactive can be used to ask the connecting user a series of questions. This can be used for two factor authentication, for example. GSSAPI authentication allows for using Kerberos tokens obtained, for example, by logging into a Windows domain to be used as SSH credentials.

## OAuth2: Why?

When SSH was first invented by by Tatu Ylönen in 1995 most terminal windows had the size of 80 by 25 characters. [Netscape Navigator](https://en.wikipedia.org/wiki/Netscape_Navigator) was barely a year old and systems like single sign-on weren't even on the horizon.

The SSH protocol has, of course, evolved over the years, but even the most recent RFC's that are implemented are over 10 years old.

Traditionally, large enterprises (telco providers, etc) relied on strong firewall rules to isolate their administrative (SSH) access from the Internet. In some cases central authentication was implemented, for example by means of authenticating from a central LDAP server, or via configuration management. This was rather the exception and implemented only when required by security standards such as PCI-DSS.

As companies moved ouside their traditional network environment into the cloud in recent years access control became more and more of a problem. However, this is not a new problem. [SAML](https://en.wikipedia.org/wiki/SAML_2.0) was introduced in 2005, but proved to be an unwieldy XML beast, difficult to implement.

Recently OpenID Connect (OIDC) became a very popular add-on to OAuth2 to manage single sign-on needs. (This is not to be confused with the traditional OpenID, the two are not related.) Microsoft Active Directory Federation offers OIDC support along with SAML 2.0, and [Kubernetes](https://kubernetes.io/docs/reference/access-authn-authz/authentication/) also supports OIDC as an authentication method for administrator.

**What's missing? SSH.** The method of accessing the servers running Kubernetes, or traditional workloads.

Of course, you can use GSSAPI to provide automatic login capabilities using your Windows domain, but in the age of Bring Your Own Device that's no longer appropriate. 

## OAuth2: How?

Ok, so it's not 1995 any more, how can we get SSH to authenticate via a browser-based authentication flow?

The key lies in the `keyboard-interactive` authentication method described in [RFC 4256](https://tools.ietf.org/html/rfc4256). This method is supported by almost all SSH clients and gives the SSH server the ability to send the client a list of questions the client needs to answer. It also allows the server to send the client an instruction text. This instruction text can be used to show the client a link.

From here it's fairly simple. Option one is the **authorization code flow**: client logs in to the web browser and must then copy the code back into their console. The SSH server checks their identity and that's it. [See this 17 second video.](https://youtu.be/ifP0xUraH20)

Option two is the device code flow, where the user is sent to a link and must enter a code from the SSH console. [See this 25 second video.](https://youtu.be/SGHee9cV_rA)

The latter would also lend itself to displaying a QR code, but OpenSSH, unfortunately, limits the length of the instruction field to 255 characters and doesn't support UTF-8 either.

## Client support
 
As of writing, we have tested the following clients:

- [PuTTY](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html) displays the link, but breaks the link after 78 characters and limits the instruction field to 255 characters.
- [WinSCP](https://winscp.net/) displays the instruction text, but the link is not clickable or copyable. The author of WinSCP has sent us a preview build which contains this feature.
- [FileZilla](https://filezilla-project.org/) exhibits a similar link breakage as PuTTY, but it also duplicates all `&` characters as well. [This has been fixed in a nightly build.](https://trac.filezilla-project.org/ticket/12415)
- [Termius](https://termius.com/) does not display the instruction field on mobile at all, and does not make it possible to copy or click the link on desktop. This issue has been forwarded to their dev team.
- [Bitvise](https://www.bitvise.com/) does not make it possible to copy or click the link. They are addressing this as a bug.
- [JuiceSSH](https://juicessh.com/) (Android) does not display the instruction field on mobile at all.

## When?

Soon. We don't have an exact release date, it's uncharted territory and we want to wait at least for the more popular SSH clients to release full support for this feature.

*We would like to thank everyone who helped this project with ideas, input and testing.**