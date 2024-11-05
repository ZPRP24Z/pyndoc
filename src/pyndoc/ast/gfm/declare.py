import pyndoc.ast.gfm.blocks as gfm


def declare_gfm():
    declared_blocks = {
        gfm.Para: [None, None],
        gfm.Header: ["#{1,6} ", None],
        gfm.Italic: [" \*[^*]", "* "],
        gfm.Bold: [" **", "** "]
    }
    return declared_blocks
