import pytest
from pyndoc.readers.reader import Reader
import pyndoc.ast.blocks as ast


@pytest.fixture
def gfm_reader():
    return Reader("gfm")


def test_reader_init(gfm_reader):
    assert len(gfm_reader._block_types) == 4
    assert len(gfm_reader._atom_block_types) == 2


def test_simple_header_with_space(mocker, gfm_reader):
    mocked_data = mocker.mock_open(read_data="# simple header \n")
    builtin_open = "builtins.open"
    mocker.patch(builtin_open, mocked_data)

    gfm_reader.read(filename="Foo")

    assert gfm_reader._tree[0]
    inside_blocks = gfm_reader._tree[0].contents.contents
    print(inside_blocks)

    assert inside_blocks[0] == ast.Str("simple")
    assert inside_blocks[1] == ast.Space()
    assert inside_blocks[2] == ast.Str("header")
