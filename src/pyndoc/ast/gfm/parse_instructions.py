import re

import pyndoc.ast.blocks as ast


class Header(ast.Header):
    def __init__(self, match: re.Match):
        super().__init__(len(match.group("h")))

class Emph(ast.Emph):
    def __init__(self, _=None):
        super().__init__()

    @classmethod
    def start(cls, token: str) -> tuple[re.Match | None, str]:
        match = re.search(cls.start_pattern, token)
        token = token[-1:] if match else token
        return (match, token)
