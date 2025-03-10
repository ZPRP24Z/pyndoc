from __future__ import annotations
import re
from typing_extensions import Unpack
from abc import ABC

import pyndoc.ast.basic_blocks as ast_base
import pyndoc.ast.blocks as ast
from pyndoc.ast.read_handler import CompositeReadHandler
import pyndoc.ast.helpers as ast_helpers


class Space(ast.Space):
    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def match_pattern(cls, **kwargs: Unpack[ast_helpers.AtomMatchParams]) -> tuple[re.Match | None, str]:
        context = kwargs["context"]
        text = kwargs["text"]
        if not context or context[-1].__class__.__name__ in ("BulletList", "OrderedList"):
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

        if not context or context[-1].__class__.__name__ in ("BulletList", "OrderedList"):
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

        if context[-2] and context[-2].__class__.__name__ == "Strong":
            match = re.search(cls.end_pattern[:2], token)
            token = token[match.end() :] if match else token
        else:
            match = re.search(cls.end_pattern[:], token)
            token = token[match.end() - 1 :] if match else token
        return (match, token)

    @classmethod
    def handle_premature_closure(cls, **kwargs: Unpack[ast_helpers.EndParams]) -> str:
        token = kwargs["token"]
        return token[:-1] if token[-1] == "*" else token


class _GFMList(ABC, CompositeReadHandler):
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


class Table(ast.Table):
    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def add_table_head(context: list) -> None:
        table_head = TableHead()
        context.append(table_head)

    @staticmethod
    def add_table_body(context: list) -> None:
        table_body = TableBody()
        context.append(table_body)

    @staticmethod
    def add_row(context: list) -> None:
        row = Row()
        context.append(row)

    @staticmethod
    def add_cell(context: list) -> None:
        cell = Cell()
        context.append(cell)

    @classmethod
    def handle_table_end(cls, context: list) -> None:
        table = context[-1]
        thead = table.contents.contents[0]
        alignment = table.contents.metadata[0]
        row_size = len(alignment)

        TableHead.format_table_head(thead, alignment, row_size)
        if len(table.contents.contents) > 1:
            tbody = table.contents.contents[1]
            TableBody.format_table_body(tbody, alignment, row_size)

        context[-1] = table

    @classmethod
    def handle_table_head_end(cls, context: list) -> None:
        table = context[-2]
        thead = context[-1]
        delimiter_row = thead.contents.contents.pop()
        row_contents = delimiter_row.contents.contents

        if not Row.is_delimiter_row(delimiter_row):
            raise NotImplementedError

        alignment = ast_helpers.AlignmentList([Cell.get_delimiter_cell_alignment(cell) for cell in row_contents])

        table.contents.metadata = [alignment]

    def process_read(self, **kwargs: Unpack[ast_helpers.ProcessParams]) -> None:
        context = kwargs.get("context")
        self.add_table_head(context)
        self.add_row(context)
        self.add_cell(context)
        return

    @classmethod
    def handle_premature_closure(cls, **kwargs: Unpack[ast_helpers.EndParams]) -> str:
        context = kwargs["context"]
        token = kwargs["token"]
        cls.handle_table_end(context)
        return token

    @classmethod
    def start(cls, **kwargs: Unpack[ast_helpers.StartParams]) -> tuple[re.Match | None, str]:
        token = kwargs["token"]
        context = kwargs["context"]

        if context and context[-1].__class__.__name__ in ("Table", "TableHead", "TableBody", "Row", "Cell"):
            return (None, token)

        match = re.search(cls.start_pattern, token)
        token = token[match.end() :] if match else token

        return (match, token)

    @classmethod
    def end(cls, **kwargs: Unpack[ast_helpers.EndParams]) -> tuple[re.Match | None, str]:
        token = kwargs["token"]
        match = re.search(cls.end_pattern, token)

        if match:
            cls.handle_table_end(kwargs["context"])

        return (match, token)


