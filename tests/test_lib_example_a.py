
from lib_example import lib_example_a
from lib_example.lib_example_a import B as BE


def test_A():
    a = lib_example_a.A("test_A")
    assert a.name == "test_A"

def test_BE():
    be = BE('be')
