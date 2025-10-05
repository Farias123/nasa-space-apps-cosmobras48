#!/bin/sh -e
set -x

ruff check ./backend/src --fix --unsafe-fixes
ruff format ./backend/src
