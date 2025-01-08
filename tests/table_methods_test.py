from pyndoc.readers.gfm.blocks import Cell, Row
from pyndoc.ast.blocks import Str, Space
from pyndoc.ast.helpers import Alignment
import pytest


@pytest.fixture
def cell(contents):
    cell = Cell()
    cell.contents.contents = contents
    return cell


@pytest.fixture
def row(contents):
    row = Row()
    row_contents = []

    for cell_contents in contents:
        cell = Cell()
        cell.contents.contents = cell_contents
        row_contents.append(cell)

    row.contents.contents = row_contents
    return row


@pytest.mark.parametrize(
    ("contents", "is_delimiter"),
    [
        ([Str("-")], True),
        ([Str(":-:")], True),
        ([Str("-:")], True),
        ([Str("------------------")], True),
        ([Str(":---------")], True),
        ([Str(":----:")], True),
        ([Str("---:")], True),
        ([Str("blblblb")], False),
        ([Str(":9dsd--2:")], False),
        ([Str("900-600-300")], False),
        ([Str("10:37")], False),
        ([Str(":tag")], False),
        ([Str("dss"), Space(), Str("test")], False),
        ([Space(), Str("sth")], False),
        ([Str("other_test:"), Space()], False),
        ([Str("multiple"), Space(), Str("words"), Space(), Str("here")], False),
    ],
)
def test_check_delimiter_cells(cell, is_delimiter):
    assert Cell.is_delimiter_cell(cell) == is_delimiter


@pytest.mark.parametrize(
    ("contents", "alignment"),
    [
        ([Str("-")], Alignment.ALIGN_DEFAULT),
        ([Str(":-:")], Alignment.ALIGN_CENTER),
        ([Str("-:")], Alignment.ALIGN_RIGHT),
        ([Str("-------------")], Alignment.ALIGN_DEFAULT),
        ([Str(":---------")], Alignment.ALIGN_LEFT),
        ([Str(":----:")], Alignment.ALIGN_CENTER),
        ([Str("---:")], Alignment.ALIGN_RIGHT),
    ],
)
def test_cell_get_alignment(cell, alignment):
    assert Cell.get_delimiter_cell_alignment(cell) == alignment


@pytest.mark.parametrize(
    ("contents", "is_delimiter_row"),
    [
        ([[Str("---")], [Str("----")], [Str("-----")]], True),
        ([[Str(":---:")], [Str(":----:")], [Str(":-----:")]], True),
        ([[Str("esfsd")], [Str("---")], [Str("sdsd")]], False),
        ([[Str("--:")]], True),
        ([[Str("---"), Space()], [Str("----")], [Str("-----")]], False),
    ],
)
def test_check_delimiter_row(row, is_delimiter_row):
    assert Row.is_delimiter_row(row) == is_delimiter_row


@pytest.mark.parametrize(
    ("contents", "alignment", "row_size"),
    [
        (
            [[Str("first"), Space(), Str("cell")], [Str("dsds")], [Str("third"), Space(), Str("cell")]],
            [Alignment.ALIGN_CENTER, Alignment.ALIGN_CENTER, Alignment.ALIGN_CENTER],
            3,
        ),
        (
            [[Str("row"), Space(), Str("missing")], [Str("Cells")]],
            [Alignment.ALIGN_LEFT, Alignment.ALIGN_DEFAULT, Alignment.ALIGN_RIGHT, Alignment.ALIGN_CENTER],
            4,
        ),
    ],
)
def test_format_row(row, alignment, row_size):
    Row.format_row(row, alignment, row_size)
    assert len(row.contents.contents) == row_size
    for cell, align in zip(row.contents.contents, alignment):
        assert cell.contents.metadata[0] == align
