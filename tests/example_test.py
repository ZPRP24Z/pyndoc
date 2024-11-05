from pyndoc.ExampleClass import ExampleClass


def test_example_class():
    value = 4
    example_instance = ExampleClass(value)

    assert example_instance.num == value


def test_always_passes():
    assert True
