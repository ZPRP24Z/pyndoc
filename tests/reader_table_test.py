import pytest
from pyndoc.ast.blocks import Table, TableHead, TableBody
from pyndoc.readers.reader import Reader
from tests.reader_test import mock_file


@pytest.fixture
def gfm_reader():
    return Reader("gfm")


@pytest.mark.parametrize(
    ("data", "content_types"),
    [
        ("| hhhh | gggg |\n| ----- | ----- |\n\n", [TableHead]),
        (
            "|here header text | second col | dsdsds |\n| --- | ----- | --- |\n\nHere is additional text",
            [TableHead],
        ),
        (
            "|now|multiline|table|\n|---|--|-|\n|hello|dssdsd|row3|\n\nAnd now lets check if it ends correctly",
            [TableHead, TableBody],
        ),
    ],
)
@mock_file
def test_table_contents(gfm_reader, content_types, mocker, data):
    gfm_reader.read("")
    table = gfm_reader._parser._tree[0]
    assert isinstance(table, Table)
    assert len(table.contents.contents) == len(content_types)
    for content, type in zip(table.contents.contents, content_types):
        assert isinstance(content, type)
