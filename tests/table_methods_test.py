from pyndoc.readers.gfm.blocks import Cell
from pyndoc.ast.blocks import Str, Space
from pyndoc.ast.helpers import Alignment
import pytest


@pytest.fixture
def cell_fix(contents):
    cell = Cell()
    cell.contents.contents = contents
    return cell


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
def test_checking_delimiter_cells(cell_fix, is_delimiter):
    assert Cell.is_delimiter_cell(cell_fix) == is_delimiter


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
def test_cell_get_alignment(cell_fix, alignment):
    assert Cell.get_delimiter_cell_alignment(cell_fix) == alignment
