import importlib
from pyndoc.ast.ast_tree import ASTTree


class Parser:
    """Class representing a general reader for all input languages

    :param lang:
        The reader's language
    :type lang: ``str``
    """

    def __init__(self, lang: str) -> None:
        self._tree = ASTTree([])  #: The current AST Tree (blocks already read)
        self.context = []  #: The context stack
        self.token = ""  #: Token currently matched

        lang_module = importlib.import_module(f"pyndoc.readers.{lang}.tokens")
        self._block_types = (
            lang_module.declared_tokens.keys()
        )  #: Types of available composite blocks (declared by lang)
        self._atom_block_types = lang_module.declared_atomic_patterns.keys()  #: Atom block types (declared by lang)
        self._atom_wrapper_block = (
            lang_module.atom_wrapper
        )  #: The block in which atom blocks will be wrapped if no context is found

        lang_module.assign_patterns()

    def check_atom_block(self) -> None:
        """Check if an atom block has ended.
        That is, if matching it with a next character results in None (but previously matched)
        """

        for atom_block in self._atom_block_types:
            match_cur, self.token = atom_block.match_pattern(text=self.token, context=self.context)
            match_prev, _ = atom_block.match_pattern(text=self.token[:-1], context=self.context)

            if not match_cur and match_prev:
                old_token, self.token = self.token[:-1], self.token[-1:]
                self._process_atom_block(old_token)

    def _process_atom_block(self, token: str) -> None:
        """process an atom block (Str, Space etc.)

        :param token:
            The token to be processed
        :type token: ``str``
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
        """check if the current context block has ended"""
        if len(self.context):
            end_match, new_token = self.context[-1].end(token=self.token, context=self.context)
        else:
            end_match, new_token = self._atom_wrapper_block.end(token=self.token, context=self.context)
        if not end_match:
            return

        # process token before the block-end
        self._process_atom_block(self.token[: end_match.start()])
        self.token = new_token

        self._end()

    def _end(self) -> None:
        """Move a processed blocks to the finished tree"""
        if len(self.context) > 1:
            item = self.context.pop()
            self.context[-1].insert(item)
        elif self.context:
            self._tree.append(self.context.pop())

    def check_start(self) -> None:
        """Check if a new block has just started.
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
        """
        If the file has ended - go through each block in the context and end it
        """
        while self.context:
            self.token = self.context[-1].handle_premature_closure(token=self.token, context=self.context)
            self.process_trailing_atom()
            self._end()

    def process_trailing_atom(self) -> None:
        """
        Immediately process an atom block without checking for the usual condition
        """
        self._process_atom_block(self.token)
        self.token = ""
