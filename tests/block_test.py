import pytest
from pyndoc.ast.blocks import AstBlock, Str
import pyndoc.ast.gfm.blocks as gfm


def test_empty_ast_block():
    """
    new AST blocks need a name,
    TypeError should be raised if one is not provided
    """
    with pytest.raises(TypeError):
        AstBlock()


def test_custom_ast_block():
    """
    Testing an AST Block with just another name
    """
    b = AstBlock(name="NewBlock")
    assert b.name == "NewBlock"


def test_str_block():
    """
    Testing a generic Str block
    """
    b = Str("This is a string")
    assert b.contents == "This is a string"


def test_str_change():
    """
    Testing changing Str contents
    """
    b = Str()
    assert not b.contents
    b.contents = ["abcd"]
    assert b.contents == ["abcd"]

# -------------- GFM BLOCKS -------------------

def test_gfm_header():
    b = gfm.Header(1, "This is a header!")
    assert b.contents[1][0].contents == "This is a header!"
