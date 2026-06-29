from number_line import parse_nl


def test_parse_number_line_algebraic_inequality():
    parsed = parse_nl("x + 1 > 3")

    assert parsed == {
        "type": "ray",
        "bound": (2.0, False),
        "direction": "right",
    }


def test_parse_number_line_or_expression():
    parsed = parse_nl("x < -3 or x > 3")

    assert parsed["type"] == "union"
    assert len(parsed["parts"]) == 2
    assert parsed["parts"][0]["type"] == "ray"
    assert parsed["parts"][1]["type"] == "ray"


def test_parse_number_line_and_expression():
    parsed = parse_nl("x > 1 and x < 5")

    assert parsed == {
        "type": "segment",
        "left": (1.0, False),
        "right": (5.0, False),
    }


def test_parse_number_line_absolute_value_union():
    parsed = parse_nl("|x| > 3")

    assert parsed["type"] == "union"
    assert len(parsed["parts"]) == 2
    assert parsed["parts"][0]["type"] == "ray"
    assert parsed["parts"][1]["type"] == "ray"


def test_parse_number_line_absolute_value_segment():
    parsed = parse_nl("|x| <= 3")

    assert parsed == {
        "type": "segment",
        "left": (-3.0, True),
        "right": (3.0, True),
    }


def test_parse_number_line_tokenizer_errors_return_none():
    assert parse_nl("x > 2'") is None


def test_parse_number_line_unmatched_parentheses_return_none():
    assert parse_nl("(x > 2") is None


def test_parse_number_line_invalid_compound_syntax_returns_none():
    assert parse_nl("x > and x < 4") is None
