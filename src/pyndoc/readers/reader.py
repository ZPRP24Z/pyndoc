import importlib
import re
import pyndoc.ast.blocks as ast

class Reader():
    def __init__(self, lang: str):
        self._tree = []
        self._context = []
        self._token = ''

        lang_module = importlib.import_module(f"pyndoc.ast.{lang}.tokens")
        self._block_types = lang_module.starts().keys()

        lang_module.assign_patterns()

    def _process_atom_block(self):
        """
        Process an atom block (Str, Space, etc.)
        """
        blocks = ast.decompose_text(self._token)

        if self._context:
            self._context[-1].contents.contents.extend(blocks)
        else:
            self._tree.extend(blocks)

        self._token = ''

    def _check_end(self):
        """
        Check if the current context block has ended
        """
        if not self._context:
            return

        if self._context[-1]:
            end_match = self._context[-1].end(self._token)
            if not end_match:
                return

            self._token = self._token[:end_match.start()]
            self._process_atom_block()

            self._tree.append(self._context.pop())

    def _check_start(self):
        """
        Check if a new block has just started.
        If so, set the current context as the block
        """
        for block in self._block_types:
            start_match = block.start(self._token)

    def process(self, char: str):
        """
        Process a single character
        """
        self._token += char
        self._check_end()

    def read(self, filename: str) -> str:
        with open(filename, "r") as fp:
            contents = fp.read()
        for char in contents:
            self.process(char)
        return contents