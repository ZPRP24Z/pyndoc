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
        gfm.Emph: r"\*[^*]{1}",
        ast.Code: r"`",
    }
    return declared_tokens


def ends():
    declared_ends = {
        ast.Strong: r"\*\*",
        gfm.Emph: r"\*",
        ast.ASTCompositeBlock: r"(\n)$",  # DEFAULT
    }
    return declared_ends


def atomic_patterns():
    declared_atomic_patterns = {
        ast.Str: (r"^[^\s\n]+$", True),
        ast.Space: (r"^[ ]+$", False)
    }
    return declared_atomic_patterns


def assign_patterns():
    start_dict = starts()
    end_dict = ends()
    atomic_patterns_dict = atomic_patterns()

    for block in end_dict.keys():
        block.override_end(end_dict[block])

    for block in start_dict.keys():
        block.override_start(start_dict[block])

    for block in atomic_patterns_dict.keys():
        block.override_match_pattern(atomic_patterns_dict[block][0])

    for block in atomic_patterns_dict.keys():
        block.override_has_content(atomic_patterns_dict[block][1])
