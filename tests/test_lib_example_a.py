
from lib_example import lib_example_a


def test_A():
    a = lib_example_a.A("test_A")
    assert a.name == "test_A"
