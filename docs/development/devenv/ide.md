<h1>Setting up an IDE</h1>

We strongly recommend setting up an IDE to warn you about potential issues and make the development process easier.

## Visual Studio Code

[Visual Studio Code](https://code.visualstudio.com/) is a free IDE for various languages from Microsoft for Windows, MacOS and Linux. It can be installed without admin permissions.

Once you have installed it, please click the "Extensions" icon on the left and install the "Go" extension.

You can then click the "Explorer" icon and click the "Clone Repository" button to clone a [ContainerSSH repository](https://github.com/containerssh).

When you clone the repository you will be asked to install other tools, such as the [delve debugger](https://github.com/go-delve/delve). Please install them.

Once the repository is set up you can go to the file you want to run (e.g. `cmd/containerssh/containerssh.go`), then go to the *Run* &rarr; *Add configuration*. You can then customize the parameters of running the program (e.g. where to get the config file from).

To run tests open the test file (e.g. `godogs_test.go`), click on `TestMain` and click the little "run test" text that comes up.

The details of running ContainerSSH are discussed in the [Getting started with ContainerSSH Development](../getting-started.md) guide. 

## Goland

[Goland](https://www.jetbrains.com/go/) is a commercial IDE from Jetbrains often used for Go development. It contains a number of analysis tools and quality of life features making it a popular choice.

We recommend installing Goland using the [Jetbrains Toolbox](https://www.jetbrains.com/toolbox-app/) which will also keep it up to date.

Once you launch Goland you will have the option to directly clone a Git repository. However, we recommend first going into the settings, then to *Go* &rarr; `GOROOT` and setting up Go.

Once you have cloned the repository you can navigate to the file you want to run (e.g. `cmd/containerssh/containerssh.go`), then click the little "run" icon next to the `main` function and click the "Create" button. This will create a configuration you can edit from the "Run" menu.

To run the tests you can open the specific test you want to run or create a `go test` configuration from the Run menu.

The details of running ContainerSSH are discussed in the [Getting started with ContainerSSH Development](../getting-started.md) guide.
