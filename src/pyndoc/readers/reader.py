import importlib


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

    def _process_atom_block(self, token: str):
        """
        process an atom block (Str, Space etc.)
        """
        print(f"PROCESSING ATOM BLOCK: {token}")
        if not self._context:
            return

        atom_block = [
            atom_block
            for atom_block in self._atom_block_types
            if atom_block.match_pattern(token)
        ]
        if not atom_block:
            return
        args = tuple([token]) if atom_block[0].block_has_content() else ()
        print(f"PROCESSED, ADDING {atom_block[0]} to {self._context[-1]}")
        self._context[-1].insert(atom_block[0](*args))

    def _check_end(self):
        """
        check if the current context block has ended
        """
        if len(self._context):
            end_match = self._context[-1].end(self._token)
            if not end_match:
                return
            print(
                f"FOUND END: \n\ttoken: {self._token}\n\tcontext: {self._context[-1]}\n\t"
            )

            # process token before the block-end
            self._process_atom_block(self._token[: end_match.start()])
            self._token = ""

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
            start_match, new_token = block.start(self._token)
            if not start_match:
                continue
            print(
                f"FOUND START: \n\ttoken: {self._token}\n\tblock: {block}\n\t new_token: {new_token}"
            )
            self._process_atom_block(self._token[: start_match.start()])
            self._token = new_token

            self._context.append(block(start_match))
            print(f"ADDED, CURRENT CONTEXT: {self._context}")

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
