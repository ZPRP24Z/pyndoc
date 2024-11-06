import re
import pyndoc.ast as ast


class Reader:
    def __init__(self, lang: str):
        self._lang = lang
        self._blocks = []

    def read(self, filename: str) -> str:
        with open(filename, "r") as fp:
            contents = fp.readlines()
        return contents

    def parse(self, contents: str):
        patterns = ast.declare_gfm()
        for n, pattern in enumerate(patterns.values()[0]):
            matches = re.finditer(pattern, contents)
            for match in matches:
                block = patterns.keys[n]()
                self._blocks.push((block, block.span()))
                self.parse(match.group("contents"))
