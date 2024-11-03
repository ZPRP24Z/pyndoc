# Pandoc AST
Pandoc's AST is a representation used as a tool for conversion of markup languages.

As the AST is not well documented on Pandoc's side, this document will attempt to break down its notation to make it easier to understand.

## 1. Converting a document to AST Representation
Pandoc provides a way to convert a document to AST representation via

```sh
pandoc <file> -t native
```

## 2. Structure

The document is broken down and stored in a list-like structure enclosed with square brackets. The structure contains every component of the document separated by commas.

### 2.1 Headers

An example level 1 header will look like this in the AST representation:
```
Header 1 ("Example-title", [], [])[Str "Example", Space, Str "Title"]
```
Where:
- `Header 1` represents the name of the component
- `"Example-title"` represents the component's title
- `[Str "Example", Space, Str "Title"]` represents the contents of the header

#### 2.1.1 Markdown
Markdown's headers are very easily translated to AST representation:

* `#` - `Header 1`
* `##` - `Header 2`
* `###` - `Header 3`

... etc.

#### 2.1.2 LaTeX
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

#### 2.1.3 typst
Typst headers/headings have more styling options than markdown ones. For more information suggested reading [typst heading documentation](https://typst.app/docs/reference/model/heading/).
Typst headings start with one or more `=` symbols followed by a space. The number of `=` determines the heading [depth](https://typst.app/docs/reference/model/heading/#parameters-depth).
* `=` - Header 1
* `==` - Header 2
* `===` - Header 3

etc

When it comes to markdown to typst conversion, Pandoc, apart form transforming `#` into `=`, adds a [typst supplement] (https://typst.app/docs/reference/model/heading/#parameters-supplement) based on the heading text.
Example:
```
## My Header
```
transforms into:
```
== My Header
<my-header>
```

### 2.2 Paragraphs

AST uses a `Para` component to represent paragraphs, an example paragraph looks like this:
```
Para [Str "Example", Space, Str "paragraph"]
```

For LaTeX, this should not be confused with `\paragraph{}`, which is **not** converted to `Para`, but to a Level 3 header. (see [2.1.2](#212-latex))


### 2.3 MD Quotes

In Markdown, a quote is a way to indicate a block of text that represents a quotation or reference. This is typically done using the > character at the beginning of each line of the quote.

Parser converts phrase 
```
> Hello world!
```
into 
```
[BlockQuote
 [Para [Str "Hello",Space,Str "world!"]]]
```

Where:
- `Block Quote` represents the name of the component
- `Para` represents single paragraph
- `[Str "Hello",Space,Str "world!"]` represents the contents of the paragraph

### 2.4 Code Blocks
In Markdown, code blocks are used to display code snippets or text exactly as written, preserving whitespace and formatting.

Parser converts phrase
```
Hello world!
```
into
```
[CodeBlock ("",[],[]) "Hello world!"]
```

Where: 
- `Code block` represents the name of the component
- `("",[],[])` represents metadata about the code block
    - First element `""`  is for the language class, Here it's empty meaning no specific language is indicated
    - Second element `[]` is for additional classes that could be applied to the code block
    - Third element `[]` is for any additional attributes (like custom identifiers or key-value pairs), but it’s also empty here
- `[Str "Hello",Space,Str "world!"]` represents the contents of the paragraph

### 2.5 MD Tables

In Markdown, tables are created using pipes | to separate columns and hyphens - to create headers.

Parser converts phrase
```
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Row 1    | Data     | More     |
| Row 2    | Data     | More     |
```
into
```
[Table [] [AlignDefault,AlignDefault,AlignDefault] [0.0,0.0,0.0]
 [[Plain [Str "Column",Space,Str "1"]]
 ,[Plain [Str "Column",Space,Str "2"]]
 ,[Plain [Str "Column",Space,Str "3"]]]
 [[[Plain [Str "Row",Space,Str "1"]]
  ,[Plain [Str "Data"]]
  ,[Plain [Str "More"]]]
 ,[[Plain [Str "Row",Space,Str "2"]]
  ,[Plain [Str "Data"]]
  ,[Plain [Str "More"]]]]]
```

Where:
- `Table` represents the name of the component
- `[]` represents optional table attributes, such as caption or label, which are not present here
- `[AlignDefault,AlignDefault,AlignDefault]` specifies the alignment of each column
- `[0.0,0.0,0.0]` represents relative column widths, where 0.0 means that the widths are unspecified, so they will be automatically adjusted
- `[[Plain [Str "Column",Space,Str "1"]] ... ]` represents a header cell
- `[Str "Column",Space,Str "1"]` represents content of the cell
