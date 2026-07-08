from dataclasses import dataclass

KEYWORDS = {
    "GROUP", "BY", "COUNT", "EACH", "ORDER", "ASC", "DESC", "TAKE",
    "EXPLORE", "FROM", "TO",
}


@dataclass(frozen=True)
class Token:
    kind: str
    value: str


def tokenize(line: str):
    tokens = []
    for word in line.split():
        if word in KEYWORDS:
            tokens.append(Token("KEYWORD", word))
        elif word.isdigit():
            tokens.append(Token("NUMBER", word))
        else:
            tokens.append(Token("IDENT", word))
    return tokens


def tokenize_program(program: str):
    return [tokenize(line) for line in program.splitlines() if line.strip()]
