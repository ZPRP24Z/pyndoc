class GenericReader:
    def __init__(self, filename: str = None):
        self._filename = filename

    def parse_line(self, text: str):
        pass

    def read(self):
        with open(self._filename, "r") as fp:
            lines = fp.readlines()
            parsed_text = [self.parse_line(line) for line in lines]
