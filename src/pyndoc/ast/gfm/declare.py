import pyndoc.ast.blocks as ast


def declare_gfm():
    """
    Function declaring the regular expressions for each block and instructions for conversion to AST.
    The "contents" group will be used as the block's contents
    """
    declared_blocks = {
        r"^#{1,6} (?P<contents>.*$)": ast.Header,
        r"(\*{1})(?P<contents>[^*\n]+?)(\*{1})": ast.Emph,
        r"(\*{2})(?P<contents>\*?[^\n]+?\*?)(\*{2})": ast.Strong,
        r"(^|[^`])(`{1,2})(?P<contents>[^\n]+?)\2(?!`)": ast.Code
    }
    return declared_blocks
