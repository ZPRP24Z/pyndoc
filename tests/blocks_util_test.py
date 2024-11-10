import pytest
from pyndoc.ast.blocks import Space, Str, decompose_text


@pytest.mark.parametrize(
    ("input_text", "block_list"),
    [
        (" after_space", [Str("after_space")]),
        ("trailing_space_cut ", [Str("trailing_space_cut")]),
        (
            "just a normal text",
            [
                Str("just"),
                Space(),
                Str("a"),
                Space(),
                Str("normal"),
                Space(),
                Str("text"),
            ],
        ),
        ("double_space  between", [Str("double_space"), Space(), Str("between")]),
    ],
)
def test_decompose_text(input_text, block_list):
    for result, expected in zip(decompose_text(input_text), block_list):
        assert result == expected
