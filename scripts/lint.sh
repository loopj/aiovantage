#!/usr/bin/env bash

set -e
set -x

mypy src examples
ruff src examples
black src examples --check