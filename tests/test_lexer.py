from rune.lexer import Token, tokenize


def test_tokenizes_keyword_and_number():
    tokens = tokenize("TAKE 10")

    assert tokens == [Token("KEYWORD", "TAKE"), Token("NUMBER", "10")]


def test_tokenizes_group_by_line():
    tokens = tokenize("GROUP nums BY value")

    assert tokens == [
        Token("KEYWORD", "GROUP"),
        Token("IDENT", "nums"),
        Token("KEYWORD", "BY"),
        Token("IDENT", "value"),
    ]


def test_tokenizes_explore_from_to_line():
    tokens = tokenize("EXPLORE graph FROM a TO b")

    assert tokens == [
        Token("KEYWORD", "EXPLORE"),
        Token("IDENT", "graph"),
        Token("KEYWORD", "FROM"),
        Token("IDENT", "a"),
        Token("KEYWORD", "TO"),
        Token("IDENT", "b"),
    ]
