import pytest
import functools
from pyndoc.readers.reader import Reader
from pyndoc.writers.latex_writer import LatexWriter


@pytest.fixture
def gfm_reader():
    return Reader("gfm")


@pytest.fixture
def latex_writer():
    return LatexWriter()


def mock_file(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        mocker = kwargs.get("mocker")
        data = kwargs.get("data")

        # Mockowanie otwarcia pliku
        mocked_data = mocker.mock_open(read_data=data)
        mocker.patch("builtins.open", mocked_data)

        return func(*args, **kwargs)

    return wrapper


@pytest.mark.parametrize(
    ("data", "expected_latex"),
    [
        (
            "# Header 1\nThis is a paragraph.",
            "\\documentclass{article}\n\\begin{document}\n\\section{Header 1}\nThis is a paragraph.\n\n\\end{document}",
        ),
        (
            "- Item 1\n- Item 2",
            "\\documentclass{article}\n\\begin{document}\n\\begin{itemize}\n\\item Item 1\n\\item Item 2\n\\end{itemize}\n\\end{document}",
        ),
    ],
)
@mock_file
def test_markdown_to_latex(gfm_reader, latex_writer, mocker, data, expected_latex):
    filename = "test.md"

    gfm_reader.read(filename)

    ast_tree = gfm_reader._parser._tree

    generated_latex = latex_writer._get_latex_representation(ast_tree)
    assert generated_latex.strip() == expected_latex.strip()


@pytest.mark.parametrize(
    ("data", "expected_latex"),
    [
        (
            "# Header 1",
            "\\documentclass{article}\n\\begin{document}\n\\section{Header 1}\n\\end{document}",
        ),
        (
            "## Header 2",
            "\\documentclass{article}\n\\begin{document}\n\\subsection{Header 2}\n\\end{document}",
        ),
        (
            "### Header 3",
            "\\documentclass{article}\n\\begin{document}\n\\subsubsection{Header 3}\n\\end{document}",
        ),
        (
            "#### Header 4",
            "\\documentclass{article}\n\\begin{document}\n\\paragraph{Header 4}\n\\end{document}",
        ),
        (
            "##### Header 5",
            "\\documentclass{article}\n\\begin{document}\n\\subparagraph{Header 5}\n\\end{document}",
        ),
    ],
)
@mock_file
def test_headers_to_latex(gfm_reader, latex_writer, mocker, data, expected_latex):
    filename = "test_headers.md"

    gfm_reader.read(filename)

    ast_tree = gfm_reader._parser._tree

    generated_latex = latex_writer._get_latex_representation(ast_tree)

    assert generated_latex.strip() == expected_latex.strip()


@pytest.mark.parametrize(
    ("data", "expected_latex"),
    [
        (
            "*italic text*",
            "\\documentclass{article}\n\\begin{document}\n\\emph{italic text}\n\n\\end{document}",
        ),
        (
            "**bold text**",
            "\\documentclass{article}\n\\begin{document}\n\\textbf{bold text}\n\n\\end{document}",
        ),
        (
            "*italic text* followed by **bold text**",
            "\\documentclass{article}\n\\begin{document}\n\\emph{italic text} followed by \\textbf{bold text}\n\n\\end{document}",
        ),
        (
            "**bold text with *italic inside***",
            "\\documentclass{article}\n\\begin{document}\n\\textbf{bold text with \\emph{italic inside}}\n\n\\end{document}",
        ),
        (
            "Normal text with *italic*, **bold**, and **bold *italic***",
            "\\documentclass{article}\n\\begin{document}\nNormal text with \\emph{italic}, \\textbf{bold}, and \\textbf{bold \\emph{italic}}\n\n\\end{document}",
        ),
    ],
)
@mock_file
def test_emphasis_and_bold_to_latex(gfm_reader, latex_writer, mocker, data, expected_latex):
    filename = "test_emphasis.md"

    gfm_reader.read(filename)

    ast_tree = gfm_reader._parser._tree

    generated_latex = latex_writer._get_latex_representation(ast_tree)

    assert generated_latex.strip() == expected_latex.strip()


@pytest.mark.parametrize(
    ("data", "expected_latex"),
    [
        (
            "# Header 1\nThis is a paragraph.",
            "\\documentclass{article}\n\\begin{document}\n\\section{Header 1}\nThis is a paragraph.\n\n\\end{document}",
        ),
        (
            "## Header 2\nThis is a paragraph.\n\n- Item 1\n- *Item 2*",
            "\\documentclass{article}\n\\begin{document}\n\\subsection{Header 2}\nThis is a paragraph.\n\n\\begin{itemize}\n\\item Item 1\n\\item \\emph{Item 2}\n\\end{itemize}\n\\end{document}",
        ),
    ],
)
@mock_file
def test_mixed_latex(gfm_reader, latex_writer, mocker, data, expected_latex):
    filename = "test_mixed.md"

    gfm_reader.read(filename)

    ast_tree = gfm_reader._parser._tree

    generated_latex = latex_writer._get_latex_representation(ast_tree)

    assert generated_latex.strip() == expected_latex.strip()
