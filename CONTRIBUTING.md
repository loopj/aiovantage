# Contributing

First off, thanks for taking the time to contribute!

## Table of contents

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [🔨 Set up Development Environment](#-set-up-development-environment)
- [💡 Adding support for new devices](#-adding-support-for-new-devices)
- [✨ Submit your work](#-submit-your-work)
- [🎨 Style guidelines](#-style-guidelines)
- [📦️ Build a package](#%EF%B8%8F-build-a-package)
- [🚀 Publish a release](#-publish-a-release)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## 🔨 Set up Development Environment

### Using `hatch`

aiovantage uses [Hatch](https://hatch.pypa.io/) to run scripts, manages virtual environments, create reproducible builds, and publish packages. Check out the [Hatch installation guide](https://hatch.pypa.io/latest/install/) to get started.

If you'd like to run a command in a virtual environment with development dependencies available, prefix it with `hatch -e dev run`. For example,

```bash
hatch -e dev run python examples/dump_system.py hostname
```

### Manually

If you'd prefer to manage your own python environment, you can install the development dependencies manually.

```bash
pip install -e ".[dev]"
```

## 💡 Adding support for new devices

### Adding a new object type to an existing controller

To add a new object type to an existing controller, follow these steps:

- Create a new [xsdata-style `@dataclass`](https://xsdata.readthedocs.io/en/latest/models.html) model in `src/aiovantage/objects/`
- The new class should inherit from the appropriate subclass expected by the controller
- Your class name should match the Vantage object name if possible, otherwise use [class metadata](https://xsdata.readthedocs.io/en/latest/models.html#class-metadata) to specify the name
- Export the class in `src/aiovantage/objects/__init__.py` so it can be automatically parsed
- Add the object name to the `vantage_types` tuple in the appropriate controller in `src/aiovantage/controllers/`, so we know to fetch it when populating the controller
- Test that the object appears in the controller, by running the `dump_system.py` example script

### Adding support for a new class of device

If you want to add support for a new class of device, you'll need to add a new controller. Create an issue to discuss the new controller before you start working on it.

## ✨ Submit your work

Submit your improvements, fixes, and new features to one at a time, using GitHub [Pull Requests](https://docs.github.com/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests).

Good pull requests remain focused in scope and avoid containing unrelated commits. If your contribution involves a significant amount of work or substantial changes to any part of the project, please open an issue to discuss it first to avoid any wasted or duplicate effort.

## 🎨 Style guidelines

This project uses [pre-commit](https://pre-commit.com/) to run code linting and formatting checks before commits are made.

To install `pre-commit` and its associated hooks, run the following:

```bash
pip install pre-commit
pre-commit install
```

To run our linters on the full code base, run the following command:

```bash
pre-commit run --all-files
```

## 📦️ Build a package

To build the package, first bump the version

```bash
hatch version <major|minor|patch>
```

Then build the package

```bash
hatch build -c
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

Don't forget to [create a release on GitHub](https://github.com/loopj/aiovantage/releases/new).
