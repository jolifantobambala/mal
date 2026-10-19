from shared import Symbol

class Env:
    def __init__(self, outer, binds=None, exprs=None):
        self.outer = outer
        self.data = {}
        if binds:
            for key, expr in zip(binds, exprs):
                self.set(key, expr)

    def set(self, key: Symbol, v):
        self.data[key.name] = v

    def get(self, key: Symbol):
        if (v := self.data.get(key.name, None)) is not None:
            return v
        if self.outer:
            return self.outer.get(key)
        raise KeyError(f"symbol '{key.name}' not found")

    
