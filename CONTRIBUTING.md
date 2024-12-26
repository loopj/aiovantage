# Contributing

First off, thanks for taking the time to contribute!

## Table of contents

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [🔨 Set up development environment](#-set-up-development-environment)
- [💡 Adding support for new devices](#-adding-support-for-new-devices)
- [✨ Submit your work](#-submit-your-work)
- [🎨 Style guidelines](#-style-guidelines)
- [📦️ Build a package](#%EF%B8%8F-build-a-package)
- [🚀 Publish a release](#-publish-a-release)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## 🔨 Set up development environment

### Using `uv`

aiovantage uses [uv](https://docs.astral.sh/uv/) to run scripts, manage virtual environments, create reproducible builds, and publish packages. Check out the [uv installation guide](https://docs.astral.sh/uv/getting-started/installation/) to get started.

To set up your development environment, run the following commands:

```bash
# Create a virtual environment
uv venv

# Install development dependencies
uv pip install -e ".[dev]"
```

If you'd like to run a command in a virtual environment with development dependencies available, prefix it with `uv run`. For example,

```bash
uv run python examples/dump_system.py hostname
```

### Manually

If you'd prefer to manage your own python environment, you can install the development dependencies manually.

```bash
# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Install development dependencies
pip install -e ".[dev]"
```

## 💡 Adding support for new devices

### Adding a new object type to an existing controller

To add a new object type to an existing controller, follow these steps:

- Create a new [xsdata-style `@dataclass`](https://xsdata.readthedocs.io/en/latest/models.html) model in `src/aiovantage/objects/`
- The new class should inherit from the appropriate subclass expected by the controller
- Your class name should match the Vantage object name if possible, otherwise use [class metadata](https://xsdata.readthedocs.io/en/latest/models.html#class-metadata) to specify the name
- Export the class in `src/aiovantage/objects/__init__.py` so it can be automatically parsed
- Add the object type to the `vantage_types` tuple in the appropriate controller in `src/aiovantage/controllers/`, so we know to fetch it when populating the controller
- Test that the object appears in the controller as expected

### Adding support for a new class of device

If you want to add support for a new class of device, you'll need to add a new controller. Create an issue to discuss the new controller before you start working on it.

## ✨ Submit your work

Submit your improvements, fixes, and new features to one at a time, using GitHub [Pull Requests](https://docs.github.com/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests).

Good pull requests remain focused in scope and avoid containing unrelated commits. If your contribution involves a significant amount of work or substantial changes to any part of the project, please open an issue to discuss it first to avoid any wasted or duplicate effort.

## 🎨 Style guidelines

Before submitting a pull request, make sure your code follows the style guidelines. This project uses [pyright](https://microsoft.github.io/pyright/) for type checking, and [ruff](https://docs.astral.sh/ruff/) for linting and formatting.

Pull requests will trigger a CI check that blocks merging if the code does not pass the style guidelines.

### Running checks automatically with vscode

If you are using vscode, you'll be prompted to install the recommended extensions when you open the workspace.

### Running checks manually

```bash
# Run type checking
uv run pyright
```

```bash
# Run linting
uv run ruff check
```

```bash
# Format code
uv run ruff format
```

## 📦️ Build a package

To build the package, first update the version number:

```bash
bumpver update --patch # or --major --minor
```

Then build the package:

```bash
uv build
```

## 🚀 Publish a release

To publish the package to PyPi:

```bash
uv publish
```

Don't forget to [create a release on GitHub](https://github.com/loopj/aiovantage/releases/new)!
