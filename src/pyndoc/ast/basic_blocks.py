from abc import ABC
from pyndoc.ast.read_handler import CompositeReadHandler, AtomReadHandler


class ASTBlock(ABC):
    """Definition of a base AST block"""

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __str__(self) -> str:
        return f"{self.__class__.__name__}"


class ASTAtomBlock(ASTBlock, AtomReadHandler):
    """Definition of an AST Atom Block.
    An AST Atom block is a block that cannot hold any other blocks inside of it.

    :param contents:
        the contents of the Atom Block, empty by default
    :type contents: ``str``, optional
    """

    def __init__(self, contents: str = "") -> None:
        """Constructor method"""
        self.contents = contents
        self.metadata = []

    def __eq__(self, other: object) -> bool:
        if isinstance(other, ASTAtomBlock):
            return self.__class__.__name__ == other.__class__.__name__ and self.contents == other.contents
        return NotImplemented

    def __str__(self) -> str:
        return self.__class__.__name__ + (f"({self.contents!r})" if self.__class__.has_content else "")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(contents={self.contents!r})"


class ASTCompositeContents:
    """The representation of a composite block's contents

    :param metadata: The block's special metadata
    :type metadata: ``list``
    :param contents: The contents of the class
    :type contents: ``list[ASTBlock]``
    """

    def __init__(self, metadata: list, contents: list[ASTBlock]) -> None:
        self.metadata = metadata
        self.contents = contents


class ASTCompositeBlock(ASTBlock, CompositeReadHandler):
    """The definition of an AST Composite block.
    This block can hold both atom, and other composite blocks inside of it.

    :param metadata: List of block's metadata
    :type metadata: ``list | None``
    :param contents: A list of other ASTBlocks representing the block's contents, defaults to a None object
    :type contents: ``list | None``
    """

    def __init__(self, metadata: list | None = None, contents: list | None = None) -> None:
        metadata = metadata if metadata else []
        contents = contents if contents else []
        self.contents = ASTCompositeContents(metadata, contents)

    def insert(self, block: ASTBlock) -> None:
        """Insert another AST Block into this one
        :param block: the other block object
        :type block: ASTBlock
        """
        self.contents.contents.append(block)

    def __str__(self) -> str:
        result_str = f"{self.__class__.__name__}: [\n  "

        if self.contents.metadata:
            result_str += f"Metadata: {[element.__str__() for element in self.contents.metadata]}\n  "

        contents_str = "\n".join(
            ["    " + str(block).replace("\n", "\n    ") + "," for block in self.contents.contents]
        )
        result_str += (f"Contents: \n  [\n{contents_str}\n  ]," if contents_str else "Contents: None") + "\n]"

        return result_str

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}()" f"metadata={self.contents.metadata!r}, contents={self.contents.contents!r})"
        )
