<h1>Implementing your first SSH server</h1>

This section will guide you through implementing your first SSH server in go and combine it with Docker.

!!! tip
    If you are new to SSH development please read our [Understanding SSH](ssh.md) guide first.

!!! tip
    The source code for this mini project is [available on GitHub](https://github.com/ContainerSSH/minicontainerssh/blob/master/main.go).
    
## Step 1: The basic loop

Let's start off easy: implementing a TCP server. On *NIX systems listen sockets can be started using the `listen()` system call and Go follows that pattern nicely:

```go
listener, err := net.Listen("tcp", "0.0.0.0:2222")
```

However, `net.Listen` does not accept connections, it merely opens a listen socket telling the system kernel that it should not reject connections coming to the specified port.

Now we need to accept any incoming connections. Let's do that:

```go
tcpConn, err := listener.Accept()
```

This call will *block* until a client connects or the listen socket is closed. Let's ignore the second case and focus on the first. With `tcpConn` we now have an open plain text TCP connection. We can read from it, we can write to it, but until we call `listener.Accept()` again we won't get any new connections. So let's put it in a loop:

```go
for {
    tcpConn, err := listener.Accept()
}
```

Cool, so now we can accept multiple connections! However, these are still just plain text connections, so let's make them into an SSH connection:

```go
sshConn, chans, reqs, err := ssh.NewServerConn(tcpConn, sshConfig)
```

We won't go into the details of `sshConfig` here, let's focus on the returned variables instead. The first returned variable, `sshConn` is the raw SSH connection. If you use an IDE you can use code completion to figure out some useful methods it contains, for example for closing the connection.

More interesting to us are the `chans` and `reqs` variables, however. The `chans` variable contains a [Go channel](https://gobyexample.com/channels) containing SSH channel request. When a client wants to open a new channel we can read from this Go channel and process the request. (Confusing, we know, two things with the same name.)

The `reqs` variable is also a Go channel, but it contains global requests. We won't deal with these now, so let's disregard these completely:

```go
go ssh.DiscardRequests(reqs)
```

As you can see we used the `go` keyword. This is running the method called in a [goroutine](https://gobyexample.com/goroutines). If you are coming from another programming language you can imagine these as multi-threaded coroutines. Suffice it to say, they won't block our main loop.

Back to the `chans`, let's deal with them too. Let's handle them in a method called `handleChannels`:

```go
go handleChannels(sshConn, chans)
```

This method will be rather simple:

```go
func handleChannels(conn *ssh.ServerConn, chans <-chan ssh.NewChannel) {
	for newChannel := range chans {
		go handleChannel(conn, newChannel)
	}
}
```

For each new channel we open yet another goroutine. Fear not, goroutines are *very* cheap in Go.

Let's deal with that channel:

```go
func handleChannel(conn *ssh.ServerConn, newChannel ssh.NewChannel) {
	if t := newChannel.ChannelType(); t != "session" {
		_ = newChannel.Reject(ssh.UnknownChannelType, fmt.Sprintf("unknown channel type: %s", t))
		return
	}
    channel, requests, err := newChannel.Accept()
    //...
}
```

So far so good, we reject all non-session channels and otherwise accept. The `channel` contains the reference to the channel, which is also an `io.Reader` and an `io.Writer` for `stdin` and `stdout`. The `requests` variable is a go channel containing SSH channel-specific requests.

Now, let's use [Docker](https://docker.io) as our backend. It's simple and it's [really well documented](https://docs.docker.com/engine/api/v1.40/). On a *NIX system we can create a Docker client like this:

```go
docker, err := client.NewClient("unix:///var/run/docker.sock", nil,  make(map[string]string))
```

Now we can loop over the requests and handle them, one by one:

```
for req := range requests {
    reply := func(success bool, message []byte) {
        if req.WantReply {
            err := req.Reply(success, message)
            if err != nil {
                closeConnections()
            }
        }
    }
    handleRequest(
        //...
    )
}
```

As you can see, the requests may need a reply, so we are constructing a simplified function to send a reply back to the SSH client.

For the final piece of our puzzle, let's implement the `handleRequest` method. For simplicity let's implement a switch-case:

```
switch req.Type {
    case "env":
        // Save environment variables for later use
    case "pty-req":
        // Set the TTY flag on the Docker client to true later
    case "window-change":
        // Use the ContainerResize method on the Docker client later
    case "shell":
        // Create a container and run it
    case "exec":
        // Create a container and run it
}
```

That's it! You can find the details on how to run a container in our highly simplified [minicontainerssh example](https://github.com/ContainerSSH/minicontainerssh/blob/master/main.go). We have skipped many parts like error handling, but it should give you a good overview of how an SSH server in Go works and how it interacts with the container backend.

Now you are ready to dive into the [internal architecture of ContainerSSH](internal-architecture.md). 