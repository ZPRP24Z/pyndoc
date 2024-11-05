from pyndoc.ast.blocks import AstBlock, Str


class Header(AstBlock):
    def __init__(self, level: int, contents: str):
        super().__init__("Header", [level, [Str(contents)]])


class Para(AstBlock):
    def __init__(self, contents: str):
        super().__init__("Para", [Str(contents)])


class Italic(AstBlock):
    def __init__(self, contents: str):
        super().__init__("Italic", [Str(contents)])

class Bold(AstBlock):
    def __init__(self, contents: str):
        super().__init__("Bold", [Str(contents)])
