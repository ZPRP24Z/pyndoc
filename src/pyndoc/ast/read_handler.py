import pyndoc.ast.helpers as helpers
from typing_extensions import Unpack
import re


class CompositeReadHandler:
    """
    Class that is meant as a handler for reading logic for an AST Composite child.
    methods implemented here are defaults for
    """

    start_pattern = ""  #: ``str``, The start pattern of a block, defaults to an empty string
    end_pattern = ""  #: ``str``, The end pattern of a block, defaults to an empty string
    inline = False  #: ``bool``, decides if the block is an inline

    def process_read(self, **_: Unpack[helpers.ProcessParams]) -> None:
        """Process additional keyword arguments after block initialization.
        Not used here, the function is meant to be used inside of
        blocks inherited from basic AST blocks. Otherwise no processing will be done
        """
        pass

    @classmethod
    def start(cls, **kwargs: Unpack[helpers.StartParams]) -> tuple[re.Match | None, str]:
        r"""Check if a block has started.
        Returns a match if matched, otherwise None

        :param \**kwargs:
            See below
        :Keyword Arguments:
            * *token* (``str``) -- the current token
        """
        token = kwargs["token"]
        match = re.search(cls.start_pattern, token)
        token = token[: match.start()] if match else token
        return (match, token)

    @classmethod
    def end(cls, **kwargs: Unpack[helpers.EndParams]) -> tuple[re.Match | None, str]:
        r"""Check if a block has ended.
        Returns a match if matched, otherwise None

        :param \**kwargs:
            See below

        :Keyword Arguments:
            * token (``str``) -- string representing current token to be matched against pattern
        """
        token = kwargs["token"]
        match = re.search(cls.end_pattern, token)
        token = token[match.end() :] if match else token
        return (match, token)

    @classmethod
    def override_start(cls, pattern: str) -> None:
        """Override the start pattern of an ASTCompositeBlock

        :param pattern:
            The new pattern of a block
        :type pattern: str
        """
        cls.start_pattern = pattern

    @classmethod
    def override_end(cls, pattern: str) -> None:
        """Override the end pattern of an ASTCompositeBlock

        :param pattern:
            The new pattern of a block
        :type pattern: str
        """
        cls.end_pattern = pattern

    @classmethod
    def override_inline(cls, value: bool) -> None:
        """Override the inline boolean value of an ASTBlock

        :param value:
            The new value of the attribute
        :type value: bool
        """
        cls.inline = value

    @classmethod
    def is_inline(cls) -> bool:
        """Check if a given block type is inline, default: False"""
        return cls.inline

    @classmethod
    def handle_premature_closure(cls, **kwargs: Unpack[helpers.EndParams]) -> str:
        """Used when when the file has ended, but context has not been closed
        Potentially modify recieved token end return it

        :param token:
            The current token to be modified
        :type token: str
        """
        token = kwargs["token"]
        return token


class AtomReadHandler:
    pattern = ""
    start_pattern = ""
    has_content = True

    @classmethod
    def match_pattern(cls, **kwargs: Unpack[helpers.AtomMatchParams]) -> tuple[re.Match | None, str]:
        r"""Check if the block matches a given token.
        Returns a regex match (or None if match failed)

        :param \**kwargs:
            See below

        :Keyword Arguments:
            * text (``str``) -- the token to be matched against the pattern attribute
        """
        text = kwargs["text"]
        match = re.search(cls.pattern, text)
        if match and len(text) != match.end():
            return (None, text)
        return (match, text)

    @classmethod
    def override_match_pattern(cls, pattern: str) -> None:
        """
        Set the match pattern to a new value

        :param pattern:
            The new pattern to be set
        :type pattern: str
        """
        cls.pattern = pattern

    @classmethod
    def block_has_content(cls) -> bool:
        """Check if a block can have contents

        :return: True if the block can have contents
        :rtype: bool
        """
        return cls.has_content

    @classmethod
    def override_has_content(cls, value: bool) -> None:
        """Change if a block can have contents, usually
        set at runstart

        :param value:
            If the block can have contents
        :type value: bool
        """
        cls.has_content = value
