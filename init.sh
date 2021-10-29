#!/bin/bash

/usr/local/bin/python -m pip install -r requirements.txt

exec /usr/local/bin/python -m mkdocs $*