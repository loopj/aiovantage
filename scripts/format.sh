#!/bin/sh -e
set -x

ruff src examples --fix
black src examples