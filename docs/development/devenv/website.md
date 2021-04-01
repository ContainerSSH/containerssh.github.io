title: Setting up the website development environment

<h1>Setting up the website development environment</h1>

This website is developed using [mkdocs](https://www.mkdocs.org/) using the [Material theme](https://squidfunk.github.io/mkdocs-material/). This guide will run you through the steps of setting it up.

## Installing Python

You can download Python [from the official website](https://www.python.org/downloads/). You will need at least Python 3.8.

## Cloning the repository

In order to develop this website you will need to clone the repository:

```
git clone https://github.com/containerssh/containerssh.github.io
```

## Creating a venv

Once you have all that done we recommend you create a venv to avoid polluting your computer with packages:

```
python3 -m venv /path/to/containerssh.github.io
```

You can then activate the venv using the following script:

```
venv/Scripts/activate
```

## Installing the dependencies

Now you need to install the dependencies:

```
pip install -r requirements.txt
```

## Optional: Setting the `GITHUB_TOKEN`

Some functions of the website require a working GitHub Token without any special permissions. You can [create a token here](https://github.com/settings/tokens).

You can then set the token using the command line:

=== "Linux / MacOS"
    ```
    export GITHUB_TOKEN="your-token-here"
    ```
=== "Windows (PowerShell)"
    ```
    $env:GITHUB_TOKEN="your-token-here"
    ```
=== "Windows (Command prompt)"
    ```
    set GITHUB_TOKEN=your-token-here
    ```

!!! warning
    Setting `GITHUB_TOKEN` dramatically slows down the development server because the GitHub API is queried for every refresh. Only set it when you need it.

## Running the dev server

Run the following command to get a dev server up and running:

```
python -m mkdocs serve
```

This will start the development server on [localhost:8000](https://localhost:8000).

!!! tip
    We recommend using the free [Visual Studio Code](https://code.visualstudio.com/) or the [PyCharm Community Edition](https://www.jetbrains.com/pycharm/download/) as a development environment for the website.