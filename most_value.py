import sympy as sp


def func_maximum(func, var, interval):
    """
    只适用于连续函数，函数不含参数。
    必须保证最值存在。
    极值点个数必须是有穷的。

    func: 函数表达式（sympy 表达式）， 如 x^2+1,  y^3+1
    var: 自变量
    interval: 区间（可以是无穷区间）
    """
    assert var in func.free_symbols

    func_diff = sp.diff(func, var)
    xs = sp.solveset(func_diff, var, interval)
    x_y = {}
    if type(xs) is sp.FiniteSet:
        for x in xs:
            x_y[x] = func.subs(var, x)

    x_y[interval.left] = func.subs(var, interval.left)
    x_y[interval.right] = func.subs(var, interval.right)

    x_y = sorted(x_y.items(), key=lambda x: x[1], reverse=True)
    return x_y[0]


def func_minimum(func, var, interval):
    """
    只适用于连续函数，函数不含参数。
    必须保证最值存在。
    极值点个数必须是有穷的。

    func: 函数表达式（sympy 表达式）， 如 x^2+1,  y^3+1
    var: 自变量
    interval: 区间（可以是无穷区间）
    """
    assert var in func.free_symbols
    func_diff = sp.diff(func, var)
    xs = sp.solveset(func_diff, var, interval)
    x_y = {}
    if type(xs) is sp.FiniteSet:
        for x in xs:
            x_y[x] = func.subs(var, x)

    x_y[interval.left] = func.subs(var, interval.left)
    x_y[interval.right] = func.subs(var, interval.right)

    x_y = sorted(x_y.items(), key=lambda x:x[1])

    return x_y[0]


if __name__ == "__main__":
    x = sp.symbols('x', real=True)
    func = x + 1/x
    interval = sp.Interval(sp.Rational(1, 2), sp.Rational(3, 2))  # [0.5, 1.5]

    x1, y1 = func_maximum(func, x, interval)
    x2, y2 = func_minimum(func, x, interval)

    print(f"max: ({x1} , {y1})")
    print(f"min: ({x2} , {y2})")

