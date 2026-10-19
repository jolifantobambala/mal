from shared import *

def pr_str(data):
    match data:
        case Symbol(name):
            return name
        case int(x):
            return f"{x}"
        case list(vv):
            return "(" + " ".join(pr_str(v) for v in vv) + ")"
        case _:
            raise TypeError(f"unexpected type ({type(data)}) passed to pr_str")
