from function import Function
from shared import *

def pr_str(data):
    if type(data) is bool:
        return "true" if data else "false"
    
    match data:
        case Symbol(name):
            return name
        case int(x):
            return f"{x}"
        case list(vv):
            return "(" + " ".join(pr_str(v) for v in vv) + ")"
        case None:
            return "nil"
        case Function():
            return "#<function>"
        case data if callable(data):
            return "#<function>"
        case _:
            raise TypeError(f"unexpected type ({type(data)}) passed to pr_str")
