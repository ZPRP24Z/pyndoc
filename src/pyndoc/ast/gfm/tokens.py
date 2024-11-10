import pyndoc.ast.blocks as ast
import pyndoc.ast.gfm.parse_instructions as gfm


def starts():
    """
    Function declaring the regular expressions for each block and instructions for conversion to AST.
    The "contents" group will be used as the block's contents
    """
    declared_tokens = {
        gfm.Header: r"^(?P<h>#{1,6}) ",
        ast.Strong: r"\*\*",
        ast.Emph: r"\*",
        ast.Code: r"`",
    }
    return declared_tokens


def ends():
    declared_ends = {
        ast.Strong: r"\*\*",
        ast.Emph: r"\*",
        ast.ASTCompositeBlock: r"\n",  # DEFAULT
    }
    return declared_ends


def assign_patterns():
    start_dict = starts()
    end_dict = ends()

    for block in end_dict.keys():
        block.override_end(end_dict[block])

    for block in start_dict.keys():
        block.override_start(start_dict[block])
