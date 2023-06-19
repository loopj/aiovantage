# Contributing

`aiovantage` uses [Hatch](https://hatch.pypa.io/) to run scripts, create reproducible builds, and publish packages.
Check out the [Hatch installation guide](https://hatch.pypa.io/latest/install/) to get started.

## Linting

```console
$> hatch run lint:all
```

## Building

Bump the version

```console
$> hatch version [major|minor|patch]
```

Build the package

```console
$> hatch build
```

## Publishing

Commit `src/aiovantage/__about__.py` to source control.

```console
$> git add src/aiovantage/__about__.py
$> git commit -m "Preparing for release"
```

Tag the release

```console
$> git tag `hatch version`
$> git push && git push --tags
```

Publish the release to PyPi

```console
$> hatch publish
```
