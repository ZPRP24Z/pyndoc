# Pyndoc - An alternative to Pandoc written in python

![GitHub License](https://img.shields.io/github/license/ZPRP24Z/pyndoc)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/ZPRP24Z/pyndoc/format_test.yml?label=tests)


*Pyndoc* will be a CLI for conversion of markup languages, functioning effectively as an alternative to [Pandoc](https://github.com/jgm/pandoc). The application will be compatible with Pandoc's Abstract Syntax Tree (AST).

The primary goal of the project is to make the CLI easily extensible in terms of new formats.

For development use see [development instructions](https://github.com/ZPRP24Z/pyndoc/wiki/Development-Instructions)

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

Currently, the project uses the Github Wiki for storing documentation, see the [Home](https://github.com/ZPRP24Z/pyndoc/wiki) page for details. In later stages of development, there are plans to switch to Github Pages.
