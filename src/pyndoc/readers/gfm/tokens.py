import pyndoc.ast.blocks as ast
import pyndoc.readers.gfm.parse_instructions as gfm

declared_tokens = {
        gfm.Header: r"^(?P<h>#{1,6}) ",
        ast.Strong: r"\*\*",
        gfm.Emph: r"\*[^*]{1}",
        ast.Code: r"`",
    }


declared_ends = {
        ast.Strong: r"\*\*",
        gfm.Emph: r"\*",
        ast.ASTCompositeBlock: r"(\n)$",  # DEFAULT
    }


declared_atomic_patterns = {
        ast.Str: (r"^[^\s\n]+$", True),
        ast.Space: (r"^[ ]+$", False),
    }


def assign_patterns():
    start_dict = declared_tokens
    end_dict = declared_ends
    atomic_patterns_dict = declared_atomic_patterns

    for block in end_dict.keys():
        block.override_end(end_dict[block])

    for block in start_dict.keys():
        block.override_start(start_dict[block])

    for block in atomic_patterns_dict.keys():
        block.override_match_pattern(atomic_patterns_dict[block][0])

    for block in atomic_patterns_dict.keys():
        block.override_has_content(atomic_patterns_dict[block][1])
