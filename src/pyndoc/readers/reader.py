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

    def within_span(self, span_match: tuple, span_block: tuple[int, int]):
        return span_block[0] <= span_match[0] and span_match[1] <= span_block[1]


    # TODO: ADD SPAN CHECKS HERE, SO BLOCKS DONT GET CHECKED TWICE!
    def parse(self, contents: str, span_offset: int = 0):
        """
        parse a document, turn all reader objects to functions
        """
        # get all regex matches with their parse functions
        patterns = self._lang_module.declare()

        for pattern in patterns.keys():
            matches = re.finditer(pattern, contents)
            for match in matches:
                print("matching ", match.string, ": ", patterns[pattern])
                # calculate offset span
                span = tuple(original_span + span_offset for original_span in match.span())
                already_checked = [el[1] for el in self._blocks if self.within_span(span, el[1])]
                if already_checked:
                    print("this was already checked! continuing")
                    continue
                block = patterns[pattern]()
                # parse blocks
                content = block.parse(match)
                if content:
                    self.parse(match.group("contents"), match.start("contents"))
                else:
                    self._blocks.append([block, span])
                    break
                self._blocks.append([block, span])
