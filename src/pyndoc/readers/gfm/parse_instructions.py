import re

import pyndoc.ast.blocks as ast


class Header(ast.Header):
    def __init__(self, **kwargs):
        if "match" not in kwargs:
            level = 1
        else:
            level = len(kwargs["match"].group("h"))
        super().__init__(level=level)


class Emph(ast.Emph):
    def __init__(self, **_):
        super().__init__()

    @classmethod
    def start(cls, **kwargs) -> tuple[re.Match | None, str]:
        if "token" not in kwargs:
            return None, ""
        token = kwargs["token"]
        match = re.search(cls.start_pattern, token)
        token = token[-1:] if match else token
        return (match, token)
