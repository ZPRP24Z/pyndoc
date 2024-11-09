import re

import pyndoc.ast.blocks as ast

class Header(ast.Header):
    def __init__(self, match: re.Match):
        super().__init__(len(match.group('h')))
