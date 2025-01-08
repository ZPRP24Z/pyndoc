import pytest
from pyndoc.ast.blocks import Table, TableHead, TableBody
from pyndoc.readers.reader import Reader
from pyndoc.ast.helpers import Alignment
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
        (
            "|head1|head2|\n|-|-|\n|normal|row|\n|row missing cell|\n|normal|row|\n\n",
            [TableHead, TableBody],
        ),
        (
            "| head |\n| :-- | :-----: |\n| there is a | missing head cell |\n\n",
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


@pytest.mark.parametrize(
    ("data", "alignment"),
    [
        ("| sdsds | fdf |\n| ----- | ----- |\n\n", [Alignment.ALIGN_DEFAULT, Alignment.ALIGN_DEFAULT]),
        (
            "|here header text | second col | dsdsds |\n| :-- | :---: | --: |\n\nHere is additional text",
            [Alignment.ALIGN_LEFT, Alignment.ALIGN_CENTER, Alignment.ALIGN_RIGHT],
        ),
        (
            "|now|multiline|table|\n|---|:--|-|\n|hello|dssdsd|row3|\n\nAnd now lets check if it ends correctly",
            [Alignment.ALIGN_DEFAULT, Alignment.ALIGN_LEFT, Alignment.ALIGN_DEFAULT],
        ),
        (
            "|head1|head2|\n|:-:|:-:|\n|normal|row|\n|row missing cell|\n|normal|row|\n\n",
            [Alignment.ALIGN_CENTER, Alignment.ALIGN_CENTER],
        ),
        (
            "| head |\n| :-- | :-----: |\n| there is a | missing head cell |\n\n",
            [Alignment.ALIGN_LEFT, Alignment.ALIGN_CENTER],
        ),
    ],
)
@mock_file
def test_table_alignment(gfm_reader, alignment, mocker, data):
    gfm_reader.read("")
    table = gfm_reader._parser._tree[0]
    assert table.contents.metadata[0] == alignment
