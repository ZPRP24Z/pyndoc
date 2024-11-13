import re

import pyndoc.ast.blocks as ast


class Header(ast.Header):
    def __init__(self) -> None:
        super().__init__()

    def process_read(self, **kwargs: re.Match) -> None:
        if "match" not in kwargs:
            level = 1
        else:
            match = kwargs["match"]
            level = len(match.group("h"))
        self.contents.metadata = [level]


class Emph(ast.Emph):
    def __init__(self, **_: None) -> None:
        super().__init__()

    @classmethod
    def start(cls, **kwargs: str) -> tuple[re.Match | None, str]:
        print("w gfm emph start")
        if "token" not in kwargs:
            return None, ""
        token = kwargs["token"]
        match = re.search(cls.start_pattern, token)
        token = token[-1:] if match else token
        return (match, token)

    @classmethod
    def handle_premature_closure(cls, token):
        return token[:-1] if token[-1] == "*" else token
