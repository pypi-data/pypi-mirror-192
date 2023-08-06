import sympy
import math

def ratio_test(expr):
    try:
        expr = sympy.sympify(expr)
        x = sympy.Symbol('x')
        limit = sympy.limit(abs(expr.subs(x, x+1)/expr), x, sympy.oo)
        if limit < 1:
            return 'Convergent'
        elif limit > 1:
            return 'Divergent'
        else:
            return 'Inconclusive'
    except:
        return 'Inconclusive'


def integral_test(expr):
    try:
        expr = sympy.sympify(expr)
        x = sympy.Symbol('x')
        if sympy.integrate(expr, (x, 1, sympy.oo)).is_finite:
            return 'Convergent'
        else:
            return 'Divergent'
    except:
        return 'Inconclusive'


def nth_term_test(expr):
    try:
        expr = sympy.sympify(expr)
        n = sympy.Symbol('n')
        a_n = expr.subs(n, n+1)/expr
        if sympy.limit(a_n, n, sympy.oo) == 0:
            return 'Convergent'
        else:
            return 'Divergent'
    except:
        return 'Inconclusive'


def p_series_test(expr):
    try:
        expr = sympy.sympify(expr)
        x = sympy.Symbol('x')
        p = sympy.Wild('p')
        if expr.match(1/x):
            return 'Divergent'
        elif expr.match(1/x**p) and sympy.re(p) > 1:
            return 'Convergent'
        else:
            return 'Divergent'
    except:
        return 'Inconclusive'


def alternating_series_test(expr):
    try:
        expr = sympy.sympify(expr)
        x = sympy.Symbol('x')
        a_n = expr.subs('n', x)
        if sympy.limit(a_n, x, sympy.oo) != 0:
            return 'Divergent'
        if not sympy.is_decreasing(abs(a_n)):
            return 'Inconclusive'
        return 'Convergent'
    except:
        return 'Inconclusive'


def check_convergence(expr):
    try:
        if isinstance(expr, str):
            expr = sympy.sympify(expr)
        else:
            raise ValueError("Expression must be a string")

        if ratio_test(expr) == 'Convergent':
            return 'Convergent by the Ratio Test'

        if integral_test(expr) == 'Convergent':
            return 'Convergent by the Integral Test'

        if nth_term_test(expr) == 'Convergent':
            return 'Convergent by the Nth Term Test'

        if p_series_test(expr) == 'Convergent':
            return 'Convergent by the P-Series Test'

        if alternating_series_test(expr) == 'Convergent':
            return 'Convergent by the Alternating Series Test'

        return 'Divergent'

    except:
        return 'Inconclusive'


