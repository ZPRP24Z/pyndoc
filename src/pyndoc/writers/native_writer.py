from pyndoc.ast.basic_blocks import ASTBlock


class NativeWriter:
    def print_tree(self, ast_tree: list[ASTBlock]) -> None:
        print(ast_tree)

    def write_tree_to_file(self, filename: str, ast_tree: list[ASTBlock]) -> None:
        with open(filename, "w") as fp:
            fp.write(ast_tree.__str__())
