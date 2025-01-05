from pyndoc.readers.gfm.blocks import Cell
from pyndoc.ast.blocks import Str, Space
import pytest


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
def test_checking_delimiter_cells(contents, is_delimiter):
    cell = Cell()
    cell.contents.contents = contents
    assert Cell.is_delimiter_cell(cell) == is_delimiter
