from ast import Number, Var, BinOp, Assign, Print, IfElse, Block
import operator

# Map operator symbols to safe Python functions
_BINOP_MAP = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
    '%': operator.mod,
    '==': operator.eq,
    '!=': operator.ne,
    '<': operator.lt,
    '<=': operator.le,
    '>': operator.gt,
    '>=': operator.ge,
    'and': lambda a, b: bool(a) and bool(b),
    'or': lambda a, b: bool(a) or bool(b),
}


def eval_expr(node, symbols):
    """Avalia expressões da AST de forma segura (sem usar eval).

    Retorna int/float/bool conforme a expressão.
    Levanta NameError ou ZeroDivisionError conforme apropriado.
    """
    if isinstance(node, Number):
        return node.value

    if isinstance(node, Var):
        return symbols.get(node.name)

    if isinstance(node, BinOp):
        left = eval_expr(node.left, symbols)
        right = eval_expr(node.right, symbols)
        op = node.op

        if op == '/' and right == 0:
            raise ZeroDivisionError('Divisão por zero')

        func = _BINOP_MAP.get(op)
        if func is None:
            # se for um operador inesperado, tente suportar operadores de símbolo único
            raise ValueError(f"Operador desconhecido: {op}")

        return func(left, right)

    # Caso não reconhecido
    raise TypeError(f"Nó de expressão desconhecido: {type(node).__name__}")


def exec_stmt(node, symbols):
    if isinstance(node, Assign):
        value = eval_expr(node.expr, symbols)
        symbols.define(node.name, value)

    elif isinstance(node, Print):
        print(eval_expr(node.expr, symbols))

    elif isinstance(node, IfElse):
        cond = eval_expr(node.cond, symbols)
        branch = node.then_branch if cond else node.else_branch
        # branch pode ser None (else opcional) — apenas não faz nada nesse caso
        if branch is None:
            return
        exec_block(branch, symbols)

    else:
        raise TypeError(f"Nó de statement desconhecido: {type(node).__name__}")


def exec_block(block, symbols):
    if block is None:
        return

    if not isinstance(block, Block):
        raise TypeError('exec_block espera um Block')

    for stmt in block.statements:
        exec_stmt(stmt, symbols)
