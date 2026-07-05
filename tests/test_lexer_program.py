from lang.lexer import Token, tokenize_program


def test_tokenize_program_splits_into_per_line_token_lists():
    program = "GROUP nums BY value\nTAKE 10"

    lines = tokenize_program(program)

    assert lines == [
        [Token("KEYWORD", "GROUP"), Token("IDENT", "nums"), Token("KEYWORD", "BY"), Token("IDENT", "value")],
        [Token("KEYWORD", "TAKE"), Token("NUMBER", "10")],
    ]
