from printer import pr_str
from reader import read_str

def READ(s):
    return read_str(s)

def EVAL(s):
    return s

def PRINT(s):
    return pr_str(s)

def rep(s):
    try:
        t = READ(s)
    except Exception as e:
        return str(e)
    u = EVAL(t)
    v = PRINT(u)
    return v

while True:
    s = input("user> ")
    v = rep(s)
    print(v)
