import pytest
import functools
from pyndoc.readers.reader import Reader
from pyndoc.writers.typst_writer import TypstWriter


@pytest.fixture
def gfm_reader():
    return Reader("gfm")


@pytest.fixture
def typst_writer():
    return TypstWriter()


def mock_file(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        mocker = kwargs.get("mocker")
        data = kwargs.get("data")

        mocked_data = mocker.mock_open(read_data=data)
        mocker.patch("builtins.open", mocked_data)

        return func(*args, **kwargs)

    return wrapper


@pytest.mark.parametrize(
    ("data", "expected_typst"),
    [
        (
            "# Header 1\nThis is a paragraph.",
            "= Header 1\nThis is a paragraph.\n\n",
        ),
        (
            "- Item 1\n- Item 2",
            "- Item 1\n- Item 2",
        ),
    ],
)
@mock_file
def test_markdown_to_typst(gfm_reader, typst_writer, mocker, data, expected_typst):
    filename = "test.md"

    gfm_reader.read(filename)

    ast_tree = gfm_reader._parser._tree

    generated_typst = typst_writer._get_typst_representation(ast_tree)
    assert generated_typst.strip() == expected_typst.strip()


@pytest.mark.parametrize(
    ("data", "expected_typst"),
    [
        ("# Header 1", "= Header 1"),
        ("## Header 2", "== Header 2"),
        ("### Header 3", "=== Header 3"),
        ("#### Header 4", "==== Header 4"),
        ("##### Header 5", "===== Header 5"),
    ],
)
@mock_file
def test_headers_to_typst(gfm_reader, typst_writer, mocker, data, expected_typst):
    filename = "test_headers.md"

    gfm_reader.read(filename)

    ast_tree = gfm_reader._parser._tree

    generated_typst = typst_writer._get_typst_representation(ast_tree)

    assert generated_typst.strip() == expected_typst.strip()


@pytest.mark.parametrize(
    ("data", "expected_typst"),
    [
        ("*italic text*", "*_italic text_*"),
        ("**bold text**", "*bold text*"),
        ("*italic text* followed by **bold text**", "*_italic text_* followed by *bold text*"),
        ("**bold text with *italic inside***", "*bold text with *_italic inside_**"),
        (
            "Normal text with *italic*, **bold**, and **bold *italic***",
            "Normal text with *_italic_*, *bold*, and *bold *_italic_**",
        ),
    ],
)
@mock_file
def test_emphasis_and_bold_to_typst(gfm_reader, typst_writer, mocker, data, expected_typst):
    filename = "test_emphasis.md"

    gfm_reader.read(filename)

    ast_tree = gfm_reader._parser._tree

    generated_typst = typst_writer._get_typst_representation(ast_tree)

    assert generated_typst.strip() == expected_typst.strip()
