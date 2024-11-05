from pyndoc.ExampleClass import ExampleClass
from pyndoc.reader import GenericReader


def test_example_class():
    value = 4
    example_instance = ExampleClass(value)

    assert example_instance.num == value


def test_always_passes():
    assert True

def test_empty_generic_reader():
    r = GenericReader("md")
    assert r._file_type == "md"

