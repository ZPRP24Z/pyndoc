from pyndoc.readers.parser import Parser


class Reader:
    def __init__(self, lang: str) -> None:
        self._parser = Parser(lang)

    def process(self, char: str) -> None:
        """Process a current token
        taking into consideration the current context tree, check if
        a new block has started or ended, process atom blocks

        :param char: The currently processed character
        :type char: ``str``
        """
        self._parser.token += char
        self._parser.check_end()
        self._parser.check_start()
        self._parser.check_atom_block()

    def read(self, filename: str) -> None:
        """Open and read a file one character at a time,
        then pass the character to tokenizer
        """
        with open(filename, "r") as fp:
            while True:
                char = fp.read(1)
                if not char:
                    if not self._parser.context:
                        self._parser.process_trailing_atom()
                    self._parser.close_context()
                    break

                self.process(char)
