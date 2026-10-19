import re

from shared import *

RX = re.compile(r"[\s,]*(~@|[\[\]{}()'`~^@]|\"(?:\\.|[^\\\"])*\"?|;.*|[^\s\[\]{}('\"`,;)]*)")

class Reader:
    def __init__(self, tokens):
        self.tokens = tokens
        self.ptr = 0

    def peek(self):
        return self.tokens[self.ptr]

    def next(self):
        t = self.tokens[self.ptr]
        self.ptr += 1
        return t

    def read_list(self):
        lst = []
        self.next()  # discard (
        while True:
            t = self.peek()
            if t == ")":
                self.next()  # discard )
                break
            try:
                f = self.read_form()
            except IndexError:
                raise IndexError("premature end of input")
            lst.append(f)
        return lst

    def read_atom(self):
        t = self.next()
        try:
            return int(t)
        except ValueError:
            pass

        match t:
            case "nil":
                return None
            case "true":
                return True
            case "false":
                return False
            case _:
                return Symbol(t)
    
    def read_form(self):
        t = self.peek()
        match t[0]:
            case "(":
                return self.read_list()
            case _:
                return self.read_atom()

def tokenize(s):
    return RX.findall(s)

def read_str(s):
    toks = tokenize(s)
    r = Reader(toks)
    return r.read_form()
