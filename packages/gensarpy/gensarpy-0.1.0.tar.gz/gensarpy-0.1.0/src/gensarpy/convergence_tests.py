import sympy


def integral_test(expr):
    try:
        expr = sympy.sympify(expr)
        x = sympy.Symbol('x')
        integral = sympy.integrate(expr, (x, 1, sympy.oo))
        if integral.is_finite:
            return 'Convergent'
        else:
            return 'Divergent'
    except:
            raise ValueError
    

def nth_term_test(expr):
    try:
        expr = sympy.sympify(expr)
        x = sympy.Symbol('x')
        limit = sympy.limit(expr, x, sympy.oo)
        if limit != 0:
            return 'Divergent'
        else:
            return 'Inconclusive2'
    except:
        raise ValueError


def ratio_test(expr):
    try:
        expr = sympy.sympify(expr)
        x = sympy.Symbol('x')
        if sympy.simplify(expr) == 1/x:
            return 'Divergent'
        limit = sympy.limit(abs(expr.subs(x, (x + 1))/expr), x, sympy.oo)
        if limit < 1:
            return 'Convergent'
        elif limit > 1 or limit == sympy.oo: 
            return 'Divergent'
        else:
            return 'Inconclusive'
    except:
        raise ValueError
     

def check_convergence(expr):
    conv = 0
    div = 0
    try:
        if not isinstance(expr, str):
            raise ValueError("Expression must be a string")

        if ratio_test(expr) == 'Convergent':
            conv = conv + 1

        if ratio_test(expr) == 'Divergent':
            div = div + 1

        if integral_test(expr) == 'Convergent':
            conv = conv + 1

        if integral_test(expr) == 'Divergent':
            div = div + 1

        if nth_term_test(expr) == 'Convergent':
            conv = conv + 1
        
        if nth_term_test(expr) == 'Divergent':
            div = div + 1
         
        if div > conv:
            return 'Divergent'
        elif div == conv:
            return 'Something happened!'
        else:
            return 'Convergent'
    except:
        raise ValueError


def isconvergent(expr): 
    conv = 0
    div = 0
    try:
        if not isinstance(expr, str):
            raise ValueError("Expression must be a string")

        if ratio_test(expr) == 'Convergent':
            conv = conv + 1

        if ratio_test(expr) == 'Divergent':
            div = div + 1

        if integral_test(expr) == 'Convergent':
            conv = conv + 1

        if integral_test(expr) == 'Divergent':
            div = div + 1

        if nth_term_test(expr) == 'Convergent':
            conv = conv + 1
        
        if nth_term_test(expr) == 'Divergent':
            div = div + 1
         
        if div > conv:
            return False
        elif div == conv:
            return 'Something happened!'
        else:
            return True
    except:
        raise ValueError


def isdivergent(expr): 
    conv = 0
    div = 0
    try:
        if not isinstance(expr, str):
            raise ValueError("Expression must be a string")

        if ratio_test(expr) == 'Convergent':
            conv = conv + 1

        if ratio_test(expr) == 'Divergent':
            div = div + 1

        if integral_test(expr) == 'Convergent':
            conv = conv + 1

        if integral_test(expr) == 'Divergent':
            div = div + 1

        if nth_term_test(expr) == 'Convergent':
            conv = conv + 1
        
        if nth_term_test(expr) == 'Divergent':
            div = div + 1
         
        if div > conv:
            return True
        elif div == conv:
            return 'Something happened!'
        else:
            return False
    except:
        raise ValueError
          
