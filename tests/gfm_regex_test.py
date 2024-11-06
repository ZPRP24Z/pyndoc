import pyndoc.ast.blocks as ast
import re
import pytest
from pyndoc.ast.gfm.declare import declare_gfm

GFM_DICT = declare_gfm()


@pytest.mark.parametrize(
    ("pattern", "text"),
    [
        (GFM_DICT[ast.Header][0], "# H"),
        (GFM_DICT[ast.Header][0], "## H"),
        (GFM_DICT[ast.Header][0], "#### H"),
        (GFM_DICT[ast.Header][0], "###### H"),
    ],
)
def test_header_regex(pattern, text):
    assert re.search(pattern, text)


@pytest.mark.parametrize(
    ("pattern", "text"),
    [
        (GFM_DICT[ast.Emph][0], "*italic*"),
        (GFM_DICT[ast.Emph][0], "test *italic* test"),
        (GFM_DICT[ast.Strong][0], "**bold**"),
        (GFM_DICT[ast.Strong][0], "test **bold** test"),
    ],
)
def test_italic_bold_regex(pattern, text):
    assert re.search(pattern, text)


@pytest.mark.parametrize(
    ("pattern", "text"),
    [
        (GFM_DICT[ast.Emph][0], "***italic***"),
        (GFM_DICT[ast.Emph][0], "test ***italic*** test"),
        (GFM_DICT[ast.Strong][0], "***bold***"),
        (GFM_DICT[ast.Strong][0], "test ***bold*** test"),
    ],
)
def test_italic_and_bold_regex(pattern, text):
    assert re.search(pattern, text)


@pytest.mark.parametrize(
    ("pattern", "text"),
    [
        (GFM_DICT[ast.Emph][0], "*italic* *italic*"),
        (GFM_DICT[ast.Emph][0], "*italic* **bold**"),
        (GFM_DICT[ast.Strong][0], "**bold** **bold**"),
        (GFM_DICT[ast.Strong][0], "**bold** *italic*"),
    ],
)
def test_multiple_patterns_in_line(pattern, text):
    assert re.search(pattern, text)


@pytest.mark.parametrize(
    ("pattern", "text"),
    [
        (GFM_DICT[ast.Code][0], "`code` `code`"),
        (GFM_DICT[ast.Code][0], "``code`` `code`"),
        (GFM_DICT[ast.Code][0], "`code` ``code``"),
        (GFM_DICT[ast.Code][0], "`code`"),
    ],
)
def test_inline_code(pattern, text):
    assert re.search(pattern, text)


@pytest.mark.parametrize(
    ("pattern", "text"),
    [
        (GFM_DICT[ast.Code][0], "`not \n code`"),
        (GFM_DICT[ast.Emph][0], "*not \n italic*"),
        (GFM_DICT[ast.Strong][0], "`**not \n bold**"),
        (
            GFM_DICT[ast.Code][0],
            """
        `this is
         not code`
         """,
        ),
    ],
)
def test_newline_inline_patterns(pattern, text):
    assert not re.search(pattern, text)


@pytest.mark.parametrize(
    ("pattern", "text", "contents"),
    [
        (GFM_DICT[ast.Header][0], "# Header", "Header"),
        (GFM_DICT[ast.Emph][0], "*italic*", "italic"),
        (GFM_DICT[ast.Strong][0], "**bold**", "bold"),
        (GFM_DICT[ast.Code][0], "`code`", "code"),
        (GFM_DICT[ast.Strong][0], "***bolditalic***", "*bolditalic*"),
    ],
)
def test_groups(pattern, text, contents):
    match = re.search(pattern, text)
    assert match.group("contents") == contents
