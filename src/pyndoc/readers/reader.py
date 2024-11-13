import importlib


class Reader:
    """
    Class representing a general reader for all input languages
    Fields:
        * tree - representing the tree into which the blocks will be processed
        * context - stack-like representation of currently processed blocks
        * token - currently processed token
        * block_types - types of composite blocks found in a given language
        * atom_block_types - atom blocks found in a give language
    """

    def __init__(self, lang: str) -> None:
        self._tree = []
        self._context = []
        self._token = ""

        lang_module = importlib.import_module(f"pyndoc.readers.{lang}.tokens")
        self._block_types = lang_module.declared_tokens.keys()
        self._atom_block_types = lang_module.declared_atomic_patterns.keys()
        self._atom_wrapper_block = lang_module.atom_wrapper

        lang_module.assign_patterns()

    def _check_atom_block(self) -> None:
        """
        Check if an atom block has ended.
        That is, if matching it with a next character results in None (but previously matched)
        """
        for atom_block in self._atom_block_types:
            if not atom_block.match_pattern(self._token) and atom_block.match_pattern(
                self._token[:-1]
            ):
                old_token, self._token = self._token[:-1], self._token[-1:]
                self._process_atom_block(old_token)

    def _process_atom_block(self, token: str) -> None:
        """
        process an atom block (Str, Space etc.)
        """
        print(f"PROCESSING ATOM BLOCK: {token}")

        atom_block = [
            atom_block
            for atom_block in self._atom_block_types
            if atom_block.match_pattern(token)
        ]
        if not atom_block:
            return
        if not self._context:
            self._context.append(self._atom_wrapper_block())

        args = tuple([token]) if atom_block[0].block_has_content() else ()
        print(f"PROCESSED, ADDING {atom_block[0]} to {self._context[-1]}")
        self._context[-1].insert(atom_block[0](*args))

    def _check_end(self) -> None:
        """
        check if the current context block has ended
        """
        if len(self._context):
            end_match = self._context[-1].end(token=self._token)
        else:
            end_match = self._atom_wrapper_block.end(token=self._token)
        if not end_match:
            return

        # process token before the block-end
        self._process_atom_block(self._token[: end_match.start()])
        self._token = ""

        self._end()

    def _end(self) -> None:
        # block is processed, move it to finished tree
        if len(self._context) > 1:
            item = self._context.pop()
            self._context[-1].insert(item)
        else:
            self._tree.append(self._context.pop())

    def _check_start(self) -> None:
        """
        Check if a new block has just started.
        If so, set the current context as the block
        """
        for block in self._block_types:
            start_match, new_token = block.start(
                token=self._token, context=self._context
            )
            if not start_match:
                continue
            print(
                f"FOUND START: \n\ttoken: {self._token}\n\tblock: {block}\n\t new_token: {new_token}"
            )
            if block.is_inline() and not self._context:
                self._context.append(self._atom_wrapper_block())
            else:
                self._process_atom_block(self._token[: start_match.start()])
            self._token = new_token

            self._context.append(block())
            self._context[-1].process_read(match=start_match)
            print(f"ADDED, CURRENT CONTEXT: {self._context}")
            break

    def _close_context(self) -> None:
        while self._context:
            self._process_trailing_atom()
            self._end()

    def _process_trailing_atom(self) -> None:
        self._process_atom_block(self._token)
        self._token = ""

    def process(self, char: str) -> None:
        """
        Process a current token
        taking into consideration the current context tree, check if
        a new block has started or ended, process atom blocks
        """
        self._token += char
        self._check_end()
        self._check_start()
        self._check_atom_block()

    def read(self, filename: str) -> None:
        """
        Open and read a file one character at a time,
        then pass the character to tokenizer
        """
        with open(filename, "r") as fp:
            while True:
                char = fp.read(1)
                if not char:
                    print("EOF!")
                    if not self._context:
                        self._process_trailing_atom()
                    self._close_context()
                    break

                self.process(char)
