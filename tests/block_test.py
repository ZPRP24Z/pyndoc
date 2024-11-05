import pytest
from pyndoc.ast.blocks import AstBlock, Str
import pyndoc.ast.blocks as ast
from pyndoc.ast.gfm.declare import declare_gfm
import re


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
GFM_DICT = declare_gfm()

@pytest.mark.parametrize(
    ("pattern", "text"),
    [
        (GFM_DICT[ast.Header][0], "# H"),
        (GFM_DICT[ast.Header][0], "## H"),
        (GFM_DICT[ast.Header][0], "#### H"),
        (GFM_DICT[ast.Header][0], "###### H"),
    ]    
)
def test_header_regex(pattern, text):
    assert re.search(pattern, text)

@pytest.mark.parametrize(
    ("pattern", "text"),
    [
        (GFM_DICT[ast.Italic][0], "*italic*"),
        (GFM_DICT[ast.Italic][0], "test *italic* test"),
        (GFM_DICT[ast.Bold][0], "**bold**"),
        (GFM_DICT[ast.Bold][0], "test **bold** test")
    ]
)
def test_italic_bold_regex(pattern, text):
    assert re.search(pattern, text)

@pytest.mark.parametrize(
    ("pattern", "text"),
    [
        (GFM_DICT[ast.Italic][0], "***italic***"),
        (GFM_DICT[ast.Italic][0], "test ***italic*** test"),
        (GFM_DICT[ast.Bold][0], "***bold***"),
        (GFM_DICT[ast.Bold][0], "test ***bold*** test")
    ]
)
def test_italic_and_bold_regex(pattern, text):
    assert re.search(pattern, text)
