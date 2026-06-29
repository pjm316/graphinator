"""Number line expression parsing: convert user text into geometric forms."""

import re
from tokenize import TokenError

from sympy import And, Or, S, SympifyError
from sympy.parsing.sympy_parser import parse_expr
from sympy.solvers.inequalities import solve_univariate_inequality

from shared import LOCAL_DICT, TRANSFORMS, X, normalize_absolute_value_notation

PARSE_ERRORS = (SyntaxError, TokenError, TypeError, ValueError, SympifyError)


def normalize_boolean_relations(text: str) -> str:
    """Convert 'or'/'and' to '|'/'&' and wrap operands in parens."""
    text = re.sub(r"\s+or\s+", " | ", text, flags=re.IGNORECASE)
    text = re.sub(r"\s+and\s+", " & ", text, flags=re.IGNORECASE)
    tokens = re.split(r"([|&])", text)
    if len(tokens) == 1:
        return text
    wrapped = []
    for token in tokens:
        if token in {"|", "&"}:
            wrapped.append(token)
            continue
        segment = token.strip()
        if re.search(r"<=|>=|<|>|=", segment):
            if not (segment.startswith("(") and segment.endswith(")")):
                segment = f"({segment})"
        wrapped.append(segment)
    return " ".join(wrapped)


def _parse_simple_expression(text: str):
    """Try regex-based parsing for common patterns before sympy."""
    m = re.match(
        r"^(.+?)\s*(<=|>=|<|>|=)\s*x\s*(<=|>=|<|>|=)\s*(.+)$", text, re.IGNORECASE
    )
    if m:
        try:
            lhs, op1, op2, rhs = m.groups()
            lv, rv = float(lhs), float(rhs)
            li, ri = "=" in op1, "=" in op2
            if ">" in op1:
                lv, rv, li, ri = rv, lv, ri, li
            return {"type": "segment", "left": (lv, li), "right": (rv, ri)}
        except ValueError:
            return None
    m = re.match(r"^x\s*(<=|>=|<|>|=)\s*(.+)$", text, re.IGNORECASE)
    if m:
        try:
            op, rhs = m.groups()
            value = float(rhs)
            return {
                "type": "ray",
                "bound": (value, "=" in op),
                "direction": "right" if ">" in op else "left",
            }
        except ValueError:
            return None
    return None


def _interval_to_parsed(interval):
    """Convert SymPy Interval to parsed form."""
    if interval.is_empty:
        return None
    if interval.start is S.NegativeInfinity and interval.end is S.Infinity:
        return None
    lv, rv = interval.start, interval.end
    li, ri = not interval.left_open, not interval.right_open
    if lv is S.NegativeInfinity:
        return {"type": "ray", "bound": (float(rv), ri), "direction": "left"}
    if rv is S.Infinity:
        return {"type": "ray", "bound": (float(lv), li), "direction": "right"}
    return {"type": "segment", "left": (float(lv), li), "right": (float(rv), ri)}


def _set_to_parsed(set_expr):
    """Convert SymPy set to parsed form."""
    if set_expr.is_Interval:
        return _interval_to_parsed(set_expr)
    if set_expr.is_Union:
        parts = []
        for arg in set_expr.args:
            parsed = _set_to_parsed(arg)
            if parsed is None:
                return None
            if parsed["type"] == "union":
                parts.extend(parsed["parts"])
            else:
                parts.append(parsed)
        return {"type": "union", "parts": parts}
    if set_expr.is_FiniteSet and len(set_expr) == 1:
        return {"type": "point", "value": float(next(iter(set_expr)))}
    return None


def _solution_set(expr):
    """Solve expression to get solution set."""
    if expr.is_Relational:
        solution = solve_univariate_inequality(expr, X)
        try:
            return solution.as_set()
        except Exception:
            return None
    if expr.func is And:
        return _combine_solution_sets(expr.args, "intersect")
    if expr.func is Or:
        return _combine_solution_sets(expr.args, "union")
    return None


def _combine_solution_sets(args, operation):
    """Combine multiple solution sets via intersect or union."""
    sets = [_solution_set(arg) for arg in args]
    if any(s is None for s in sets):
        return None
    result = sets[0]
    for s in sets[1:]:
        result = getattr(result, operation)(s)
    return result


def _parse_with_sympy(text: str):
    """Use SymPy to parse complex expressions."""
    try:
        expr = parse_expr(text, local_dict=LOCAL_DICT, transformations=TRANSFORMS)
    except PARSE_ERRORS:
        return None
    set_expr = _solution_set(expr)
    if set_expr is None:
        return None
    return _set_to_parsed(set_expr)


def parse_nl(text):
    """Parse a number line expression into ray, segment, or union form."""
    text = text.strip().replace("≥", ">=").replace("≤", "<=").replace("−", "-")
    text = normalize_absolute_value_notation(text)
    text = normalize_boolean_relations(text)
    parsed = _parse_simple_expression(text)
    if parsed is not None:
        return parsed
    return _parse_with_sympy(text)
