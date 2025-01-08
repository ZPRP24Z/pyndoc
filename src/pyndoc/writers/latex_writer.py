from pyndoc.ast.basic_blocks import ASTBlock
from pyndoc.ast.blocks import Space, Str, SoftBreak, Header, Para, Emph, Strong, Code, BulletList, Plain


class LatexWriter:
    def __init__(self) -> None:
        self.block_handlers = {
            "Para": self._process_para,
            "Emph": self._process_emph,
            "Strong": self._process_strong,
            "Code": self._process_code,
            "Header": self._process_header,
            "BulletList": self._process_bullet_list,
            "Str": self._process_str,
            "Space": self._process_space,
            "SoftBreak": self._process_soft_break,
        }

    def _get_latex_representation(self, ast_tree: list[ASTBlock]) -> str:
        result = "\\documentclass{article}\n\\begin{document}\n"
        result += "\n".join(self._process_block(block) for block in ast_tree)
        result += "\n\\end{document}"
        return result

    def _process_block(self, block: ASTBlock) -> str:
        handler = self.block_handlers.get(block.name, self._process_unknown)
        return handler(block)

    def _process_para(self, block: Para) -> str:
        return f"{self._process_contents(block.contents.contents)}\n"

    def _process_emph(self, block: Emph) -> str:
        return f"\\emph{{{self._process_contents(block.contents.contents)}}}"

    def _process_strong(self, block: Strong) -> str:
        return f"\\textbf{{{self._process_contents(block.contents.contents)}}}"

    def _process_code(self, block: Code) -> str:
        return f"\\texttt{{{self._process_contents(block.contents.contents)}}}"

    def _process_header(self, block: Header) -> str:
        level = block.contents.metadata[0] if block.contents.metadata else 1
        commands = {1: "section", 2: "subsection", 3: "subsubsection", 4: "paragraph", 5: "subparagraph"}
        command = commands.get(level, "paragraph")
        return f"\\{command}{{{self._process_contents(block.contents.contents)}}}"

    def _process_bullet_list(self, block: BulletList) -> str:
        items = "\n".join(
            f"\\item {self._process_contents(item.contents.contents)}"
            for item in block.contents.contents
            if isinstance(item, (BulletList, Plain))
        )
        return f"\\begin{{itemize}}\n{items}\n\\end{{itemize}}"

    def _process_str(self, block: Str) -> str:
        return block.contents

    def _process_space(self, block: Space) -> str:
        return " "

    def _process_soft_break(self, block: SoftBreak) -> str:
        return "\n"

    def _process_unknown(self, block: ASTBlock) -> str:
        return f"% Unknown block: {block.name}"

    def _process_contents(self, contents: list[ASTBlock]) -> str:
        return "".join(self._process_block(item) for item in contents)

    def print_tree(self, ast_tree: list[ASTBlock]) -> None:
        print(self._get_latex_representation(ast_tree))

    def write_tree_to_file(self, filename: str, ast_tree: list[ASTBlock]) -> None:
        with open(filename, "w") as fp:
            fp.write(self._get_latex_representation(ast_tree))
