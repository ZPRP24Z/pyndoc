import pyndoc.ast.blocks as ast
import pyndoc.ast.gfm.blocks as gfm


def declare():
    """
    Function declaring the regular expressions for each block and instructions for conversion to AST.
    The "contents" group will be used as the block's contents
    """
    declared_blocks = {
        r"(?m)^(?P<h>#{1,6}) (?P<contents>.*$)": gfm.Header,
        r"(\*{2})(?P<contents>(?P<a>\*?)[^\n]+(?P=a))(\*{2})": ast.Strong,
        r"(\*{1})(?P<contents>[^*\n]+?)(\*{1})": ast.Emph,
        r"(^|[^`])(`{1,2})(?P<contents>[^\n]+?)\2(?!`)": ast.Code
    }
    return declared_blocks
