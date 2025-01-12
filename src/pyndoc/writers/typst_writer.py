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


class TypstWriter:
    """
    A class for converting an Abstract Syntax Tree (AST) representation of a document into Typst format.
    """

    def __init__(self) -> None:
        """
        Initializes the Typst writer and sets up a mapping of block types to processing methods.
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

    def _get_typst_representation(self, ast_tree: list[ASTBlock]) -> str:
        """
        Converts the given AST tree into a Typst document.

        :param ast_tree: List of AST blocks representing the document structure.
        :return: String containing the Typst representation of the document.
        """
        result = ""
        result += "\n".join(self._process_block(block) for block in ast_tree)
        return result

    def _process_block(self, block: ASTBlock) -> str:
        """
        Processes a single AST block using the appropriate handler.

        :param block: The AST block to process.
        :return: The Typst representation of the block.
        """
        handler = self.block_handlers.get(block.__class__.__name__, self._process_unknown)
        try:
            return handler(block)
        except Exception as e:
            return f"// Error processing block {block.__class__.__name__}: {str(e)}"

    def _process_para(self, block: Para) -> str:
        """
        Processes a paragraph block.

        :param block: The paragraph block.
        :return: The Typst representation of the paragraph.
        """
        return f"{self._process_contents(block.contents.contents)}\n\n"

    def _process_emph(self, block: Emph) -> str:
        """
        Processes an emphasized (italic) text block.

        :param block: The emphasized text block.
        :return: The Typst representation of the emphasized text.
        """
        return f"*_{self._process_contents(block.contents.contents)}_*"

    def _process_strong(self, block: Strong) -> str:
        """
        Processes a strong (bold) text block.

        :param block: The strong text block.
        :return: The Typst representation of the strong text.
        """
        contents = self._process_contents(block.contents.contents)
        return f"*{contents}*"

    def _process_code(self, block: Code) -> str:
        """
        Processes inline code.

        :param block: The inline code block.
        :return: The Typst representation of the inline code.
        """
        return f"`{self._process_contents(block.contents.contents)}`"

    def _process_code_block(self, block: CodeBlock) -> str:
        """
        Processes a block of code.

        :param block: The code block.
        :return: The Typst representation of the code block.
        """
        return f"```\n{block.contents}\n```"

    def _process_header(self, block: Header) -> str:
        """
        Processes a header block.

        :param block: The header block.
        :return: The Typst representation of the header.
        """
        level = block.contents.metadata[0] if block.contents.metadata else 1
        command = "=" * level
        return f"{command} {self._process_contents(block.contents.contents)}"

    def _process_bullet_list(self, block: BulletList) -> str:
        """
        Processes a bullet list.

        :param block: The bullet list block.
        :return: The Typst representation of the bullet list.
        """
        items = "\n".join(
            f"- {self._process_contents(item.contents.contents)}"
            for item in block.contents.contents
            if isinstance(item, (BulletList, Plain))
        )
        return items

    def _process_ordered_list(self, block: OrderedList) -> str:
        """
        Processes an ordered list.

        :param block: The ordered list block.
        :return: The Typst representation of the ordered list.
        """
        items = "\n".join(
            f"+ {self._process_contents(item.contents.contents)}"
            for item in block.contents.contents
            if isinstance(item, Plain)
        )
        return items

    def _process_table(self, block: Table) -> str:
        """
        Processes a table.

        :param block: The table block.
        :return: The Typst representation of the table.
        """
        num_columns = len(block.contents.contents[0].contents.contents[0].contents.contents)

        headers = []
        for row in block.contents.contents[0].contents.contents:
            headers.append(
                ", ".join(f"[*{self._process_contents(cell.contents.contents)}*]" for cell in row.contents.contents)
            )

        body_rows = []
        for row in block.contents.contents[1].contents.contents:
            body_rows.append(
                ", ".join(f"[{self._process_contents(cell.contents.contents)}]" for cell in row.contents.contents)
            )

        table_representation = f"#table(\n  columns: {num_columns},\n  " + ",\n  ".join(headers + body_rows) + "\n)"
        return table_representation

    def _process_str(self, block: Str) -> str:
        """
        Processes a string block.

        :param block: The string block.
        :return: The Typst representation of the string.
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
        :return: A Typst comment indicating an unknown block type.
        """
        return f"// Unknown block: {block.__class__.__name__}"

    def _process_contents(self, contents: list[ASTBlock]) -> str:
        """
        Processes a list of content blocks.

        :param contents: List of AST blocks or strings.
        :return: A concatenated string of processed blocks.
        """
        try:
            return "".join(self._process_block(item) for item in contents)
        except Exception as e:
            return f"// Error processing contents: {str(e)}"

    def print_tree(self, ast_tree: list[ASTBlock]) -> None:
        """
        Prints the Typst representation of an AST tree.

        :param ast_tree: List of AST blocks representing the document structure.
        """
        print(self._get_typst_representation(ast_tree))

    def write_tree_to_file(self, filename: str, ast_tree: list[ASTBlock]) -> None:
        """
        Writes the Typst representation of an AST tree to a file.

        :param filename: The name of the file to write to.
        :param ast_tree: List of AST blocks representing the document structure.
        """
        with open(filename, "w") as fp:
            fp.write(self._get_typst_representation(ast_tree))