class TableHead(ast.TableHead):
    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def format_table_head(thead: TableHead, alignment: list[ast_helpers.Alignment], row_size: int) -> None:
        if not len(thead.contents.contents):
            raise ValueError("Invalid table head")
        elif not isinstance(thead.contents.contents[0], Row):
            raise ValueError("TableHead should contain only rows")

        Row.format_row(thead.contents.contents[0], alignment, row_size)

    @classmethod
    def end(cls, **kwargs: Unpack[ast_helpers.EndParams]) -> tuple[re.Match | None, str]:
        context = kwargs.get("context")
        token = kwargs.get("token")
        if len(context[-1].contents.contents) != 2:
            return (None, token)

        match = re.search(cls.end_pattern, token)
        if match:
            context[-2].handle_table_head_end(context)

        token = token[match.end() :] if match else token

        return (match, token)


class TableBody(ast.TableBody):
    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def format_table_body(tbody: TableBody, alignment: list[ast_helpers.Alignment], row_size: int) -> None:
        for row in tbody.contents.contents:
            if not isinstance(row, Row):
                raise ValueError("TableBody should contain only rows in contents")
            row = Row.format_row(row, alignment, row_size)

    @classmethod
    def end(cls, **kwargs: Unpack[ast_helpers.EndParams]) -> tuple[re.Match | None, str]:
        token = kwargs.get("token")

        match = re.search(cls.end_pattern, token)
        token = token[match.end() :] if match else token

        return (match, token)


class Row(ast.Row):
    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def format_row(row: Row, alignment: list[ast_helpers.Alignment], size: int) -> None:
        while len(row.contents.contents) < size:
            row.contents.contents.append(Cell())
        row.contents.contents = row.contents.contents[:size]

        for cell, align in zip(row.contents.contents, alignment):
            if not isinstance(cell, Cell):
                raise ValueError("Row should contain only cells")
            cell.contents.metadata.append(align)

    @staticmethod
    def is_delimiter_row(row: Row) -> bool:
        """Determines whether a row is delimiter row

        :param row: row being checked
        :type row: Row
        return: true if row is delimiter row, otherwise false
        :rtype: bool
        """
        for cell in row.contents.contents:
            if not isinstance(cell, Cell) or not Cell.is_delimiter_cell(cell):
                return False
        return True

    @classmethod
    def end(cls, **kwargs: Unpack[ast_helpers.EndParams]) -> tuple[re.Match | None, str]:
        token = kwargs.get("token")

        match = re.search(cls.end_pattern, token)
        token = token[match.end() :] if match else token

        return (match, token)


class Cell(ast.Cell):
    delimiter_regex = r"(?P<l>:?)-+(?P<r>:?)"

    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def is_delimiter_cell(cls, cell: Cell) -> bool:
        """Determines whether a cell is delimiter cell - has only one element
        that is a string and its content is in format matches regular expression (?P<l>:?)-+(?P<l>:?)
        e.g.: "-", ":----", "--:", ":---:"

        :param cell: cell being checked
        :type cell: Cell
        :return: true if passed cell is delimiter cell, otherwise false
        :rtype: bool
        """
        contents = cell.contents.contents

        if len(contents) == 1 and isinstance(contents[0], ast.Str):
            return re.match(cls.delimiter_regex, contents[0].contents) is not None

        return False

    @classmethod
    def get_delimiter_cell_alignment(cls, cell: Cell) -> ast_helpers.Alignment:
        """Returns the alignment of delimiter cell. To be used with cell that passed is_delimiter_cell method

        :param cell: cell being checked
        :type cell: Cell
        :return: cell alignment
        :rtype: Alignment
        """

        def _is_not_empty(span: tuple[int, int]) -> bool:
            return span[0] != span[1]

        if not cls.is_delimiter_cell(cell) or not isinstance(cell.contents.contents[0], ast.Str):
            raise ValueError("The cell provided as delimiter cell is not a delimiter cell")

        match = re.match(cls.delimiter_regex, cell.contents.contents[0].contents)

        if not match:
            raise ValueError("The cell provided didnt match delimiter cell regex")

        alignment_map = {
            (True, True): ast_helpers.Alignment.ALIGN_CENTER,
            (True, False): ast_helpers.Alignment.ALIGN_LEFT,
            (False, True): ast_helpers.Alignment.ALIGN_RIGHT,
            (False, False): ast_helpers.Alignment.ALIGN_DEFAULT,
        }
        return alignment_map[(_is_not_empty(match.span("l")), _is_not_empty(match.span("r")))]

    @classmethod
    def _delete_trailing_spaces(cls, context: list) -> None:
        contents = context[-1].contents.contents
        if not isinstance(context[-1], cls) or len(contents) == 1:
            return

        contents = contents[1:] if len(contents) > 1 and isinstance(contents[0], ast.Space) else contents
        context[-1].contents.contents = contents

    @classmethod
    def start(cls, **kwargs: Unpack[ast_helpers.StartParams]) -> tuple[re.Match | None, str]:
        # cell from its regex (due to its easy to meet contition) starts only within
        # existing table(and its components)
        token = kwargs["token"]
        context = kwargs["context"]

        match = re.search(cls.start_pattern, token)
        if not context or not match or context[-1].__class__.__name__ not in ("Table", "TableHead", "TableBody", "Row"):
            return (None, token)

        match context[-1].__class__.__name__:
            case "Table":
                context[-1].add_table_body(context)
                context[-2].add_row(context)
            case "TableBody" | "TableHead":
                context[-2].add_row(context)

        return (match, token[match.end("c") :])

    @classmethod
    def end(cls, **kwargs: Unpack[ast_helpers.EndParams]) -> tuple[re.Match | None, str]:
        token = kwargs["token"]
        context = kwargs["context"]

        match = re.search(cls.end_pattern, token)
        token = token[match.end() - 1 :] if match else token
        cls._delete_trailing_spaces(context)

        return (match, token)


