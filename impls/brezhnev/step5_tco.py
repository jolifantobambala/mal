import operator
from ast import literal_eval
from itertools import batched
from typing import cast

from core import ns
from env import Env
from function import Function
from printer import pr_str
from reader import read_str
from shared import Symbol

repl_env = Env(None)
for k, fn in ns.items():
    repl_env.set(Symbol(k), fn)

def READ(s):
    return read_str(s)

def EVAL(ast, env):
    while True:
        match ast:
            case Symbol():
                return env.get(ast)
            case list(vv):
                if not vv:
                    return []
                car = cast(Symbol, vv[0])
                match car.name:
                    case "def!":
                        evald = EVAL(vv[2], env)
                        env.set(vv[1], evald)
                        return evald
                    case "let*":
                        binding_list, body = vv[1], vv[2]
                        nenv = Env(env)
                        for sym_name, binding_ast in batched(binding_list, 2):
                            nenv.set(sym_name, EVAL(binding_ast, nenv))
                        ast, env = body, nenv
                        continue
                    case "do":
                        butlast_evald = [EVAL(v, env) for v in vv[1: -1]]
                        ast = vv[-1]
                        continue
                    case "if":
                        cond, body_t = vv[1], vv[2]
                        body_f = vv[3] if len(vv) > 3 else None
                        cond_evald = EVAL(cond, env)
                        if cond_evald is not None and cond_evald != False:
                            ast = body_t
                            continue
                        if body_f is not None:
                            ast = body_f
                            continue
                        return None
                    case "fn*":
                        def _new_fn(*args):
                            nenv = Env(env, vv[1], args)
                            return EVAL(vv[2], nenv)
                        return Function(vv[2], vv[1], env, _new_fn)
                    case _:
                        evald = [EVAL(v, env) for v in vv]
                        f = evald[0]
                        match f:
                            case Function(fn_ast, params, fn_env, fn):
                                ast = fn_ast
                                env = Env(fn_env, params, evald[1:])
                                continue
                            case f if callable(f):
                                return f(*evald[1:])
                            case _:
                                raise TypeError(f'{evald[0]} ({type(evald[0]).__name__}) is not a function')                        
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
