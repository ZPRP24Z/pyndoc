from typing import Any
import re


class ASTBlock:
    def __init__(self, name: str):
        self.name = name


class ASTAtomBlock(ASTBlock):
    pattern = ""
    has_content = False

    def __init__(self, name: str, contents: str = ""):
        self.content = contents
        super().__init__(name)

    def __eq__(self, other):
        if isinstance(other, ASTAtomBlock):
            return self.name == other.name and self.content == other.content
        return NotImplemented

    def __repr__(self):
        return f'{self.name}("{self.content}")'

    @classmethod
    def match_pattern(cls, text: str) -> re.Match | None:
        return re.search(cls.pattern, text)

    @classmethod
    def override_match_pattern(cls, pattern: str) -> None:
        cls.pattern = pattern

    @classmethod
    def block_has_content(cls) -> Any:
        return cls.has_content

    @classmethod
    def override_has_content(cls, value: Any) -> None:
        cls.has_content = value


class ASTCompositeContents:
    def __init__(self, metadata: list, contents: list[ASTBlock]):
        self.metadata = metadata
        self.contents = contents


class ASTCompositeBlock(ASTBlock):
    start_pattern = ""
    end_pattern = ""

    def __init__(self, name: str, metadata=None, contents=None):
        metadata = metadata if metadata else []
        contents = contents if contents else []
        self.contents = ASTCompositeContents(metadata, contents)
        super().__init__(name)

    def insert(self, block: ASTBlock) -> None:
        self.contents.contents.append(block)

    @classmethod
    def start(cls, **kwargs) -> tuple[re.Match | None, str]:
        if "token" not in kwargs:
            return None, ""
        token = kwargs["token"]
        match = re.search(cls.start_pattern, token)
        token = token[: match.start()] if match else token
        return (match, token)

    @classmethod
    def end(cls, **kwargs) -> re.Match | None:
        if "token" not in kwargs:
            return None
        token = kwargs["token"]
        return re.search(cls.end_pattern, token)

    @classmethod
    def override_start(cls, pattern: str) -> None:
        cls.start_pattern = pattern

    @classmethod
    def override_end(cls, pattern: str):
        cls.end_pattern = pattern


class Space(ASTAtomBlock):
    """
    AST Atom block representing whitespace
    """

    def __init__(self):
        super().__init__("Space")


class Str(ASTAtomBlock):
    """
    special AST block representing string without whitespace characters
    """

    def __init__(self, contents: str = ""):
        super().__init__("Str", contents)


class Header(ASTCompositeBlock):
    """
    AST block representing a heading
    """

    def __init__(self, **kwargs):
        if "level" not in kwargs:
            level = 1
        else:
            level = kwargs["level"]
        super().__init__("Header", [level])


class Para(ASTCompositeBlock):
    """
    AST block representing a paragraph.
    """

    def __init__(self, **_):
        super().__init__("Para")


class Emph(ASTCompositeBlock):
    """
    Basic Italic AST block
    """

    def __init__(self, **_):
        super().__init__("Emph")


class Strong(ASTCompositeBlock):
    """
    Basic Bold AST block
    """

    def __init__(self, **_):
        super().__init__("Strong")


class Code(ASTCompositeBlock):
    def __init__(self, **_):
        super().__init__("Code")


# TODO change function name to more informative, probalby refactor
def decompose_text(text: str) -> list[ASTBlock]:
    char_chains = text.rstrip().split()
    blocks = []

    for idx, char_chain in enumerate(char_chains):
        blocks.append(Str(char_chain))

        if idx != len(char_chains):
            blocks.append(Space())

    return blocks
