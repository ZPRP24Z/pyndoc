from pyndoc.ast.read_handler import CompositeReadHandler, AtomReadHandler


class ASTBlock:
    """
    Definition of a base AST block containing just a name
    """

    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name!r})"

    def __str__(self) -> str:
        return f"{self.name}"


class ASTAtomBlock(ASTBlock, AtomReadHandler):
    """
    Definition of an AST Atom Block.
    An AST Atom block is a block that cannot hold any other blocks inside of it.
    """

    def __init__(self, name: str, contents: str = "") -> None:
        """
        Keyword arguments:
            * name - the name of the block
            * contents - the block's contents if it has any
        """
        self.contents = contents
        super().__init__(name)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, ASTAtomBlock):
            return self.name == other.name and self.contents == other.contents
        return NotImplemented

    def __str__(self) -> str:
        return f"{self.__class__.__name__}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name!r}, contents={self.contents!r})"


class ASTCompositeContents:
    """
    The representation of a composite block's contents
    """

    def __init__(self, metadata: list, contents: list[ASTBlock]) -> None:
        """
        Keyword arguments:
            * metadata -- block's metadata (level for headers, etc.)
            * contents -- a list of other AST blocks
        """
        self.metadata = metadata
        self.contents = contents


class ASTCompositeBlock(ASTBlock, CompositeReadHandler):
    """
    The definition of an AST Composite block.
    This block can hold both atom, and other composite blocks inside of it.
    """

    def __init__(self, name: str, metadata: list | None = None, contents: list | None = None) -> None:
        """
        Keyword arguments:
            * name -- the name of the block
            * metadata -- list of block's metadata
            * contents -- a list of other ASTBlocks representing the block's content
        """
        metadata = metadata if metadata else []
        contents = contents if contents else []
        self.contents = ASTCompositeContents(metadata, contents)
        super().__init__(name)

    def insert(self, block: ASTBlock) -> None:
        """
        Insert another AST Block into this one
        Keyword arguments:
            * block -- the other block object
        """
        self.contents.contents.append(block)

    def __str__(self) -> str:
        result_str = f"{self.__class__.__name__}: [\n  "

        if self.contents.metadata:
            result_str += f"Metadata: {self.contents.metadata}\n  "

        contents_str = "\n".join(
            ["    " + str(block).replace("\n", "\n    ") + "," for block in self.contents.contents]
        )
        result_str += (f"Contents: \n  [\n{contents_str}\n  ]," if contents_str else "Contents: None") + "\n]"

        return result_str

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(name={self.name!r}, "
            f"metadata={self.contents.metadata!r}, contents={self.contents.contents!r})"
        )
