import pyndoc.ast.blocks as ast
import pyndoc.ast.basic_blocks as ast_base
import pyndoc.readers.gfm.parse_instructions as gfm

INLINE = True

# How do composite blocks start?
declared_tokens = {
    gfm.Header: (r"^(?P<h>#{1,6}) ", not INLINE),
    ast.Strong: (r"\*\*", INLINE),
    gfm.BulletList: (r"^(?P<s>[\t|\s]*)[\*|\+|\-] ", not INLINE),
    gfm.Emph: (r"\*[^*]{1}", INLINE),
    ast.Code: (r"`", INLINE),
    # The atom wrapper does not need to be declared here
}


# How do composite blocks end?
declared_ends = {
    ast.Strong: r"\*\*",
    gfm.Emph: r"\*[^*]{1}",
    ast.Para: r"\n\n",
    gfm.BulletList: r"non-ending-placeholder",
    ast_base.ASTCompositeBlock: r"(\n)$",  # DEFAULT
}


# what block to use if an atom block is found without context? (not within other blocks)
atom_wrapper = ast.Para

# how should we define atomic patterns? (blocks not containing other blocks)
declared_atomic_patterns = {
    gfm.Space: (r"^[ ]+$", False),
    ast.Str: (r"^[^\s\n]+$", True),
    ast.SoftBreak: (r"^\n(?!\n)", False),
}


def assign_patterns() -> None:
    start_dict = declared_tokens
    end_dict = declared_ends
    atomic_patterns_dict = declared_atomic_patterns

    for block in end_dict.keys():
        block.override_end(end_dict[block])

    for block in start_dict.keys():
        block.override_start(start_dict[block][0])
        if start_dict[block][1]:
            block.override_inline(True)

    for block in atomic_patterns_dict.keys():
        block.override_match_pattern(atomic_patterns_dict[block][0])

    for block in atomic_patterns_dict.keys():
        block.override_has_content(atomic_patterns_dict[block][1])
