
from sphinxcontrib import glossario


def test_import_file():
    mod = glossario.import_file("tests/lib_example/lib_example_a.py")
    assert mod.__name__ == 'lib_example_a'


def test_get_imports():
    imports = list(glossario.get_imports("tests/lib_example/lib_example_b.py"))
    assert "lib_example_a" in [m for imp in imports for m in imp.name]
    assert "lib_example_c" in [m for imp in imports for m in imp.module]


def test_get_full_import_names():
    names = glossario.get_full_import_names("tests/test_glossario.py")
    assert names == ['glossario.glossario']


def test_get_full_used_names():
        names = glossario.get_full_used_names("tests/test_glossario.py")
