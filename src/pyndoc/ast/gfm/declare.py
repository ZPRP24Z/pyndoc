import pyndoc.ast.blocks as ast


def declare_gfm():
    """
    Function declaring the regular expressions for each block and instructions for conversion to AST.
    The "contents" group will be used as the block's contents
    """
    declared_blocks = {
        # match a paragraph if no other block found
        ast.Para: [None, None],
        # match a markdown # Header
        ast.Header: [r"^#{1,6} (?P<contents>.*$)", None],
        # match *italic* text
        ast.Emph: [r"(\*{1})(?P<contents>[^*\n]+?)(\*{1})", None],
        ast.Strong: [r"(\*{2})(?P<contents>\*?[^\n]+?\*?)(\*{2})", None],
        ast.Code: [r"(^|[^`])(`{1,2})(?P<contents>[^\n]+?)\2(?!`)", None],
    }
    return declared_blocks
