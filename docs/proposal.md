# Pyndoc - Design Proposal

*Pyndoc* will be a CLI for conversion of markup languages, functioning effectively as an alternative to [Pandoc](https://github.com/jgm/pandoc). The application will be compatible with Pandoc's Abstract Syntax Tree (AST).

The primary goal of the project is to make the CLI easily extensible in terms of new formats.

## Target Capabilities (core)
- Conversion of markup languages
- Compatibility with Pandoc AST
- Implementation of `GitHub Flavored Markdown` as an input
- Implementation of `LaTeX` and `typst` as an output
- A CLI interface
- Interface for easy implementation of new formats in the future
### Usability Features:
- Options to specify input and output files
- Flag options for output or detailed error messages
## Technology stack
- Programming language: `Python 3.12`
- Issue tracker: `GitHub Issues`
- Additional tools:
	- `Black`
	- `Ruff`
	- `Sphinx`
	- `GNU make`
	- `Poetry`
	- `Tox`
	- `Pytest`

## Bibliography
- [Pandoc Documentation](https://pandoc.org/MANUAL.htmlPandoc)
- [Typst Documentation](https://typst.app/docs/)
- [LaTeX Documentation](https://www.latex-project.org/help/documentation/)
- [GitHub Flavored Markdown Spec](https://github.github.com/gfm/)
