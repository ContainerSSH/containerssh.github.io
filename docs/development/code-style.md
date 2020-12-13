# Coding style

We don't have a strict coding convention that will force you to write code in a very specific way. Instead, we will try to explain how we think about ensuring quality in this document.

Please, feel free to bring your own ideas and [discuss on the discussions board](https://github.com/ContainerSSH/ContainerSSH/discussions).

## Object-Oriented Programming

Wait, what? OOP in Go?

Yes, bear with me. Go has a concept called [receivers](https://gobyexample.com/methods) that allow you to pass a context structure to a function. This is very similar to how private and public variables are handled in OOP languages.

The main benefit of receivers is that they can be used to implement [interfaces](https://gobyexample.com/interfaces). Interfaces, in turn, give us the ability to create a standardized API between components without involving a network.
 
The [log library](https://github.com/containerssh/log/), for example, provides the `Logger` interface and then also includes an implementation for the logger. However, at no point do we have a hard dependency on the actual implementation of the logger. If in the future the implementation turns out to be insufficient replacing it is easy.

We use this pattern extensively to separate the [ContainerSSH libraries](https://github.com/containerssh/) from each other. We are then using these interfaces to write tests for each library without having to run an end-to-end test for every test.

## Testing

This brings us to the topic of testing. ContainerSSH is a security-relevant software so we want to ensure a reasonable level of quality. In the beginning we had a manual testing protocol, but as features became more extensive it became very hard to test each feature for each release.

We also rely on GitHub's Dependabot to update our external dependencies. Without tests we would have a very hard time verifying that the updated third party library did not break something.

When it comes to test sizes we prefer having unit- or component-level tests and only have a few end-to-end tests. This is because e2e tests require several Kubernetes clusters and a Docker server so they are quite slow and hard to run in a development environment. We want to make sure that contributors can avoid the frustrating cycle of Commit, Push, Wait for CI, Realize it breaks, Repeat, so running tests quickly is very desirable. End-to-end tests also have the drawback that if they break the bug can be hard to track down.

In summary, we prefer having granular tests for each library. This is why we have split the codebase into [several libraries on GitHub](https://github.com/containerssh/). Each library has their own tests and own CI setup. When a library needs to interact with a different library we usually implement an interface with a well-described contract. This contract can then be used to write tests against.

When it comes to actually writing the tests we follow the [Detroit/classicist school of testing](https://medium.com/dev-genius/detroit-and-london-schools-of-test-driven-development-3d2f8dca71e5). Our tests are put in the separate [`_test` package](https://gobyexample.com/testing) and test our code from the outside.

## Structuring your code

In the early versions of ContainerSSH we had a rather monolithic application. The core SSH server would perform logging, write metrics, deal with SSH specifics, etc. Needless to say, writing and maintaining the code became very tedious. It took a a large amount of concentration to find the right parts to implement a change on, and finding bugs often took a slog through layers and layers of code.

This is frustrating and hinders productivity. We don't want contributors to spend more time finding the right code piece than implementing the actual change. This requires a short-term sacrifice: better code structure and abstractions. Yes, we know, they are not fun to implement. When we refactored ContainerSSH in version 0.4 the size of the codebase grew by over 50%. However, this change was worth it as it paved the way for adding new features without pain in the future.

Our aim is that each library or component should deal with one concern. The [auth library](https://github.com/containerssh/auth) should deal with authentication, the [sshserver library](https://github.com/containerssh/sshserver) with SSH, and so on. This goes so far that the integration work between two libraries is often relegated to a separate library. Sticking with the example before, the [authintegration library](https://github.com/containerssh/authintegration) creates a layer for the SSH server and calls the authentication library when user authentication is desired.

There is no hard and fast rule what (not) to separate. Creating a prototype as a single library is fine. If it turns out that it is too unwieldy to test or use it can be refactored. Thankfully, we have no quarterly deadlines we need to hit, so a feature is released when it is ready.  

## Third party libraries

We group third party dependencies in two categories: primary and utility. Primary dependencies are the ones that are required to fulfil the primary function of a library. For example, the Docker libraries would be a primary dependency for the [dockerrun library](https://github.com/containerssh/dockerrun). These libraries are integrated directly. Needless to say, the libraries include component-level tests to verify the integration still works.

This stands in contrast to utility libraries. For example, we use [Yuki Iwanaga's defaults library](github.com/creasty/defaults) to provide default values for structs in multiple ContainerSSH libraries. However, since the library may need to be replaced in the future we opt to create a wrapping layer called [structutils](https://github.com/ContainerSSH/structutils). This wrapping layer describes our expectation towards the library and also includes tests to verify  that this functionality still holds true.

## Dealing with networks

ContainerSSH integrates several components that can be reached over the network, for example the config server, the auth server, or even Docker and Kubernetes. While in the development environment everything typically works fine, they can be notoriously unreliable in production. 

What's worse, these issues are extremely hard to debug, so we aim to prevent them. Our two choices of prevention are [contexts](https://gobyexample.com/context) and retries.

Contexts in Go provide a graceful way to observe timeouts. The simplest way to create a timeout context is the following:

```go
ctx, cancelFunc := context.WithTimeout(
    context.Background,
    60 * time.Second,
)
defer cancelFunc()
```

!!! warning
    It is very important that you include the call to `cancelFunc()` otherwise you may leak memory.

Now that you have a context you can check it inside a loop:

```go
loop:
for {
    select {
    case <-ctx.Done():
        break loop
    default:
        //Continue whatever you need to do
    }
}
```

**Retries** also come into play: when performing a call over the network you may encounter random errors you may wish to retry. We frequently couple the context with retries:

```go
var lastError error
loop:
for {
    lastError = someNetworkCall()
    if err == nil {
        break loop
    } else {
        logger.Warningf(
            "failed to perform network call, retrying in 10 seconds (%v)",
            lastError,
        )
    }
    select {
    case <-ctx.Done():
        break loop
    case <-time.After(10 * time.Second):
       // Next loop
    }
}
if lastError != nil {
    logger.Errorf("failed to perform network call, giving up (%v)", err)
    return lastError
}
```

## Microserviecs

The above-mentioned networks also factor into the concept of *microservices*. ContainerSSH uses two external services for *authentication* and *configuration*. These are provided for user convenience making it easier to integrate ContainerSSH. However, we do not plan to add more microservices for development convenience. We want to avoid having more deployment YAML files than actual code. ContainerSSH should be simple to run, even if that means making it harder to structure the code.

## Conclusion

We hope you now have a better idea of the design goals of ContainerSSH. However, it is worth reiterating: there is room for disagreement. If in doubt, feel free to submit a simple pull request and we'll work from there. If your solution is missing bits we'll work with you or even add missing code pieces to come to an agreeable solution.