[![ContainerSSH - Launch Containers on Demand](https://containerssh.github.io/images/logo-for-embedding.svg)](https://containerssh.github.io/)

<!--suppress HtmlDeprecatedAttribute -->
<h1 align="center">The ContainerSSH Website</h1>


This repository contains the source code for the ContainerSSH website. It is built using [mkdocs](https://www.mkdocs.org/) and the [material theme](https://squidfunk.github.io/mkdocs-material/).

In order to build the website you will need [Python](https://www.python.org/) and [pip](https://pypi.org/project/pip/). You can install the required dependencies using pip:

```
pip install -r requirements.txt
```

Then you can launch the development server:

```
mkdocs serve
```

This launches the development server on http://localhost:8000/. If it doesn't work, try `python -m mkdocs serve`.