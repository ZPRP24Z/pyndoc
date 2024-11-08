from pyndoc.readers.reader import Reader

rd = Reader

def test_reader_init():
    reader = Reader("gfm")
    assert reader._lang == "gfm"
    assert not reader._blocks

def test_reader_header():
    reader = Reader("gfm")
    reader.parse("# test")
    assert len(reader._blocks) == 1
    assert reader._blocks[0][0].contents.metadata == [1]

def test_reader_header_higherlevel():
    reader = Reader("gfm")
    reader.parse("### test")
    assert len(reader._blocks) == 1
    assert reader._blocks[0][0].contents.metadata == [3]

def test_italic():
    reader = Reader("gfm")
    reader.parse("*italic text*")
    assert len(reader._blocks) == 1

def test_multiple_items_bolditalic():
    reader = Reader("gfm")
    reader.parse("## Header **bold that holds *italic***")
    assert len(reader._blocks) == 3

def test_multiple_items_itabold():
    reader = Reader("gfm")
    reader.parse("## Header *italic that holds **bold***")
    assert len(reader._blocks) == 3
