from pyndoc.ast.basic_blocks import ASTAtomBlock, ASTCompositeBlock


class Space(ASTAtomBlock):
    """AST Atom block representing whitespace"""

    def __init__(self) -> None:
        super().__init__("Space")


class Str(ASTAtomBlock):
    """special AST block representing string without whitespace characters"""

    def __init__(self, contents: str = "") -> None:
        super().__init__("Str", contents)

    def __str__(self) -> str:
        return super().__str__() + f' "{self.contents}"'


class SoftBreak(ASTAtomBlock):
    def __init__(self) -> None:
        super().__init__("SoftBreak")


class Header(ASTCompositeBlock):
    """AST block representing a heading"""

    def __init__(self) -> None:
        super().__init__("Header")


class Para(ASTCompositeBlock):
    """AST block representing a paragraph."""

    def __init__(self) -> None:
        super().__init__("Para")


class Emph(ASTCompositeBlock):
    """Basic Italic AST block"""

    def __init__(self) -> None:
        super().__init__("Emph")


class Strong(ASTCompositeBlock):
    """Basic Bold AST block"""

    def __init__(self) -> None:
        super().__init__("Strong")


class Code(ASTCompositeBlock):
    """Basic Code AST block"""

    def __init__(self) -> None:
        super().__init__("Code")


class BulletList(ASTCompositeBlock):
    def __init__(self) -> None:
        super().__init__("BulletList")


class OrderedList(ASTCompositeBlock):
    """Ordered List AST block"""

    def __init__(self) -> None:
        super().__init__("OrderedList")


class Plain(ASTCompositeBlock):
    def __init__(self) -> None:
        super().__init__("Plain")


class Table(ASTCompositeBlock):
    """Table AST block"""

    def __init__(self) -> None:
        super().__init__("Table")


class TableHead(ASTCompositeBlock):
    """Table Head AST block"""

    def __init__(self) -> None:
        super().__init__("TableHead")


class TableBody(ASTCompositeBlock):
    """Table Body AST block"""

    def __init__(self) -> None:
        super().__init__("TableBody")


class Row(ASTCompositeBlock):
    """Table Row AST block"""

    def __init__(self) -> None:
        super().__init__("Row")


class Cell(ASTCompositeBlock):
    """Table Cell AST block"""

    def __init__(self) -> None:
        super().__init__("Cell")


class CodeBlock(ASTAtomBlock):
    """Code block AST block"""

    def __init__(self) -> None:
        super().__init__("CodeBlock")
