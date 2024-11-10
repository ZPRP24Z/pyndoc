from pyndoc.readers.reader import Reader


def test_reader_init():
    rd = Reader("gfm")
    assert len(rd._block_types) == 4
