from lang.lexer import tokenize_program
from lang.model import Take, TransformationGraph


def _parse_line(tokens):
    head = tokens[0]
    if head.value == "TAKE":
        return Take(count=int(tokens[1].value))
    raise ValueError(f"unrecognized step starting with {head.value!r}")


def parse_program(program: str) -> TransformationGraph:
    steps = [_parse_line(line) for line in tokenize_program(program)]
    return TransformationGraph(steps=steps)
