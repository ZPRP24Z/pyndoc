from pyndoc.ast.basic_blocks import ASTBlock
from pyndoc.ast.blocks import (
    Space,
    Str,
    SoftBreak,
    Header,
    Para,
    Emph,
    Strong,
    Code,
    CodeBlock,
    BulletList,
    Plain,
    OrderedList,
    Table,
)


class LatexWriter:
    """
    A class for converting an Abstract Syntax Tree (AST) representation of a document into LaTeX format.
    """

    def __init__(self) -> None:
        """
        Initializes the LaTeX writer and sets up a mapping of block types to processing methods.
        """
        self.block_handlers = {
            "Para": self._process_para,
            "Emph": self._process_emph,
            "Strong": self._process_strong,
            "Code": self._process_code,
            "CodeBlock": self._process_code_block,
            "Header": self._process_header,
            "BulletList": self._process_bullet_list,
            "OrderedList": self._process_ordered_list,
            "Table": self._process_table,
            "Str": self._process_str,
            "Space": self._process_space,
            "SoftBreak": self._process_soft_break,
        }

    def _get_latex_representation(self, ast_tree: list[ASTBlock]) -> str:
        """
        Converts the given AST tree into a LaTeX document.

        :param ast_tree: List of AST blocks representing the document structure.
        :return: String containing the LaTeX representation of the document.
        """
        result = "\\documentclass{article}\n\\begin{document}\n"
        result += "\n".join(self._process_block(block) for block in ast_tree)
        result += "\n\\end{document}"
        return result

    def _process_block(self, block: ASTBlock) -> str:
        """
        Processes a single AST block using the appropriate handler.

        :param block: The AST block to process.
        :return: The LaTeX representation of the block.
        """
        handler = self.block_handlers.get(block.__class__.__name__, self._process_unknown)
        return handler(block)

    def _process_para(self, block: Para) -> str:
        """
        Processes a paragraph block.

        :param block: The paragraph block.
        :return: The LaTeX representation of the paragraph.
        """
        return f"{self._process_contents(block.contents.contents)}\n"

    def _process_emph(self, block: Emph) -> str:
        """
        Processes an emphasized (italic) text block.

        :param block: The emphasized text block.
        :return: The LaTeX representation of the emphasized text.
        """
        return f"\\emph{{{self._process_contents(block.contents.contents)}}}"

    def _process_strong(self, block: Strong) -> str:
        """
        Processes a strong (bold) text block.

        :param block: The strong text block.
        :return: The LaTeX representation of the strong text.
        """
        return f"\\textbf{{{self._process_contents(block.contents.contents)}}}"

    def _process_code(self, block: Code) -> str:
        """
        Processes inline code.

        :param block: The inline code block.
        :return: The LaTeX representation of the inline code.
        """
        return f"\\texttt{{{block.contents}}}"

    def _process_code_block(self, block: CodeBlock) -> str:
        """
        Processes a block of code.

        :param block: The code block.
        :return: The LaTeX representation of the code block.
        """
        return f"\\begin{{verbatim}}\n{block.contents}\n\\end{{verbatim}}"

    def _process_header(self, block: Header) -> str:
        """
        Processes a header block.

        :param block: The header block.
        :return: The LaTeX representation of the header.
        """
        level = block.contents.metadata[0] if block.contents.metadata else 1
        commands = {1: "section", 2: "subsection", 3: "subsubsection", 4: "paragraph", 5: "subparagraph"}
        command = commands.get(level, "paragraph")
        return f"\\{command}{{{self._process_contents(block.contents.contents)}}}"

    def _process_bullet_list(self, block: BulletList) -> str:
        """
        Processes a bullet list.

        :param block: The bullet list block.
        :return: The LaTeX representation of the bullet list.
        """
        items = "\n".join(
            f"\\item {self._process_contents(item.contents.contents)}"
            for item in block.contents.contents
            if isinstance(item, (BulletList, Plain))
        )
        return f"\\begin{{itemize}}\n{items}\n\\end{{itemize}}"

    def _process_ordered_list(self, block: OrderedList) -> str:
        """
        Processes an ordered list.

        :param block: The ordered list block.
        :return: The LaTeX representation of the ordered list.
        """
        items = "\n".join(
            f"\\item {self._process_contents(item.contents.contents)}"
            for item in block.contents.contents
            if isinstance(item, Plain)
        )
        return f"\\begin{{enumerate}}\n{items}\n\\end{{enumerate}}"

    def _process_table(self, block: Table) -> str:
        """
        Processes a table.

        :param block: The table block.
        :return: The LaTeX representation of the table.
        """
        num_columns = len(block.contents.contents[0].contents.contents[0].contents.contents)
        table_alignment = f"|{'|'.join(['c'] * num_columns)}|"

        rows = []

        header_row = block.contents.contents[0].contents.contents[0]
        header_content = " & ".join(
            self._process_contents(cell.contents.contents) for cell in header_row.contents.contents
        )
        rows.append("\\hline")
        rows.append(f"{header_content} \\\\")
        rows.append("\\hline")

        for row in block.contents.contents[1].contents.contents:
            row_content = " & ".join(self._process_contents(cell.contents.contents) for cell in row.contents.contents)
            rows.append(f"{row_content} \\\\")
            rows.append("\\hline")

        return f"\\begin{{tabular}}{{{table_alignment}}}\n{chr(10).join(rows)}\n\\end{{tabular}}"

    def _process_str(self, block: Str) -> str:
        """
        Processes a string block.

        :param block: The string block.
        :return: The LaTeX representation of the string.
        """
        return block.contents

    def _process_space(self, block: Space) -> str:
        """
        Processes a space block.

        :param block: The space block.
        :return: A single space character.
        """
        return " "

    def _process_soft_break(self, block: SoftBreak) -> str:
        """
        Processes a soft break.

        :param block: The soft break block.
        :return: A newline character.
        """
        return "\n"

    def _process_unknown(self, block: ASTBlock) -> str:
        """
        Handles unknown block types.

        :param block: The unknown AST block.
        :return: A LaTeX comment indicating an unknown block type.
        """
        return f"% Unknown block: {block.__class__.__name__}"

    def _process_contents(self, contents: list) -> str:
        """
        Processes a list of content blocks.

        :param contents: List of AST blocks or strings.
        :return: A concatenated string of processed blocks.
        """
        return "".join(self._process_block(item) if isinstance(item, ASTBlock) else str(item) for item in contents)

    def print_tree(self, ast_tree: list[ASTBlock]) -> None:
        """
        Prints the LaTeX representation of an AST tree.

        :param ast_tree: List of AST blocks representing the document structure.
        """
        print(self._get_latex_representation(ast_tree))

    def write_tree_to_file(self, filename: str, ast_tree: list[ASTBlock]) -> None:
        """
        Writes the LaTeX representation of an AST tree to a file.

        :param filename: The name of the file to write to.
        :param ast_tree: List of AST blocks representing the document structure.
        """
        with open(filename, "w") as fp:
            fp.write(self._get_latex_representation(ast_tree))
