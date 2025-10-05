#!/usr/bin/env bash

set -e
set -x

mypy backend/src --check-untyped-defs
ruff check backend/src
ruff format backend/src --check
