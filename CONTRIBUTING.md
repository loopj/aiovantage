# Contributing

First off, thanks for taking the time to contribute!

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
## Table of Contents

- [🛠️ Set up Development Environment](#-set-up-development-environment)
- [✨ Submit your work](#-submit-your-work)
- [🎨 Style guidelines](#-style-guidelines)
- [📦️ Build a package](#%EF%B8%8F-build-a-package)
- [🚀 Publish a release](#-publish-a-release)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## 🛠️ Set up Development Environment

`aiovantage` uses [Hatch](https://hatch.pypa.io/) to run scripts, create reproducible builds and environments, and publish packages. Check out the [Hatch installation guide](https://hatch.pypa.io/latest/install/) to get started.

## ✨ Submit your work

Good pull requests, whether patches, improvements, or new features, are a fantastic help. They should remain focused in scope and avoid containing unrelated commits. If your contribution involves a significant amount of work or substantial changes to any part of the project, please open an issue to discuss it first. This will help avoid any wasted or duplicate effort. If you're unsure about whether a contribution is appropriate, feel free to ask!

## 🎨 Style guidelines

We use `mypy`, `ruff`, and `black` for code linting and formatting. Linting helps ensure code quality and consistency throughout the project.

To run linting locally, execute the following command:

```bash
hatch run lint:all
```

This command will run the linting tools, checking for against the defined linting rules in the `pyproject.toml` file.

While you're free to use your preferred linters or editor plugins, please ensure that your changes adhere to our linting rules and pass the CI checks.

## 📦️ Build a package

To build the package, first bump the version

```bash
hatch version <major|minor|patch>
```

Then build the package

```bash
hatch build
```

## 🚀 Publish a release

Follow these steps to publish the release on PyPi.

Commit `src/aiovantage/__about__.py` to source control

```bash
git add src/aiovantage/__about__.py
git commit -m "Preparing release `hatch version`"
```

Tag the release

```bash
git tag `hatch version`
git push && git push --tags
```

Publish the release to PyPi

```bash
hatch publish
```
