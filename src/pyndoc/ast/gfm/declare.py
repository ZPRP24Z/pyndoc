import pyndoc.ast.blocks as ast


def declare_gfm():
    declared_blocks = {
        ast.Para: [None, None],
        ast.Header: ["#{1,6} .*", None],
        ast.Italic: ["(?:^|\s|(?:^|\s)\*\*)\*([^*]+)\*(?:\s|$|\*\*(?:$|\s))", None],
        ast.Bold: ["(?:^|\s|(?:^|\s)\*)\*\*([^*]+)\*\*(?:\s|$|\*(?:$|\s))", None]
    }
    return declared_blocks
