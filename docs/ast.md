# Pandoc AST
Pandoc's AST is a representation used as a tool for conversion of markup languages.

As the AST is not well documented on Pandoc's side, this document will attempt to break down its notation to make it easier to understand.

## Converting a document to AST Representation
Pandoc provides a way to convert a document to AST representation via

```sh
pandoc <file> -t native
```

## Structure

The document is broken down and stored in a list-like structure enclosed with square brackets. The structure contains every component of the document separated by commas.

### Headers

An example level 1 header will look like this in the AST representation:
```
Header 1 ("Example-title", [], [])[Str "Example", Space, Str "Title"]
```
Where:
- `Header 1` represents the name of the component
- `"Example-title"` represents the component's title
- `[Str "Example", Space, Str "Title"]` represents the contents of the header

#### Markdown
Markdown's headers are very easily translated to AST representation:

* `#` - `Header 1`
* `##` - `Header 2`
* `###` - `Header 3`

... etc.

#### LaTeX
LaTeX's headers are a bit more complicated and differ depending on the type of the highest level header and document's depth.

Consider a document in which only **3** header levels will be used. In that case, the headers will look like this:
* `\section{}` - `Header 1`
* `\subsection{}` - `Header 2`
* `\subsubsection{}` - `Header 3`

However, if we want to extend the document to 5 level headers, we can shift the current headers up a level, and insert a `chapter` or `part` level header, as a new level 1.
* `\part{}` - `Header 1`
* `\chapter{}` - `Header 2`
* `\section{}` - `Header 3`

etc

When it comes to markdown to LaTeX conversion, Pandoc handles this in the following way:
* `#` - `\section{}`
* `##` - `\subsection{}`
* `###` - `\subsubsection{}`
* `####` - `\paragraph{}`
* `#####` - `\subparagraph{}`
* `######...` - converted into `Para`
