import importlib
import re
import pyndoc.ast.blocks as ast


class Reader:
    def __init__(self, lang: str):
        self._tree = []
        self._context = []
        self._token = ""

        lang_module = importlib.import_module(f"pyndoc.ast.{lang}.tokens")
        self._block_types = lang_module.starts().keys()

        lang_module.assign_patterns()

    # TODO: FINISH THIS!
    def _process_atom_block(self):
        """
        process an atom block (Str, Space etc.)
        """
        pass

    def _check_end(self):
        """
        check if the current context block has ended
        """
        if self._context[-1]:
            end_match = self._context[-1].end(self._token)
            if not end_match:
                return

            # process token before the block-end
            self._token = self._token[: end_match.start()]
            self._process_atom_block()

            # block is processed, move it to finished tree
            self._tree.append(self._context.pop())

    def _check_start(self):
        """
        Check if a new block has just started.
        If so, set the current context as the block
        """
        for block in self._block_types:
            start_match = block.start(self._token)
            if not start_match:
                continue
            self._token = self._token[: start_match.start()]
            self._process_atom_block()

            self._context = block(start_match)

    def process(self, char: str):
        """
        Process a current token
        taking into consideration the current context tree, check if
        a new block has started or ended, process atom blocks
        """
        self._token += char
        self._check_end()

    def read(self, filename: str):
        """
        Open and read a file one character at a time,
        then pass the character to tokenizer
        """
        with open(filename, "r") as fp:
            contents = fp.read()
        for char in contents:
            self.process(char)
        return contents
