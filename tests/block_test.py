import pytest
from pyndoc.ast.blocks import ASTBlock, Str


def test_empty_ast_block():
    """
    new AST blocks need a name,
    TypeError should be raised if one is not provided
    """
    with pytest.raises(TypeError):
        ASTBlock()


def test_custom_ast_block():
    """
    Testing an AST Block with just another name
    """
    b = ASTBlock(name="NewBlock")
    assert b.name == "NewBlock"


def test_str_block():
    """
    Testing a generic Str block
    """
    b = Str("This is a string")
    assert b.content == "This is a string"


def test_str_change():
    """
    Testing changing Str contents
    """
    b = Str()
    assert not b.content
    b.content = ["abcd"]
    assert b.content == ["abcd"]


# -------------- GFM BLOCKS -------------------
