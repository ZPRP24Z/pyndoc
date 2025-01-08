import pyndoc.ast.blocks as ast
import pyndoc.ast.basic_blocks as ast_base
import pyndoc.readers.gfm.blocks as gfm

INLINE = True

# How do composite blocks start?
declared_tokens = {
    gfm.Header: (r"^(?:\n)*(?P<h>#{1,6}) ", not INLINE),
    ast.Strong: (r"\*\*", INLINE),
    gfm.BulletList: (r"^(?P<s>[\t\s]*)[\*\+\-] ", not INLINE),
    gfm.OrderedList: (r"^(?P<s>[\t\s]*)(?P<num>\d{1,9})(?P<sep>[\.|)]) ", not INLINE),
    gfm.Emph: (r"\*[^*]{1}", INLINE),
    gfm.CodeHelper: (r"^`{1,2}[^`]", INLINE),
    gfm.CodeBlockHelper: (r"^```(?P<lang>.*)\n", not INLINE),
    gfm.Table: (r"^\|", not INLINE),
    gfm.Cell: (r"^(?P<c> *\| *)[^\n]+", not INLINE),
    # The atom wrapper does not need to be declared here
}

# How do composite blocks end?
declared_ends = {
    gfm.Header: r"\n",
    gfm.CodeBlockHelper: r"\n```",
    ast.Strong: r"\*\*",
    gfm.Emph: r"\*[^*]{1}",
    ast.Para: r"\n\n",
    gfm.BulletList: r"\n\n",
    gfm.OrderedList: r"\n\n",
    ast_base.ASTCompositeBlock: r"\n",  # DEFAULT
    gfm.Table: r"^[^\|]",
    gfm.Row: r"\|\n",
    gfm.Cell: r" *\|",
    gfm.TableHead: r"\n?",
    gfm.TableBody: r"\n",
}

# what block to use if an atom block is found without context? (not within other blocks)
atom_wrapper = ast.Para

# how should we define atomic patterns? (blocks not containing other blocks)
declared_atomic_patterns = {
    gfm.Space: r"^[ ]+$",
    ast.Str: r"^[^\s\n]+$",
    gfm.SoftBreak: r"^\n",
}

atoms_content = {
    gfm.Space: False,
    ast.Str: True,
    gfm.SoftBreak: False,
    ast.Code: True,
    ast.CodeBlock: True,
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
        block.override_match_pattern(atomic_patterns_dict[block])

    for block in atomic_patterns_dict.keys():
        block.override_has_content(atoms_content[block])
