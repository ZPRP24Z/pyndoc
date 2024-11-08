from pyndoc.readers.reader import Reader

rd = Reader

def test_reader_init():
    reader = Reader("gfm")
    assert reader._lang == "gfm"
    assert not reader._blocks

def test_reader_header():
    reader = Reader("gfm")
    reader.parse("# test")
    print(reader._blocks)
    assert len(reader._blocks) == 1
    assert reader._blocks[0][0].contents.metadata == [1]

def test_reader_header_higherlevel():
    reader = Reader("gfm")
    reader.parse("### test")
    print(reader._blocks)
    assert len(reader._blocks) == 1
    assert reader._blocks[0][0].contents.metadata == [3]
