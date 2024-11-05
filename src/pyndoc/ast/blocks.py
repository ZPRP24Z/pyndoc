from dataclasses import dataclass


@dataclass
class AstBlock:
    name: str
    contents: list = None


class Str(AstBlock):
    """
    special AST block representing strings
    """
    def __init__(self, contents: str = None):
        super().__init__("Str", contents)


class Space(AstBlock):
    """
    AST block representing a space character
    Mostly unused, to be inserted before multiple spaces
    """
    def __init__(self):
        super().__init__("Space")


class Header(AstBlock):
    """
    AST block representing a heading
    """
    def __init__(self, level: int, contents: str):
        super().__init__("Header", [level, [Str(contents)]])


class Para(AstBlock):
    """
    AST block representing a paragraph.
    It is recommended to make this block None-started and ended, resulting in unmatched text being converted to paragraphs
    """
    def __init__(self, contents: str):
        super().__init__("Para", [Str(contents)])


class Italic(AstBlock):
    """
    Basic Italic AST block
    """
    def __init__(self, contents: str):
        super().__init__("Italic", [Str(contents)])


class Bold(AstBlock):
    """
    Basic Bold AST block
    """
    def __init__(self, contents: str):
        super().__init__("Bold", [Str(contents)])
