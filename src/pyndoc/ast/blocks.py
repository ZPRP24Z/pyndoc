from dataclasses import dataclass

@dataclass
class AstBlock:
    name: str
    contents: list=None


class Str(AstBlock):
    def __init__(self, contents: str=None):
        super().__init__("Str", contents)


class Space(AstBlock):
    def __init__(self):
        super().__init__("Space")