class CodeBlockHelper(ast_base.ASTCompositeBlock):
    """A composite helper for parsing ``CodeBlocks``
    This block will create a ``CodeBlock`` in its contents, parse its metadata and adjust contents.
    When the block ends, it will replace itself with the ``CodeBlock`` in the context stack.
    """

    def __init__(self) -> None:
        super().__init__("CodeBlockHelper (Dev)")

    def process_read(self, **kwargs: Unpack[ast_helpers.ProcessParams]) -> None:
        """Parse a ``CodeBlock`` metadata and add an empty ``CodeBlock`` to the block's contents"""

        match = kwargs["match"]
        self.contents.contents.append(ast.CodeBlock())
        if isinstance(self.contents.contents[0], ast.CodeBlock):
            self.contents.contents[0].metadata.append(match.group("lang"))

    @classmethod
    def end(cls, **kwargs: Unpack[ast_helpers.EndParams]) -> tuple[re.Match | None, str]:
        """Add ANY token to the ``CodeBlock``,
        then check if the end of the block matches ``CodeBlock`` end pattern
        """

        token = kwargs["token"]
        context = kwargs["context"]
        code_block = context[-1].contents.contents[0]

        code_block.contents += token
        token = ""

        search_string = code_block.contents[-4:]
        match = re.search(cls.end_pattern, search_string)
        if not match:
            return (match, token)
        code_block.contents = code_block.contents[:-4]
        context[-1] = code_block
        return match, token


class CodeHelper(ast_base.ASTCompositeBlock):
    """A Helper for parsing inline code
    This block will create a ``Code`` in its contents, parse its metadata and adjust contents.
    When the block ends, it will replace itself with the ``Code`` in the context stack.
    """

    def __init__(self) -> None:
        super().__init__("CodeHelper (Dev)")

    def process_read(self, **kwargs: Unpack[ast_helpers.ProcessParams]) -> None:
        """Set the end pattern of the block based on the start pattern.
        Then add an empty ``Code`` block to the contents
        """

        match = kwargs["match"]
        if match:
            self.override_end(match.group()[:-1])
        code = ast.Code()
        code.contents += match.group()[-1]
        self.contents.contents.append(code)

    @classmethod
    def start(cls, **kwargs: Unpack[ast_helpers.StartParams]) -> tuple[re.Match | None, str]:
        token = kwargs["token"]
        match = re.search(cls.start_pattern, token)
        token = '' if match else token
        return match, token
    
    @classmethod
    def end(cls, **kwargs: Unpack[ast_helpers.EndParams]) -> tuple[re.Match | None, str]:
        """Add ANY token to the ``Code``,
        then check if the end of the block matches ``Code`` end pattern
        """
        token = kwargs["token"]
        context = kwargs["context"]
        code = context[-1].contents.contents[0]

        code.contents += token
        token = ""

        end_len = len(cls.end_pattern)
        search_string = code.contents[-end_len:]
        match = re.search(cls.end_pattern, search_string)
        if not match:
            return (match, token)
        code.contents = code.contents[:-end_len]
        context[-1] = code
        return match, token
