from rune.lexer import tokenize_program
from rune.model import Count, Explore, Group, Objective, Order, Take, TransformationGraph


def _parse_line(tokens):
    head = tokens[0]
    if head.value == "TAKE":
        return Take(count=int(tokens[1].value))
    if head.value == "COUNT":
        # tokens: COUNT EACH <noun>
        return Count(noun=tokens[2].value)
    if head.value == "ORDER":
        # tokens: ORDER BY <key> [ASC|DESC]
        key = tokens[2].value
        descending = len(tokens) > 3 and tokens[3].value == "DESC"
        return Order(key=key, descending=descending)
    if head.value == "GROUP":
        # tokens: GROUP <source> BY <key>
        return Group(source=tokens[1].value, key=tokens[3].value)
    if head.value == "EXPLORE":
        # tokens: EXPLORE <source> FROM <start> [TO <target>]
        target = tokens[5].value if len(tokens) > 4 else None
        return Explore(source=tokens[1].value, start=tokens[3].value, target=target)
    if head.value in ("MAXIMIZE", "MINIMIZE"):
        # tokens: MAXIMIZE|MINIMIZE <measure> OVER <scope> <source>
        return Objective(
            direction=head.value.lower(),
            measure=tokens[1].value.lower(),
            scope=tokens[3].value.lower(),
            source=tokens[4].value,
        )
    raise ValueError(f"unrecognized step starting with {head.value!r}")


def parse_program(program: str) -> TransformationGraph:
    steps = [_parse_line(line) for line in tokenize_program(program)]
    return TransformationGraph(steps=steps)
