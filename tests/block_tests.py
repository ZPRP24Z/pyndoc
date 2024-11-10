import pytest
import pyndoc.ast.blocks as ast


@pytest.fixture
def lvl1_header():
    return ast.Header(level=1)


def test_header_init(lvl1_header):

    assert lvl1_header.contents.metadata[0] == 1
    assert len(lvl1_header.contents.contents) == 0


def test_header_append(lvl1_header):
    str_block = ast.Str("Foo")

    lvl1_header.insert(str_block)
    assert len(lvl1_header.contents.contents) == 1
    assert lvl1_header.contents.contents[0] == str_block
