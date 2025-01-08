from pyndoc.ast.basic_blocks import ASTBlock
from pyndoc.ast.blocks import Space, Str, SoftBreak, Header, Para, Emph, Strong, Code, BulletList, Plain, OrderedList


class TypstWriter:
    def __init__(self) -> None:
        self.block_handlers = {
            "Para": self._process_para,
            "Emph": self._process_emph,
            "Strong": self._process_strong,
            "Code": self._process_code,
            "Header": self._process_header,
            "BulletList": self._process_bullet_list,
            "OrderedList": self._process_ordered_list,
            "Str": self._process_str,
            "Space": self._process_space,
            "SoftBreak": self._process_soft_break,
        }

    def _get_typst_representation(self, ast_tree: list[ASTBlock]) -> str:
        result = ""
        result += "\n".join(self._process_block(block) for block in ast_tree)
        return result

    def _process_block(self, block: ASTBlock) -> str:
        handler = self.block_handlers.get(block.__class__.__name__, self._process_unknown)
        try:
            return handler(block)
        except Exception as e:
            return f"// Error processing block {block.__class__.__name__}: {str(e)}"

    def _process_para(self, block: Para) -> str:
        return f"{self._process_contents(block.contents.contents)}\n\n"

    def _process_emph(self, block: Emph) -> str:
        return f"*_{self._process_contents(block.contents.contents)}_*"

    def _process_strong(self, block: Strong) -> str:
        contents = self._process_contents(block.contents.contents)
        return f"*{contents}*"

    def _process_code(self, block: Code) -> str:
        return f"`{self._process_contents(block.contents.contents)}`"

    def _process_header(self, block: Header) -> str:
        level = block.contents.metadata[0] if block.contents.metadata else 1
        command = "=" * level
        return f"{command} {self._process_contents(block.contents.contents)}"

    def _process_bullet_list(self, block: BulletList) -> str:
        items = "\n".join(
            f"- {self._process_contents(item.contents.contents)}"
            for item in block.contents.contents
            if isinstance(item, (BulletList, Plain))
        )
        return items

    def _process_ordered_list(self, block: OrderedList) -> str:
        items = "\n".join(
            f"+ {self._process_contents(item.contents.contents)}"
            for item in block.contents.contents
            if isinstance(item, Plain)
        )
        return items

    def _process_str(self, block: Str) -> str:
        return block.contents

    def _process_space(self, block: Space) -> str:
        return " "

    def _process_soft_break(self, block: SoftBreak) -> str:
        return "\n"

    def _process_unknown(self, block: ASTBlock) -> str:
        return f"// Unknown block: {block.__class__.__name__}"

    def _process_contents(self, contents: list[ASTBlock]) -> str:
        try:
            return "".join(self._process_block(item) for item in contents)
        except Exception as e:
            return f"// Error processing contents: {str(e)}"

    def print_tree(self, ast_tree: list[ASTBlock]) -> None:
        print(self._get_typst_representation(ast_tree))

    def write_tree_to_file(self, filename: str, ast_tree: list[ASTBlock]) -> None:
        with open(filename, "w") as fp:
            fp.write(self._get_typst_representation(ast_tree))
