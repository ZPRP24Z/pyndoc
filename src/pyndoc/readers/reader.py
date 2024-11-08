import importlib
import re

class Reader:
    def __init__(self, lang: str):
        self._lang = lang
        self._blocks = []
        self._lang_module = importlib.import_module(f"pyndoc.ast.{self._lang}.declare", "declare")

    def read(self, filename: str) -> str:
        with open(filename, "r") as fp:
            contents = fp.read()
        return contents

    # TODO: ADD SPAN CHECKS HERE, SO BLOCKS DONT GET CHECKED TWICE!
    def parse(self, contents: str):
        """
        parse a document, turn all reader objects to functions
        """
        # get all regex matches with their parse functions
        patterns = self._lang_module.declare()

        for pattern in patterns.keys():
            matches = re.finditer(pattern, contents)

            for match in matches:
                block = patterns[pattern]()
                # parse blocks
                content = block.parse(match)
                self._blocks.append([block, match.span()])
                if content:
                    self.parse(match.group("contents"))
                else:
                    break
