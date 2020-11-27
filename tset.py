from sympy import *
from sympy.solvers.solveset import solveset_real


def test():
    scope = {}
    cmds = [ 'cnt = 0', 'for i in range(4):\n\tcnt+=i', 'print(cnt)' ]

    for cmd in cmds:
        exec(cmd, scope)

    print(scope['cnt'])

def test2():
    x, a = symbols('x a')
    print(diff(ln(x) + 1/2*a*x**2-a*x, x))

if __name__ == '__main__':
    # test2()
    operatorList = [
        ['=', '>=', '<=', '>', '<'],
        ['+', '-'],
        ['*', '/'],
        ['^', '_']
    ]

    print(operatorList.index(['+', '-']))
