import pytest
from pyndoc.ast.blocks import BulletList, OrderedList
from pyndoc.readers.reader import Reader
from tests.reader_test import mock_file


@pytest.fixture
def gfm_reader():
    return Reader("gfm")


@pytest.mark.parametrize(
    ("data", "list_type"),
    [
        ("- item 1\n\n", BulletList),
        ("- item 1\n- item2\n- item3\n\n", BulletList),
        ("1. item 1\n2. next item", OrderedList),
        ("1. item\n\t- nested bullet\n\n2. item2", OrderedList),
    ],
)
@mock_file
def test_list_type(gfm_reader, list_type, mocker, data):
    gfm_reader.read("")
    md_list = gfm_reader._parser._tree[0]
    assert isinstance(md_list, list_type)


@pytest.mark.parametrize(
    ("data", "num_elements"),
    [
        ("- item 1\n\n", 1),
        ("- item 1\n- item2\n- item3\n\n", 3),
        ("1. item\n\t- nested bullet\n\t- next bullet item\n2. item2", 3),
    ],
)
@mock_file
def test_list_num_elements(gfm_reader, num_elements, mocker, data):
    gfm_reader.read("")
    md_list = gfm_reader._parser._tree[0]
    assert len(md_list.contents.contents) == num_elements
