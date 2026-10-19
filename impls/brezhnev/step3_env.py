import operator
from ast import literal_eval
from itertools import batched

from env import Env
from printer import pr_str
from reader import read_str
from shared import Symbol

repl_env = Env(None)
repl_env.set(Symbol("+"), operator.add)
repl_env.set(Symbol("-"), operator.sub)
repl_env.set(Symbol("*"), operator.mul)
repl_env.set(Symbol("/"), operator.floordiv)

def READ(s):
    return read_str(s)

def EVAL(ast, env):
    match ast:
        case Symbol():
            return env.get(ast)
        case list(vv):
            if not vv:
                return []
            match vv[0]:
                case Symbol("def!"):
                    evald = EVAL(vv[2], env)
                    env.set(vv[1], evald)
                    return evald
                case Symbol("let*"):
                    binding_list, body = vv[1], vv[2]
                    nenv = Env(env)
                    for sym_name, binding_ast in batched(binding_list, 2):
                        nenv.set(sym_name, EVAL(binding_ast, nenv))
                    return EVAL(body, nenv)
                case _:
                    evald = [EVAL(v, env) for v in vv]
                    if not callable(evald[0]):
                        raise TypeError(f'{evald[0]} ({type(evald[0]).__name__}) is not a function')
                    return evald[0](*evald[1:])
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
        s = str(e)
        print(literal_eval(s) if s[0] == "'" else s)
