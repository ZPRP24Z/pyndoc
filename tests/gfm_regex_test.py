# import pyndoc.ast.blocks as ast
# import pyndoc.ast.gfm.blocks as gfm
# import re
# import pytest
# from pyndoc.ast.gfm.declare import declare

# GFM_DICT = declare()
# header_pattern = [key for key in GFM_DICT.keys() if GFM_DICT[key] == gfm.Header][0]
# print(header_pattern)
# emph_pattern = [key for key in GFM_DICT.keys() if GFM_DICT[key] == ast.Emph][0]
# strong_pattern = [key for key in GFM_DICT.keys() if GFM_DICT[key] == ast.Strong][0]
# code_pattern = [key for key in GFM_DICT.keys() if GFM_DICT[key] == ast.Code][0]


# @pytest.mark.parametrize(
#     ("pattern", "text"),
#     [
#         (header_pattern, "# H"),
#         (header_pattern, "## H"),
#         (header_pattern, "#### H"),
#         (header_pattern, "###### H"),
#     ],
# )
# def test_header_regex(pattern, text):
#     assert re.search(pattern, text)


# @pytest.mark.parametrize(
#     ("pattern", "text"),
#     [
#         (emph_pattern, "*italic*"),
#         (emph_pattern, "test *italic* test"),
#         (strong_pattern, "**bold**"),
#         (strong_pattern, "test **bold** test"),
#     ],
# )
# def test_italic_bold_regex(pattern, text):
#     assert re.search(pattern, text)


# @pytest.mark.parametrize(
#     ("pattern", "text"),
#     [
#         (emph_pattern, "***italic***"),
#         (emph_pattern, "test ***italic*** test"),
#         (strong_pattern, "***bold***"),
#         (strong_pattern, "test ***bold*** test"),
#     ],
# )
# def test_italic_and_bold_regex(pattern, text):
#     assert re.search(pattern, text)


# @pytest.mark.parametrize(
#     ("pattern", "text"),
#     [
#         (emph_pattern, "*italic* *italic*"),
#         (emph_pattern, "*italic* **bold**"),
#         (strong_pattern, "**bold** **bold**"),
#         (strong_pattern, "**bold** *italic*"),
#     ],
# )
# def test_multiple_patterns_in_line(pattern, text):
#     assert re.search(pattern, text)


# @pytest.mark.parametrize(
#     ("pattern", "text"),
#     [
#         (code_pattern, "`code` `code`"),
#         (code_pattern, "``code`` `code`"),
#         (code_pattern, "`code` ``code``"),
#         (code_pattern, "`code`"),
#     ],
# )
# def test_inline_code(pattern, text):
#     assert re.search(pattern, text)


# @pytest.mark.parametrize(
#     ("pattern", "text"),
#     [
#         (code_pattern, "`not \n code`"),
#         (emph_pattern, "*not \n italic*"),
#         (strong_pattern, "`**not \n bold**"),
#         (
#             code_pattern,
#             """
#         `this is
#          not code`
#          """,
#         ),
#     ],
# )
# def test_newline_inline_patterns(pattern, text):
#     assert not re.search(pattern, text)


# r"(^|[^`])(`{1,2})(?P<contents>[^\n]+?)\2(?!`)"


# @pytest.mark.parametrize(
#     ("pattern", "text", "contents"),
#     [
#         (header_pattern, "# Header", "Header"),
#         (emph_pattern, "*italic*", "italic"),
#         (strong_pattern, "**bold**", "bold"),
#         (code_pattern, "`code`", "code"),
#         (strong_pattern, "***bolditalic***", "*bolditalic*"),
#     ],
# )
# def test_groups(pattern, text, contents):
#     match = re.search(pattern, text)
#     assert match.group("contents") == contents
