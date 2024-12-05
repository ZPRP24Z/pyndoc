import pytest
import functools
from pyndoc.readers.reader import Reader
import pyndoc.ast.blocks as ast


@pytest.fixture
def gfm_reader():
    return Reader("gfm")


def mock_file(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        mocker = kwargs.get("mocker")

        data = kwargs.get("data")
        mocked_data = mocker.mock_open(read_data=data)
        builtin_open = "builtins.open"
        mocker.patch(builtin_open, mocked_data)

        return func(*args, **kwargs)

    return wrapper


@pytest.mark.parametrize(
    ("data", "block_type"),
    [
        ("# simple header\n", ast.Header),
        ("## level 2 header\n", ast.Header),
        ("### level 3 header with *some italic text*\n", ast.Header),
        (
            "*italic text*",
            ast.Para,
        ),
        ("Paragraph", ast.Para),
    ],
)
@mock_file
def test_simple_type(gfm_reader, block_type, mocker, data):
    gfm_reader.read(filename="Foo")
    assert isinstance(gfm_reader._parser._tree[0], block_type)


@pytest.mark.parametrize(
    ("data", "contents_len"),
    [
        ("# has 5 strings 4 spaces\n", 9),
        ("# text *italic text here - header has 3 blocks - 1 space 2 str*", 3),
        (
            "*italic text with 8 strings and 7   corrected-spaces*",
            1,
        ),
    ],
)
@mock_file
def test_simple_len(gfm_reader, contents_len, mocker, data):
    gfm_reader.read("Foo")
    assert len(gfm_reader._parser._tree[0].contents.contents) == contents_len


@pytest.mark.parametrize(
    ("data", "atom_block_list"),
    [
        (
            "# level one header\n",
            [
                ast.Str("level"),
                ast.Space(),
                ast.Str("one"),
                ast.Space(),
                ast.Str("header"),
            ],
        ),
        (
            "## header with   too much    spaces\n",
            [
                ast.Str("header"),
                ast.Space(),
                ast.Str("with"),
                ast.Space(),
                ast.Str("too"),
                ast.Space(),
                ast.Str("much"),
                ast.Space(),
                ast.Str("spaces"),
            ],
        ),
    ],
)
@mock_file
def test_composite_blocks_with_atom_contents(gfm_reader, atom_block_list, mocker, data):
    gfm_reader.read("Foo")
    composite_block_contents = gfm_reader._parser._tree[0].contents.contents
    assert composite_block_contents == atom_block_list


@pytest.mark.parametrize(
    ("data", "blocks"),
    [
        (
            "# Header without newline",
            [
                ast.Str("Header"),
                ast.Space(),
                ast.Str("without"),
                ast.Space(),
                ast.Str("newline"),
            ],
        ),
    ],
)
@mock_file
def test_eof_header(gfm_reader, mocker, data, blocks):
    gfm_reader.read("Foo")
    assert gfm_reader._parser._tree[0].contents.contents == blocks


@pytest.mark.parametrize(
    ("data", "blocks"),
    [
        ("para1\n\npara2", [ast.Para, ast.Para]),
        ("para", [ast.Para]),
        ("#incorrectheader", [ast.Para]),
        ("para\npara", [ast.Para]),
        ("*para*\n\npara", [ast.Para, ast.Para]),
        ("**para**\n\npara", [ast.Para, ast.Para]),
    ],
)
@mock_file
def test_para(gfm_reader, mocker, data, blocks):
    gfm_reader.read("Foo")
    assert len(gfm_reader._parser._tree) == len(blocks)
    for idx, block in enumerate(gfm_reader._parser._tree):
        assert isinstance(block, blocks[idx])


@pytest.mark.parametrize(
    ("data", "type", "blocks"),
    [
        ("*italic text*", ast.Emph, [ast.Str("italic"), ast.Space(), ast.Str("text")]),
        (
            "*unfinished italic",
            ast.Emph,
            [ast.Str("unfinished"), ast.Space(), ast.Str("italic")],
        ),
        (
            "*italic\ntext* cos tu",
            ast.Emph,
            [ast.Str("italic"), ast.SoftBreak(), ast.Str("text")],
        ),
        ("**bold**", ast.Strong, [ast.Str("bold")]),
        (
            "**here is   bold text",
            ast.Strong,
            [
                ast.Str("here"),
                ast.Space(),
                ast.Str("is"),
                ast.Space(),
                ast.Str("bold"),
                ast.Space(),
                ast.Str("text"),
            ],
        ),
    ],
)
@mock_file
def test_para_inline_content(gfm_reader, mocker, data, type, blocks):
    gfm_reader.read("Foo")
    assert len(gfm_reader._parser._tree) == 1
    inline_block = gfm_reader._parser._tree[0].contents.contents[0]
    assert isinstance(inline_block, type)
    assert len(inline_block.contents.contents) == len(blocks)
    for idx, block in enumerate(inline_block.contents.contents):
        assert block == blocks[idx]


@pytest.mark.parametrize(
    ("data", "atom_blocks"),
    [
        ("string\n", [ast.Str("string"), ast.SoftBreak()]),
        (
            "string\nwith\nSoftbreaks",
            [
                ast.Str("string"),
                ast.SoftBreak(),
                ast.Str("with"),
                ast.SoftBreak(),
                ast.Str("Softbreaks"),
            ],
        ),
    ],
)
@mock_file
def test_para_atom_content(gfm_reader, mocker, data, atom_blocks):
    gfm_reader.read("Foo")
    assert len(gfm_reader._parser._tree) == 1
    assert isinstance(gfm_reader._parser._tree[0], ast.Para)
    read_blocks = gfm_reader._parser._tree[0].contents.contents
    assert read_blocks == atom_blocks


@pytest.mark.parametrize(
    ("data", "outside_type", "nested_type", "pos_idx"),
    [
        ("**here is nested *italic* and sth**", ast.Strong, ast.Emph, 6),
        ("**nested *italic***", ast.Strong, ast.Emph, 2),
        ("*inside italic **strong** and sth*", ast.Emph, ast.Strong, 4),
        ("***nested strong italic***", ast.Strong, ast.Emph, 0),
    ],
)
@mock_file
def test_nested_inlines(gfm_reader, mocker, data, outside_type, nested_type, pos_idx):
    gfm_reader.read("Foo")
    outside_inline = gfm_reader._parser._tree[0].contents.contents[0]
    assert isinstance(outside_inline, outside_type)
    assert isinstance(outside_inline.contents.contents[pos_idx], nested_type)


@pytest.mark.parametrize(
    ("data", "plain_amt", "plain_content_amt"),
    [
        ("* bullet list", 1, 3),
        ("+ bullet list", 1, 3),
        ("- bullet list", 1, 3),
        ("* bullet list\n* bullet list 2", 2, 8),
        ("   * bullet", 1, 1),
    ],
)
@mock_file
def test_bulletlist(gfm_reader, mocker, data, plain_amt, plain_content_amt):
    gfm_reader.read("Foo")
    bullet_list = gfm_reader._parser._tree[0].contents.contents
    assert len(bullet_list) == plain_amt
    plain_sum = 0
    for plain in bullet_list:
        assert plain.name == "Plain"
        plain_sum += len(plain.contents.contents)

    assert plain_sum == plain_content_amt


@pytest.mark.parametrize(
    ("data", "types"),
    [
        ("* bullet list\n  * nested bullet", ["Plain", "BulletList"]),
        (
            "* bullet list\n  * nested bullet\n* old bullet",
            ["Plain", "BulletList", "Plain"],
        ),
        (
            "* bullet list\n  - nested bullet\n* old bullet",
            ["Plain", "BulletList", "Plain"],
        ),
        (
            "+ bullet list\n  - nested bullet\n+ old bullet",
            ["Plain", "BulletList", "Plain"],
        ),
        (
            "+ bullet\n - nested bullet\n\n+ old bullet",
            ["Plain", "BulletList", "Plain"],
        ),
    ],
)
@mock_file
def test_nested_bullet(gfm_reader, mocker, data, types):
    gfm_reader.read("Foo")
    bullet_list = gfm_reader._parser._tree[0].contents.contents
    for idx, item in enumerate(bullet_list):
        assert item.name == types[idx]


@pytest.mark.parametrize(
    ("data", "types"),
    [
        ("`code`", ["Code"]),
        ("Some `code`", ["Str", "Space", "Code", "Str"]),
        ("`code` some", ["Code", "Space", "Str"]),
        ("`code` some `more code`", ["Code", "Space", "Str", "Space", "Code"]),
    ],
)
@mock_file
def test_code_inline(gfm_reader, mocker, data, types):
    gfm_reader.read("Foo")
    code_blocks = gfm_reader._parser._tree[0].contents.contents
    for idx, item in enumerate(code_blocks):
        assert item.name == types[idx]
