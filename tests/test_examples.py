from pathlib import Path

from rune.parser import parse_program

EXAMPLES_DIR = Path(__file__).resolve().parent.parent / "docs" / "language" / "examples"


def _example_files():
    return sorted(EXAMPLES_DIR.rglob("*.rn"))


def test_examples_directory_is_not_empty():
    assert _example_files(), "no .rn example programs found"


def test_every_example_still_parses():
    for path in _example_files():
        program = path.read_text()
        parse_program(program)
