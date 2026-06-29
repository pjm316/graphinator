"""Math utilities: expression evaluation, domain refinement, real value computation."""

from tokenize import TokenError

import numpy as np
from sympy import Abs, E, lambdify, log, parse_expr, real_root
from sympy import S, SympifyError, limit
from sympy.calculus.util import continuous_domain

from shared import LOCAL_DICT, TRANSFORMS, X, normalize_absolute_value_notation

USER_EXPRESSION_ERRORS = (
    ArithmeticError,
    SyntaxError,
    TokenError,
    TypeError,
    ValueError,
    SympifyError,
)


def _use_real_roots_for_odd_rational_powers(expr):
    """Replace odd-root powers with real_root for proper handling."""

    def is_odd_rational_power(node):
        return (
            node.is_Pow
            and node.exp.is_Rational
            and node.exp.q > 1
            and node.exp.q % 2 == 1
        )

    def real_power(node):
        return real_root(node.base, node.exp.q) ** node.exp.p

    return expr.replace(is_odd_rational_power, real_power)


def real_values(expr_text: str, symbol, values):
    """Evaluate a SymPy expression and return real finite values or NaN."""
    expr_text = normalize_absolute_value_notation(expr_text)
    try:
        expr = parse_expr(expr_text, local_dict=LOCAL_DICT, transformations=TRANSFORMS)
        expr = _use_real_roots_for_odd_rational_powers(expr)
        function = lambdify(symbol, expr, modules=["numpy"])
        with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
            raw = function(values)
        raw = np.broadcast_to(np.asarray(raw, dtype=complex), values.shape).copy()
    except USER_EXPRESSION_ERRORS as exc:
        raise ValueError("Invalid expression.") from exc
    real_result = np.where(np.isreal(raw), raw.real, np.nan).astype(float)
    real_result[~np.isfinite(real_result)] = np.nan
    return real_result


def _has_negative_infinite_limit(expr, symbol, boundary_x, *, domain_right):
    """Return True when the one-sided boundary limit is -infinity."""
    try:
        boundary_limit = limit(
            expr, symbol, boundary_x, dir="+" if domain_right else "-"
        )
    except Exception:
        return False
    return boundary_limit == S.NegativeInfinity


def refine_domain_boundaries(expr_text, symbol, x_vals, y_vals, y_bounds=None):
    """Use SymPy's domain analysis to find exact boundary points, then log-sample inward.

    Returns (x_vals, y_vals, anchor_mask). anchor_mask[i] is True for synthetic
    points inserted outside [y0,y1] so matplotlib can clip cleanly at the axes edge;
    callers must exempt those segments from jump-detection.
    """
    x0, x1 = x_vals[0], x_vals[-1]
    no_change = (x_vals, y_vals, np.zeros(len(x_vals), dtype=bool))

    try:
        _expr = parse_expr(
            normalize_absolute_value_notation(expr_text),
            local_dict=LOCAL_DICT,
            transformations=TRANSFORMS,
        )
        _expr = _use_real_roots_for_odd_rational_powers(_expr)
        domain = continuous_domain(_expr, symbol, S.Reals)
        fn = lambdify(symbol, _expr, modules=["numpy"])
    except Exception:
        return no_change

    def _eval(xs):
        with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
            raw = fn(xs)
        raw = np.broadcast_to(
            np.asarray(raw, dtype=complex), np.asarray(xs).shape
        ).copy()
        out = np.where(np.isreal(raw), raw.real, np.nan).astype(float)
        out[~np.isfinite(out)] = np.nan
        return out

    eps = 1e-6
    edges = []
    try:
        for pt in domain.boundary:
            try:
                bx = float(pt)
            except (TypeError, ValueError):
                continue
            if not x0 < bx < x1:
                continue
            left_in = bool(domain.contains(bx - eps))
            right_in = bool(domain.contains(bx + eps))
            if left_in != right_in:
                edges.append((bx, right_in))
    except Exception:
        return no_change

    if not edges:
        return no_change

    extra_x_parts, extra_y_parts, extra_anchor_parts = [], [], []

    for bx, domain_right in edges:
        if domain_right:
            span = min(bx + (x1 - bx) * 0.5, x1) - bx
            new_x = bx + np.logspace(-15, np.log10(span), 700) if span > 1e-14 else None
        else:
            span = bx - max(bx - (bx - x0) * 0.5, x0)
            new_x = bx - np.logspace(-15, np.log10(span), 700) if span > 1e-14 else None

        if new_x is None:
            continue
        new_x = new_x[(new_x >= x0) & (new_x <= x1)]
        new_y = _eval(new_x)
        new_anchor = np.zeros(len(new_x), dtype=bool)

        if y_bounds is not None:
            real_mask = ~np.isnan(new_y)
            if real_mask.any() and _has_negative_infinite_limit(
                _expr,
                symbol,
                bx,
                domain_right=domain_right,
            ):
                real_y = new_y[real_mask]
                if real_y.min() > y_bounds[0]:
                    av = y_bounds[0] - max(1.0, abs(y_bounds[0]) * 0.01)
                    if domain_right:
                        new_x = np.concatenate([new_x[:1], new_x])
                        new_y = np.concatenate([[av], new_y])
                        new_anchor = np.concatenate([[True], new_anchor])
                    else:
                        new_x = np.concatenate([new_x, new_x[-1:]])
                        new_y = np.concatenate([new_y, [av]])
                        new_anchor = np.concatenate([new_anchor, [True]])

        extra_x_parts.append(new_x)
        extra_y_parts.append(new_y)
        extra_anchor_parts.append(new_anchor)

    if not extra_x_parts:
        return no_change

    extra_x = np.concatenate(extra_x_parts)
    extra_y = np.concatenate(extra_y_parts)
    extra_anchor = np.concatenate(extra_anchor_parts)
    all_x = np.concatenate([x_vals, extra_x])
    all_y = np.concatenate([y_vals, extra_y])
    all_anchor = np.concatenate([np.zeros(len(x_vals), dtype=bool), extra_anchor])
    order = np.argsort(all_x, kind="stable")
    return all_x[order], all_y[order], all_anchor[order]
