import pytest
from pyndoc.ast.blocks import Space, Str, SoftBreak, Header, Para, Emph, Strong, Code, BulletList
from pyndoc.writers.latex_writer import LatexWriter


@pytest.fixture
def latex_writer():
    return LatexWriter()


@pytest.mark.parametrize(
    ("ast_tree", "expected_output"),
    [
        ([Str("Hello")], "\\documentclass{article}\n\\begin{document}\nHello\\end{document}"),
        (
            [Para(contents=[Str("Hello"), Space(), Str("world!")])],
            "\\documentclass{article}\n\\begin{document}\nHello world!\n\n\\end{document}",
        ),
        (
            [Header(contents=[Str("Header")], metadata=[1])],
            "\\documentclass{article}\n\\begin{document}\n\\section{Header}\\end{document}",
        ),
    ],
)
def test_get_latex_representation(latex_writer, ast_tree, expected_output):
    assert latex_writer._get_latex_representation(ast_tree) == expected_output


@pytest.mark.parametrize(
    ("block", "expected_output"),
    [
        (Str("Hello"), "Hello"),
        (Space(), " "),
        (SoftBreak(), "\n"),
        (Emph(contents=[Str("emphasized")]), "\\emph{emphasized}"),
        (Strong(contents=[Str("bold")]), "\\textbf{bold}"),
        (Code(contents=[Str("code")]), "\\texttt{code}"),
        (
            Para(contents=[Str("This"), Space(), Str("is"), Space(), Str("a"), Space(), Str("paragraph.")]),
            "This is a paragraph.\n\n",
        ),
        (
            Header(contents=[Str("Header")], metadata=[1]),
            "\\section{Header}",
        ),
        (
            BulletList(
                contents=[
                    Para(contents=[Str("Item 1")]),
                    Para(contents=[Str("Item 2")]),
                ]
            ),
            "\\begin{itemize}\n\\item Item 1\n\\item Item 2\n\\end{itemize}",
        ),
    ],
)
def test_process_block(latex_writer, block, expected_output):
    assert latex_writer._process_block(block) == expected_output


@pytest.mark.parametrize(
    ("contents", "expected_output"),
    [
        ([Str("Text"), Space(), Str("more text")], "Text more text"),
        (
            [
                Emph(contents=[Str("italic")]),
                Space(),
                Strong(contents=[Str("bold")]),
            ],
            "\\emph{italic} \\textbf{bold}",
        ),
    ],
)
def test_process_contents(latex_writer, contents, expected_output):
    assert latex_writer._process_contents(contents) == expected_output


@pytest.mark.parametrize(
    ("ast_tree", "expected_output"),
    [
        (
            [
                Para(contents=[Str("Paragraph"), Space(), Str("one")]),
                Para(contents=[Str("Paragraph"), Space(), Str("two")]),
            ],
            "\\documentclass{article}\n\\begin{document}\nParagraph one\n\nParagraph two\n\n\\end{document}",
        ),
        (
            [
                Header(contents=[Str("Header")], metadata=[1]),
                Para(contents=[Str("Body"), Space(), Str("text")]),
            ],
            "\\documentclass{article}\n\\begin{document}\n\\section{Header}\nBody text\n\n\\end{document}",
        ),
    ],
)
def test_complex_ast_tree(latex_writer, ast_tree, expected_output):
    assert latex_writer._get_latex_representation(ast_tree) == expected_output
