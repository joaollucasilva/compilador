from ast import *


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return ('EOF', '')

    def peek_type(self):
        return self.current()[0]

    def peek_value(self):
        return self.current()[1]

    def consume_keyword(self, name):
        # aceita token tipo próprio (IF/PRINT/ELSE) ou ID com o texto da keyword
        if self.peek_type() == name.upper():
            return self.match(name.upper())
        if self.peek_type() == 'ID' and self.peek_value() == name:
            return self.match('ID')
        raise SyntaxError(f"Esperado {name} mas encontrado {self.current()}")

    def match(self, expected_type):
        if self.peek_type() == expected_type:
            val = self.current()[1]
            self.pos += 1
            return val
        return None

    def expect(self, expected_type):
        val = self.match(expected_type)
        if val is None:
            raise SyntaxError(f"Esperado {expected_type} mas encontrado {self.current()}")
        return val

    # Expressions with precedence
    def parse_program(self):
        stmts = []
        while self.peek_type() != 'EOF':
            stmts.append(self.parse_statement())
        return Block(stmts)

    def parse_statement(self):
        t = self.peek_type()
        # Handle keywords that lexer may emit as ID
        if t == 'ID':
            val = self.peek_value()
            if val == 'if':
                return self.parse_if()
            if val == 'print':
                return self.parse_print()
            if val == 'else':
                # 'else' alone is invalid here
                raise SyntaxError('else inesperado')
            # could be assignment
            if (self.pos + 1) < len(self.tokens) and self.tokens[self.pos + 1][0] == 'ASSIGN':
                return self.parse_assignment()
            raise SyntaxError('ID sem atribuição não suportado')

        if t == 'PRINT':
            return self.parse_print()

        if t == 'IF':
            return self.parse_if()

        if t == 'LBRACE':
            return self.parse_block()

        raise SyntaxError(f"Statement inesperado: {self.current()}")

    def parse_assignment(self):
        name = self.expect('ID')
        self.expect('ASSIGN')
        expr = self.parse_expression()
        self.expect('SEMICOLON')
        return Assign(name, expr)

    def parse_print(self):
        self.consume_keyword('print')
        self.expect('LPAREN')
        expr = self.parse_expression()
        self.expect('RPAREN')
        self.expect('SEMICOLON')
        return Print(expr)

    def parse_if(self):
        self.consume_keyword('if')
        self.expect('LPAREN')
        cond = self.parse_expression()
        self.expect('RPAREN')
        then_branch = self.parse_block()
        else_branch = None
        # aceitar 'ELSE' ou ID 'else'
        if (self.peek_type() == 'ELSE') or (self.peek_type() == 'ID' and self.peek_value() == 'else'):
            # consumir a keyword
            if self.peek_type() == 'ELSE':
                self.match('ELSE')
            else:
                self.match('ID')
            # else must ser um bloco
            else_branch = self.parse_block()
        return IfElse(cond, then_branch, else_branch)

    def parse_block(self):
        self.expect('LBRACE')
        stmts = []
        while self.peek_type() != 'RBRACE':
            if self.peek_type() == 'EOF':
                raise SyntaxError('Bloco não fechado')
            stmts.append(self.parse_statement())
        self.expect('RBRACE')
        return Block(stmts)

    def parse_expression(self):
        return self.parse_comparison()

    def parse_comparison(self):
        node = self.parse_term()
        while self.peek_type() == 'OP' and self.current()[1] in ('==', '!=', '<', '<=', '>', '>='):
            op = self.match('OP')
            right = self.parse_term()
            node = BinOp(node, op, right)
        return node

    def parse_term(self):
        node = self.parse_factor()
        while self.peek_type() == 'OP' and self.current()[1] in ('+', '-'):
            op = self.match('OP')
            right = self.parse_factor()
            node = BinOp(node, op, right)
        return node

    def parse_factor(self):
        node = self.parse_unary()
        while self.peek_type() == 'OP' and self.current()[1] in ('*', '/', '%'):
            op = self.match('OP')
            right = self.parse_unary()
            node = BinOp(node, op, right)
        return node

    def parse_unary(self):
        if self.peek_type() == 'OP' and self.current()[1] in ('+', '-'):
            op = self.match('OP')
            node = self.parse_unary()
            if op == '-':
                return BinOp(Number(0), '-', node)
            else:
                return node
        return self.parse_atom()

    def parse_atom(self):
        t = self.peek_type()
        if t == 'NUMBER':
            val = self.match('NUMBER')
            return Number(val)
        if t == 'ID':
            name = self.match('ID')
            return Var(name)
        if t == 'LPAREN':
            self.match('LPAREN')
            node = self.parse_expression()
            self.expect('RPAREN')
            return node
        raise SyntaxError(f"Átomo inesperado: {self.current()}")

