import pyndoc.ast.blocks as ast
import re

class Header(ast.Header):
    def __init__(self):
        super().__init__()

    def parse(self, match: re.Match) -> str:
        level = len(match.group('h'))
        self.contents.metadata = [level]
        return match.group("contents")

# TODO: Change regex syntax so Emph and Strong get parsed here, modify tests accordingly
class Emph(ast.Emph):
    def __init__(self):
        super().__init__()

    def parse(self, match: re.Match) -> str:
        match_str = match.string
        match_str.strip('*', 1)
        return match_str

class Strong(ast.Strong):
    def __init__(self):
        super().__init__()

    def parse(self, match: re.Match) -> str:
        match_str = match.string
        match_str.strip('*', 2)
        return match_str

