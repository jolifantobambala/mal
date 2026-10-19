import operator
from ast import literal_eval
from itertools import batched

from core import ns
from env import Env
from printer import pr_str
from reader import read_str
from shared import Symbol

repl_env = Env(None)
for k, fn in ns.items():
    repl_env.set(Symbol(k), fn)

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
                case Symbol("do"):
                    evald = [EVAL(v, env) for v in vv]
                    return evald[-1]
                case Symbol("if"):
                    cond, body_t = vv[1], vv[2]
                    body_f = vv[3] if len(vv) > 3 else None
                    cond_evald = EVAL(cond, env)
                    if cond_evald is not None and cond_evald != False:
                        return EVAL(body_t, env)
                    return EVAL(body_f, env) if body_f is not None else None
                case Symbol("fn*"):
                    def _new_fn(*args):
                        nenv = Env(env, vv[1], args)
                        return EVAL(vv[2], nenv)
                    return _new_fn
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
