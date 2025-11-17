import re

TOKEN_REGEX = [
    ('NUMBER',   r'\d+'),
    ('ID',       r'[a-zA-Z_]\w*'),
    ('ASSIGN',   r'='),
    ('OP',       r'[+\-*/<>!]=|[+\-*/<>]'),
    ('LPAREN',   r'\('),
    ('RPAREN',   r'\)'),
    ('LBRACE',   r'\{'),
    ('RBRACE',   r'\}'),
    ('SEMICOLON',r';'),
    ('IF',       r'if'),
    ('ELSE',     r'else'),
    ('PRINT',    r'print'),
    ('WHITESPACE', r'\s+'),
]

def tokenize(code):
    tokens = []
    while code:
        for token_type, pattern in TOKEN_REGEX:
            regex = re.compile(pattern)
            match = regex.match(code)
            if match:
                if token_type != 'WHITESPACE':
                    tokens.append((token_type, match.group(0)))
                code = code[match.end():]
                break
        else:
            raise SyntaxError(f"Token inválido: {code}")
    return tokens
