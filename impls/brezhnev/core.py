import operator

from printer import pr_str

def _enforce_list(x):
    if type(x) is not list:
        raise TypeError(f"{repr(x)} ({type(x).__name__}) is not a list")

def _enforce_same_type(a, b):
    ta = type(a)
    tb = type(b)
    if ta is not tb:
        raise TypeError(f"{repr(a)} ({ta.__name__}) is not of the same type as {repr(b)} ({tb.__name__})")

def _enforce_numbers(a, b):
    ta = type(a)
    tb = type(b)
    if not (ta is int and tb is int):
        raise TypeError(f"{repr(a)} ({ta.__name__}) and {repr(b)} ({tb.__name__}) are not both numbers")
    
def prn(x):
    print(pr_str(x))

def _list(*args):
    return list(args)

def listp(x):
    return type(x) is list

def empty(x):
    _enforce_list(x)
    return not bool(x)

def count(x):
    _enforce_list(x)
    return len(x)

def eql(a, b):
    t = type(a)
    if t is not type(b):
        return False
    if t is list:
        if len(a) != len(b):
            return False
        return all(eql(xa, xb) for xa, xb in zip(a, b))
    return a == b

def lt(a, b):
    _enforce_numbers(a, b)
    return a < b

def lte(a, b):
    _enforce_numbers(a, b)
    return a <= b

def gt(a, b):
    _enforce_numbers(a, b)
    return a > b

def gte(a, b):
    _enforce_numbers(a, b)
    return a >= b

ns = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.floordiv,
    "prn": prn,
    "list": _list,
    "list?": listp,
    "empty?": empty,
    "count": count,
    "=": eql,
    "<": lt,
    "<=": lte,
    ">": gt,
    ">=": gte,
}
