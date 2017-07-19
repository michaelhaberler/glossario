
from lib_example import lib_example_a
from lib_example.lib_example_a import B as BE

A = lib_example_a.instance_of_a

def test_A():
    a = lib_example_a.A("test_A")
    assert a.name == "test_A"

def test_BE():
    be = BE('be')

class TestCase(object):

    def __init__(self):
        self.a = lib_example_a.A("TestCase")
        self.b = A
