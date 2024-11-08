import pyndoc.ast.blocks as ast
import re

class Header(ast.Header):
    def __init__(self):
        super().__init__()

    def parse(self, match: re.Match) -> str:
        level = len(match.group('h'))
        self.contents.metadata = [level]
        return match.group("contents")

