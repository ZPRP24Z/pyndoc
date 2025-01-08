# Pyndoc - An alternative to Pandoc written in python

![GitHub License](https://img.shields.io/github/license/ZPRP24Z/pyndoc)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/ZPRP24Z/pyndoc/format.yml?label=formatting)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/ZPRP24Z/pyndoc/test.yml?label=tests)
![Readthedocs build status](https://readthedocs.org/projects/pyndoc/badge/?version=latest&style=flat)


*Pyndoc* is a CLI for conversion of markup languages, functioning effectively as an alternative to [Pandoc](https://github.com/jgm/pandoc).

The primary goal of the project is to make the CLI easily extensible in terms of new formats.

For development use see [development instructions](https://pyndoc.readthedocs.io/en/latest/development-instructions.html)

## Getting Started

To start using `pyndoc`, you need to build the package first. This project uses [Poetry](https://python-poetry.org/) as a packaging and dependency manager. To install all dependencies run:

```sh
poetry install
```

Then you can build the project with:

```sh
poetry build
```

Then, you can safely install the package using `pipx`:

```as
pipx install -e .
```

## Documentation

Project documentation is available [here](https://pyndoc.readthedocs.io/en/latest/index.html).
