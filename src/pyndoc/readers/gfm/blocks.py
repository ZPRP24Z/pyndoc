import re
from typing_extensions import Unpack
from abc import ABC

import pyndoc.ast.blocks as ast
import pyndoc.ast.helpers as ast_helpers


class Space(ast.Space):
    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def match_pattern(cls, **kwargs: Unpack[ast_helpers.AtomMatchParams]) -> tuple[re.Match | None, str]:
        context = kwargs["context"]
        text = kwargs["text"]
        if not context or context[-1].name in ("BulletList", "OrderedList"):
            return (None, text)

        match = re.search(cls.pattern, text)
        if match and len(text) != match.end():
            return (None, text)
        return (match, text)


class SoftBreak(ast.SoftBreak):

    @classmethod
    def match_pattern(cls, **kwargs: Unpack[ast_helpers.AtomMatchParams]) -> tuple[re.Match | None, str]:
        context = kwargs["context"]
        text = kwargs["text"]

        if not context or context[-1].name in ("BulletList", "OrderedList"):
            return (None, text)

        match = re.search(cls.pattern, text)
        if match and len(text) != match.end():
            return (None, text)

        if match and not context:
            return (match, "")
        return (match, text)


class Header(ast.Header):
    def __init__(self) -> None:
        super().__init__()

    def process_read(self, **kwargs: Unpack[ast_helpers.ProcessParams]) -> None:
        match = kwargs["match"]
        level = len(match.group("h"))
        self.contents.metadata = [level]


class Emph(ast.Emph):
    def __init__(self, **_: None) -> None:
        super().__init__()

    @classmethod
    def start(cls, **kwargs: Unpack[ast_helpers.StartParams]) -> tuple[re.Match | None, str]:
        token = kwargs["token"]
        match = re.search(cls.start_pattern, token)
        token = token[-1:] if match else token
        return (match, token)

    @classmethod
    def end(cls, **kwargs: Unpack[ast_helpers.EndParams]) -> tuple[re.Match | None, str]:
        token = kwargs["token"]
        context = kwargs["context"]

        if context[-2] and context[-2].name == "Strong":
            match = re.search(cls.end_pattern[:2], token)
            token = token[match.end() :] if match else token
        else:
            match = re.search(cls.end_pattern[:], token)
            token = token[match.end() - 1 :] if match else token
        return (match, token)

    @classmethod
    def handle_premature_closure(cls, token: str) -> str:
        return token[:-1] if token[-1] == "*" else token


class _GFMList(ABC):
    """
    Base class for gfm lists e.g. bullet list or ordered list
    Class made to avoid code repetition, it should not be used on its own
    """

    @staticmethod
    def add_plain(context: list) -> None:
        plain = ast.Plain()
        context.append(plain)

    @classmethod
    def start(cls, **kwargs: Unpack[ast_helpers.StartParams]) -> tuple[re.Match | None, str]:
        token = kwargs["token"]
        context = kwargs["context"]
        match = re.search(cls.start_pattern, token)

        if match:
            bigger_indent = False
            if context and issubclass(context[-1].__class__, _GFMList):
                match_indent = len(match.group("s"))
                context_indent = context[-1].contents.metadata[0]
                bigger_indent = match_indent > context_indent
                if match_indent == context_indent:
                    cls.add_plain(context)
                    return (None, "")
            if not context or bigger_indent:
                token = token[: match.start()]
            else:
                match = None

        return (match, token)

    @classmethod
    def end(cls, **kwargs: Unpack[ast_helpers.EndParams]) -> tuple[re.Match | None, str]:
        """
        List end check.
        if a list with the same or larger indent started, do not end,
        otherwise - end
        """
        token = kwargs["token"]
        context = kwargs["context"]

        if len(context) >= 2 and (match := re.search(context[-2].__class__.start_pattern, token)) is not None:
            token_indent = len(match.group("s"))
            block_indent = context[-1].contents.metadata[0]
            if token_indent < block_indent:
                return (match, token)
            return (None, "")

        match = re.search(cls.end_pattern, token)
        token = token[match.end() :] if match else token
        return (match, token)


class BulletList(_GFMList, ast.BulletList):
    def __init__(self) -> None:
        super().__init__()

    def process_read(self, **kwargs: Unpack[ast_helpers.ProcessParams]) -> None:
        match = kwargs["match"]
        indent = len(match.group("s"))
        self.contents.metadata = [indent]
        self.add_plain(kwargs["context"])


class OrderedList(_GFMList, ast.OrderedList):
    separator_dict = {".": ast_helpers.Separator.PERIOD, ")": ast_helpers.Separator.CLOSING_PAREN}
    numbering_type = ast_helpers.NumberingType.DECIMAL  # gfm supports only decimal numbering type

    def __init__(self) -> None:
        super().__init__()

    def process_read(self, **kwargs: Unpack[ast_helpers.ProcessParams]) -> None:
        match = kwargs["match"]

        indent = len(match.group("s"))
        starting_num = int(match.group("num"))
        separator = self.separator_dict[match.group("sep")]

        self.contents.metadata = [indent, starting_num, OrderedList.numbering_type, separator]
        self.add_plain(kwargs["context"])
