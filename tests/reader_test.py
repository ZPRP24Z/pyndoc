import pytest
from pyndoc.readers.reader import Reader
import pyndoc.ast.blocks as ast


@pytest.fixture
def gfm_reader():
    return Reader("gfm")


def mock_file(data):
    def decorator(func):
        def wrapper(mocker, gfm_reader):
            mocked_data = mocker.mock_open(read_data=data)
            builtin_open = "builtins.open"
            mocker.patch(builtin_open, mocked_data)
            return func(gfm_reader)

        return wrapper

    return decorator


def test_reader_init(gfm_reader):
    assert len(gfm_reader._block_types) == 4
    assert len(gfm_reader._atom_block_types) == 2


@mock_file(data="# simple header\n")
def test_simple_header_with_space(gfm_reader):
    gfm_reader.read(filename="Foo")

    assert gfm_reader._tree[0]
    inside_blocks = gfm_reader._tree[0].contents.contents

    assert inside_blocks[0] == ast.Str("simple")
    assert inside_blocks[1] == ast.Space()
    assert inside_blocks[2] == ast.Str("header")


@mock_file(data="*italic*")
def test_just_italic(gfm_reader):
    gfm_reader.read(filename="Foo")

    assert gfm_reader._tree[0]
    inside_blocks = gfm_reader._tree[0].contents.contents
    assert inside_blocks[0] == ast.Str("italic")
