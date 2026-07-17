from rune.lexer import tokenize
from rune.model import Count, Explore, Group, Objective, Order, Take, TransformationGraph

# What each step looks like, keyed by its opening keyword. Used only for
# error messages -- the parsing itself stays in _parse_line.
_STEP_FORMS = {
    "GROUP": "GROUP <source> BY <key>",
    "COUNT": "COUNT EACH <noun>",
    "ORDER": "ORDER BY <key> [ASC|DESC]",
    "TAKE": "TAKE <count>",
    "EXPLORE": "EXPLORE <source> FROM <start> [TO <target>]",
    "MAXIMIZE": "MAXIMIZE SUM OVER CONTIGUOUS <source>",
    "MINIMIZE": "MINIMIZE SUM OVER CONTIGUOUS <source>",
}


def _parse_line(tokens):
    # Each branch validates the step's exact shape before building it.
    # Trailing tokens, wrong inner keywords, and wrong arity are rejected --
    # a line either matches the documented form or it does not parse. Silent
    # tolerance would let a malformed proposal through verification.
    head = tokens[0]
    if head.value == "TAKE":
        # tokens: TAKE <count>
        if len(tokens) != 2 or tokens[1].kind != "NUMBER":
            raise ValueError("malformed TAKE")
        return Take(count=int(tokens[1].value))
    if head.value == "COUNT":
        # tokens: COUNT EACH <noun>
        if len(tokens) != 3 or tokens[1].value != "EACH":
            raise ValueError("malformed COUNT")
        return Count(noun=tokens[2].value)
    if head.value == "ORDER":
        # tokens: ORDER BY <key> [ASC|DESC]
        if len(tokens) not in (3, 4) or tokens[1].value != "BY":
            raise ValueError("malformed ORDER")
        if len(tokens) == 4 and tokens[3].value not in ("ASC", "DESC"):
            raise ValueError("malformed ORDER direction")
        return Order(key=tokens[2].value, descending=len(tokens) == 4 and tokens[3].value == "DESC")
    if head.value == "GROUP":
        # tokens: GROUP <source> BY <key>
        if len(tokens) != 4 or tokens[2].value != "BY":
            raise ValueError("malformed GROUP")
        return Group(source=tokens[1].value, key=tokens[3].value)
    if head.value == "EXPLORE":
        # tokens: EXPLORE <source> FROM <start> [TO <target>]
        if len(tokens) not in (4, 6) or tokens[2].value != "FROM":
            raise ValueError("malformed EXPLORE")
        if len(tokens) == 6 and tokens[4].value != "TO":
            raise ValueError("malformed EXPLORE")
        target = tokens[5].value if len(tokens) == 6 else None
        return Explore(source=tokens[1].value, start=tokens[3].value, target=target)
    if head.value in ("MAXIMIZE", "MINIMIZE"):
        # tokens: MAXIMIZE|MINIMIZE SUM OVER CONTIGUOUS <source>
        if (
            len(tokens) != 5
            or tokens[1].value != "SUM"
            or tokens[2].value != "OVER"
            or tokens[3].value != "CONTIGUOUS"
        ):
            raise ValueError("malformed objective")
        return Objective(
            direction=head.value.lower(),
            measure=tokens[1].value.lower(),
            scope=tokens[3].value.lower(),
            source=tokens[4].value,
        )
    raise ValueError(f"unrecognized step starting with {head.value!r}")


def parse_program(program: str) -> TransformationGraph:
    steps = []
    for number, line in enumerate(program.splitlines(), start=1):
        if not line.strip():
            continue
        tokens = tokenize(line)
        head = tokens[0].value
        if head not in _STEP_FORMS:
            raise ValueError(
                f"line {number}: unrecognized step {head!r} -- every step starts "
                f"with one of {', '.join(sorted(_STEP_FORMS))}"
            )
        try:
            steps.append(_parse_line(tokens))
        except (IndexError, ValueError):
            raise ValueError(
                f"line {number}: could not parse {line.strip()!r} -- "
                f"expected {_STEP_FORMS[head]}"
            ) from None
    return TransformationGraph(steps=steps)
