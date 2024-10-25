# Pyndoc - Design Proposal

*Pyndoc* will be a CLI for conversion of markup languages, functioning effectively as an alternative to [https://github.com/jgm/pandoc](pandoc). The application will be compatible with pandoc's Abstract Syntax Tree (AST).

The primary goal of the project is to make the CLI easily extensible in terms of new formats.

## Target Capabilites (core)
- Conversion of markup languages
- Compatibility with Pandoc AST
- Implementation of `gihub flavored markdown` as an input
- Implementation of `LaTeX` and `typst` as an output
- a CLI interface
- Interface for easy implementation of new formats in the future
