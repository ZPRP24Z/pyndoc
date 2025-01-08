from pyndoc.ast.basic_blocks import ASTAtomBlock, ASTCompositeBlock


class Space(ASTAtomBlock):
    """AST Atom block representing whitespace"""

    def __init__(self) -> None:
        super().__init__()


class Str(ASTAtomBlock):
    """special AST block representing string without whitespace characters"""

    def __init__(self, contents: str = "") -> None:
        super().__init__(contents)

    def __str__(self) -> str:
        return super().__str__() + f' "{self.contents}"'


class SoftBreak(ASTAtomBlock):
    def __init__(self) -> None:
        super().__init__()


class Header(ASTCompositeBlock):
    """AST block representing a heading"""

    def __init__(self) -> None:
        super().__init__()


class Para(ASTCompositeBlock):
    """AST block representing a paragraph."""

    def __init__(self) -> None:
        super().__init__()


class Emph(ASTCompositeBlock):
    """Basic Italic AST block"""

    def __init__(self) -> None:
        super().__init__()


class Strong(ASTCompositeBlock):
    """Basic Bold AST block"""

    def __init__(self) -> None:
        super().__init__()


class Code(ASTAtomBlock):
    """Basic Code AST block"""

    def __init__(self) -> None:
        super().__init__()


class BulletList(ASTCompositeBlock):
    def __init__(self) -> None:
        super().__init__()


class OrderedList(ASTCompositeBlock):
    """Ordered List AST block"""

    def __init__(self) -> None:
        super().__init__()


class Plain(ASTCompositeBlock):
    def __init__(self) -> None:
        super().__init__()


class Table(ASTCompositeBlock):
    """Table AST block"""

    def __init__(self) -> None:
        super().__init__()


class TableHead(ASTCompositeBlock):
    """Table Head AST block"""

    def __init__(self) -> None:
        super().__init__()


class TableBody(ASTCompositeBlock):
    """Table Body AST block"""

    def __init__(self) -> None:
        super().__init__()


class Row(ASTCompositeBlock):
    """Table Row AST block"""

    def __init__(self) -> None:
        super().__init__()


class Cell(ASTCompositeBlock):
    """Table Cell AST block"""

    def __init__(self) -> None:
        super().__init__()


class CodeBlock(ASTAtomBlock):
    """Code block AST block"""

    def __init__(self) -> None:
        super().__init__()
