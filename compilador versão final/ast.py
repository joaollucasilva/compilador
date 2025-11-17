class ASTNode: pass

class Number(ASTNode):
    def __init__(self, value): self.value = int(value)

class Var(ASTNode):
    def __init__(self, name): self.name = name

class BinOp(ASTNode):
    def __init__(self, left, op, right): self.left, self.op, self.right = left, op, right

class Assign(ASTNode):
    def __init__(self, name, expr): self.name, self.expr = name, expr

class Print(ASTNode):
    def __init__(self, expr): self.expr = expr

class IfElse(ASTNode):
    def __init__(self, cond, then_branch, else_branch): self.cond, self.then_branch, self.else_branch = cond, then_branch, else_branch

class Block(ASTNode):
    def __init__(self, statements): self.statements = statements
