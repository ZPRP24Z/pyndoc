from pyndoc.ast.basic_blocks import ASTBlock


class NativeWriter:
    def _get_native_representation(self, ast_tree: list[ASTBlock]) -> str:

        blocks_str = "\n".join(
            ["  " + str(block).replace("\n", "\n  ") + "," for block in ast_tree]
        )

        return f"[\n{blocks_str}\n]"

    def print_ast_tree(self, ast_tree: list[ASTBlock]) -> None:
        print(self._get_native_representation(ast_tree))
