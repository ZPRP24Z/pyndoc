class ASTBlock:
    def __init__(self, name: str):
        self.name = name


class ASTAtomBlock(ASTBlock):
    def __init__(self, name: str, content: str):
        self.content = content
        super().__init__(name)

    def __eq__(self, other):
        if isinstance(other, ASTAtomBlock):
            return self.name == other.name and self.content == other.content
        return NotImplemented


class ASTCompositeBlock(ASTBlock):
    def __init__(self, name: str, contents: list[ASTBlock]):
        self.contents = contents
        super().__init__(name)


class Space(ASTAtomBlock):
    """
    AST Atom block representing whitespace
    """

    def __init__(self):
        super().__init__("Space", " ")


class Str(ASTAtomBlock):
    """
    special AST block representing string without whitespace characters
    """

    def __init__(self, content: str = None):
        super().__init__("Str", content)


class Header(ASTCompositeBlock):
    """
    AST block representing a heading
    """

    def __init__(self, level: int, contents: str):
        super().__init__("Header", [level, [Str(contents)]])


class Para(ASTCompositeBlock):
    """
    AST block representing a paragraph.
    It is recommended to make this block None-started and ended, resulting in unmatched text being converted to paragraphs
    """

    def __init__(self, contents: str):
        super().__init__("Para", [Str(contents)])


class Emph(ASTCompositeBlock):
    """
    Basic Italic AST block
    """

    def __init__(self, contents: str):
        super().__init__("Emph", [Str(contents)])


class Strong(ASTCompositeBlock):
    """
    Basic Bold AST block
    """

    def __init__(self, contents: str):
        super().__init__("Strong", [Str(contents)])


class Code(ASTCompositeBlock):
    def __init__(self, contents: str):
        super().__init__("Code", [Str(contents)])


# TODO change function name to more informative, probalby refactor
def decompose_text(text: str) -> list[ASTBlock]:
    char_chains = text.rstrip().split()
    blocks = []

    for idx, char_chain in enumerate(char_chains):
        blocks.append(Str(char_chain))

        if idx != len(char_chains):
            blocks.append(Space())

    return blocks
