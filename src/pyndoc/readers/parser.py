import importlib


class Parser:
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
        self.context = []
        self.token = ""

        lang_module = importlib.import_module(f"pyndoc.readers.{lang}.tokens")
        self._block_types = lang_module.declared_tokens.keys()
        self._atom_block_types = lang_module.declared_atomic_patterns.keys()
        self._atom_wrapper_block = lang_module.atom_wrapper

        lang_module.assign_patterns()

    def check_atom_block(self) -> None:
        """
        Check if an atom block has ended.
        That is, if matching it with a next character results in None (but previously matched)
        """

        for atom_block in self._atom_block_types:
            match_cur, self.token = atom_block.match_pattern(text=self.token, context=self.context)
            match_prev, _ = atom_block.match_pattern(text=self.token[:-1], context=self.context)
            if not match_cur and match_prev:
                old_token, self.token = self.token[:-1], self.token[-1:]
                self._process_atom_block(old_token)

    def _process_atom_block(self, token: str) -> None:
        """
        process an atom block (Str, Space etc.)
        """

        atom_block = [
            atom_block
            for atom_block in self._atom_block_types
            if atom_block.match_pattern(text=token, context=self.context)[0]
        ]
        if not atom_block:
            return
        if not self.context:
            self.context.append(self._atom_wrapper_block())

        args = tuple([token]) if atom_block[0].block_has_content() else ()
        self.context[-1].insert(atom_block[0](*args))

    def check_end(self) -> None:
        """
        check if the current context block has ended
        """
        if len(self.context):
            end_match, new_token = self.context[-1].end(
                token=self.token, context=self.context
            )
        else:
            end_match, new_token = self._atom_wrapper_block.end(
                token=self.token, context=self.context
            )
        if not end_match:
            return

        # process token before the block-end
        self._process_atom_block(self.token[: end_match.start()])
        self.token = new_token

        self._end()

    def _end(self) -> None:
        # block is processed, move it to finished tree
        if len(self.context) > 1:
            item = self.context.pop()
            self.context[-1].insert(item)
        else:
            self._tree.append(self.context.pop())

    def check_start(self) -> None:
        """
        Check if a new block has just started.
        If so, set the current context as the block
        """
        for block in self._block_types:
            start_match, new_token = block.start(token=self.token, context=self.context)
            if not start_match:
                self.token = new_token
                continue
            if block.is_inline() and not self.context:
                self.context.append(self._atom_wrapper_block())
            else:
                self._process_atom_block(self.token[: start_match.start()])
            self.token = new_token

            self.context.append(block())
            self.context[-1].process_read(match=start_match, context=self.context)
            break

    def close_context(self) -> None:
        while self.context:
            if self.token:
                self.token = self.context[-1].handle_premature_closure(self.token)
            self.process_trailing_atom()
            self._end()

    def process_trailing_atom(self) -> None:
        self._process_atom_block(self.token)
        self.token = ""
