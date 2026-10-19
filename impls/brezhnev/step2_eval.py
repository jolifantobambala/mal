import operator
from ast import literal_eval

from printer import pr_str
from reader import read_str
from shared import Symbol

repl_env = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.floordiv,
}

def READ(s):
    return read_str(s)

def EVAL(ast, repl_env):
    match ast:
        case Symbol(name):
            if (v := repl_env.get(name, None)) is not None:
                return v
            raise KeyError(f'unknown symbol "{name}"')
        case list(vv):
            if vv:
                evald = [EVAL(v, repl_env) for v in vv]
                return evald[0](*evald[1:])
            return []
        case _:
            return ast

def PRINT(s):
    return pr_str(s)

def rep(s):
    ast = READ(s)
    u = EVAL(ast, repl_env)
    v = PRINT(u)
    return v

while True:
    s = input("user> ")
    try:
        v = rep(s)
        print(v)
    except Exception as e:
        print(literal_eval(str(e)))
