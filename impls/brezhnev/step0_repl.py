def READ(s):
    return s

def EVAL(s):
    return s

def PRINT(s):
    return s

def rep(s):
    t = READ(s)
    u = EVAL(t)
    v = PRINT(u)
    return v

while True:
    s = input("user> ")
    v = rep(s)
    print(v)
