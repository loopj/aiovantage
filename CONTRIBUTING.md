# Contributing

First off, thanks for taking the time to contribute!

## Table of Contents

- [✨ Making a Pull Request](#making-a-pull-request)
- [🛠️ Tooling](#tooling)
- [👮 Linting and formatting](#linting)
- [📦️ Building a package](#building-a-package)
- [🚀 Publishing a release](#publishing-a-release)


## ✨ Making a Pull Request

Good pull requests, whether patches, improvements, or new features, are a fantastic help. They should remain focused in scope and avoid containing unrelated commits. If your contribution involves a significant amount of work or substantial changes to any part of the project, please open an issue to discuss it first. This will help avoid any wasted or duplicate effort. If you're unsure about whether a contribution is appropriate, feel free to ask!


## 🛠️ Tooling

`aiovantage` uses [Hatch](https://hatch.pypa.io/) to run scripts, create reproducible builds and environments, and publish packages. Check out the [Hatch installation guide](https://hatch.pypa.io/latest/install/) to get started.


## 👮 Linting and formatting

We use `mypy`, `ruff`, and `black` for code linting and formatting. Linting helps ensure code quality and consistency throughout the project.

To run linting locally, execute the following command:

```console
$> hatch run lint:all
```

This command will run the linting tools, checking for against the defined linting rules in the `pyproject.toml` file. Make sure your changes pass the linting checks before submitting a pull request.

While you're free to use your preferred linters or editor plugins, please ensure that your changes adhere to our linting rules and pass the CI checks.


## 📦️ Building a package

To build the package, first bump the version

```console
$ hatch version <major|minor|patch>
```

Then build the package

```
$ hatch build
```


## 🚀 Publishing a release

Follow these steps to publish the release on PyPi.

Commit `src/aiovantage/__about.py` to source control

```console
$ git add src/aiovantage/__about__.py
$ git commit -m "Preparing release `hatch version`"
```

Tag the release

```console
$> git tag `hatch version`
$> git push && git push --tags
```

Publish the release to PyPi

```console
$ hatch publish
```
