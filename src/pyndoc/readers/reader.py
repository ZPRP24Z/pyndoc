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
        self._atom_block_types = lang_module.atomic_patterns().keys()

        lang_module.assign_patterns()

    def _check_atom_block(self):
        for atom_block in self._atom_block_types:
            if not atom_block.match_pattern(self._token) and atom_block.match_pattern(
                self._token[:-1]
            ):
                self._process_atom_block()

    def _process_atom_block(self):
        """
        process an atom block (Str, Space etc.)
        """
        if not self._context:
            return

        atom_blocks = ast.decompose_text(self._token[:-1])
        self._token = self._token[-1:]

        for atom_block in atom_blocks:
            self._context[-1].insert(atom_block)

    def _check_end(self):
        """
        check if the current context block has ended
        """
        if len(self._context):
            end_match = self._context[-1].end(self._token)
            if not end_match:
                return

            # process token before the block-end
            self._token = self._token[: end_match.start()]
            self._process_atom_block()

            # block is processed, move it to finished tree
            if len(self._context) > 1:
                item = self._context.pop()
                self._context[-1].insert(item)
            else:
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

            self._context.append(block(start_match))

    def process(self, char: str):
        """
        Process a current token
        taking into consideration the current context tree, check if
        a new block has started or ended, process atom blocks
        """
        self._token += char
        self._check_end()
        self._check_start()
        self._check_atom_block()

    def read(self, filename: str):
        """
        Open and read a file one character at a time,
        then pass the character to tokenizer
        """
        with open(filename, "r") as fp:
            while True:
                char = fp.read(1)
                if not char:
                    break

                self.process(char)
