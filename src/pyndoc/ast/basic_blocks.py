import re


class ASTBlock:
    """
    Definition of a base AST block containing just a name
    """

    def __init__(self, name: str) -> None:
        self.name = name


class ASTAtomBlock(ASTBlock):
    """
    Definition of an AST Atom Block.
    An AST Atom block is a block that cannot hold any other blocks inside of it.
    Attributes:
        * pattern -- regex pattern defining the block (default: "")
        * has_content -- boolean describing if the block has any content (defualt: False)
    """

    pattern = ""
    has_content = False

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

    def __repr__(self) -> str:
        return f'{self.name}("{self.contents}")'

    @classmethod
    def match_pattern(cls, text: str) -> re.Match | None:
        """
        Check if the block matches a given token.
        Returns a regex match (or None if match failed)
        Keyword arguments:
            * text -- the token to be matched against the pattern attribute
        """
        match = re.search(cls.pattern, text)
        if match and len(text) != match.end():
            return None
        return match

    @classmethod
    def override_match_pattern(cls, pattern: str) -> None:
        """
        Set the match pattern to a new value
        Keyword arguments:
            * pattern -- the new pattern to be set
        """
        cls.pattern = pattern

    @classmethod
    def block_has_content(cls) -> bool:
        """
        Check if a block can have contents
        """
        return cls.has_content

    @classmethod
    def override_has_content(cls, value: bool) -> None:
        """
        Change if a block can have contents, usually
        set at runstart
        """
        cls.has_content = value


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


class ASTCompositeBlock(ASTBlock):
    """
    The definition of an AST Composite block.
    This block can hold both atom, and other composite blocks inside of it.
    Attributes:
        * start_pattern -- string representing the block's start
        * end_pattern -- string representing the block's end
        * inline -- flag showing if the block is an inline block
    """

    start_pattern = ""
    end_pattern = ""
    inline = False

    def __init__(
        self, name: str, metadata: list | None = None, contents: list | None = None
    ) -> None:
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

    def process_read(self, **_: None) -> None:
        """
        Process additional keyword arguments after block initialization.
        Not used here, the function is meant to be used inside of
        blocks inherited from basic AST blocks. Otherwise no processing will be done
        """
        pass

    @classmethod
    def start(cls, **kwargs: str) -> tuple[re.Match | None, str]:
        """
        Check if a block has started.
        Returns a match if matched, otherwise None
        Expected keyword arguments:
            * token -- string representing current token to be matched against pattern
        """
        if "token" not in kwargs:
            return None, ""
        token = kwargs["token"]
        match = re.search(cls.start_pattern, token)
        token = token[: match.start()] if match else token
        return (match, token)

    @classmethod
    def end(cls, **kwargs: str) -> re.Match | None:
        """
        Check if a block has ended.
        Returns a match if matched, otherwise None
        Expected keyword arguments:
            * token -- string representing current token to be matched against pattern
        """
        if "token" not in kwargs:
            return None, ""
        token = kwargs["token"]
        match = re.search(cls.end_pattern, token)
        token = token[match.end() :] if match else token
        return (match, token)

    @classmethod
    def override_start(cls, pattern: str) -> None:
        """
        Override the start pattern of an ASTCompositeBlock
        """
        cls.start_pattern = pattern

    @classmethod
    def override_end(cls, pattern: str) -> None:
        """
        Override the end pattern of an ASTCompositeBlock
        """
        cls.end_pattern = pattern

    @classmethod
    def override_inline(cls, value: bool) -> None:
        """
        Override the inline boolean value of an ASTBlock
        """
        cls.inline = value

    @classmethod
    def is_inline(cls) -> bool:
        """
        Check if a given block type is inline, default: False
        """
        return cls.inline

    @classmethod
    def handle_premature_closure(cls, token: str) -> str:
        """
        Used when when the file has ended, but context has not been closed
        Potentially modify recieved token end return it
        """
        return token
