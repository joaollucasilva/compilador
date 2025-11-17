class SymbolTable:
    def __init__(self): self.table = {}

    def define(self, name, value): self.table[name] = value

    def get(self, name):
        if name in self.table: return self.table[name]
        raise NameError(f"Variável '{name}' não definida")
