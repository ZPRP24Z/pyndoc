import pyndoc.ast.helpers as helpers
from typing_extensions import Unpack
import re


class CompositeReadHandler:
    """
    Class that is meant as a handler for reading logic for an AST Composite child.
    methods implemented here are defaults for 
    """
    start_pattern = ""
    end_pattern = ""
    inline = False

    def process_read(self, **_: Unpack[helpers.ProcessParams]) -> None:
        """
        Process additional keyword arguments after block initialization.
        Not used here, the function is meant to be used inside of
        blocks inherited from basic AST blocks. Otherwise no processing will be done
        """
        pass

    @classmethod
    def start(cls, **kwargs: Unpack[helpers.StartParams]) -> tuple[re.Match | None, str]:
        """
        Check if a block has started.
        Returns a match if matched, otherwise None
        Expected keyword arguments:
            * token -- string representing current token to be matched against pattern
        """
        token = kwargs["token"]
        match = re.search(cls.start_pattern, token)
        token = token[: match.start()] if match else token
        return (match, token)

    @classmethod
    def end(cls, **kwargs: Unpack[helpers.EndParams]) -> tuple[re.Match | None, str]:
        """
        Check if a block has ended.
        Returns a match if matched, otherwise None
        Expected keyword arguments:
            * token -- string representing current token to be matched against pattern
        """
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


class AtomReadHandler:
    pattern = ""
    has_content = False

    @classmethod
    def match_pattern(cls, **kwargs: Unpack[helpers.AtomMatchParams]) -> re.Match | None:
        """
        Check if the block matches a given token.
        Returns a regex match (or None if match failed)
        Keyword arguments:
            * text -- the token to be matched against the pattern attribute
        """
        text = kwargs["text"]
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
