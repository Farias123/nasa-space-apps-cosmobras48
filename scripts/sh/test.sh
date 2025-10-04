#!/usr/bin/env bash

set -e
set -x

cd ./backend
coverage run --source=src -m pytest -ssvv
coverage report --show-missing
coverage html --title "${@-coverage}"
cd ..
