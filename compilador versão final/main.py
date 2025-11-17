from lexer import tokenize
from parser import Parser
from semantic import SymbolTable
from interpreter import exec_block

with open("exemplo.txt") as f:
    code = f.read()

tokens = tokenize(code)
parser = Parser(tokens)
ast = parser.parse_program()
exec_block(ast, SymbolTable())
