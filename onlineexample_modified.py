# -----------------------------------------------------------------------------
# example.py
#
# Example of using PLY To parse the following simple grammar.
#
#   expression : term PLUS term
#              | term MINUS term
#              | term
#
#   term       : factor TIMES factor
#              | factor DIVIDE factor
#              | factor
#
#   factor     : NUMBER
#              | NAME
#              | PLUS factor
#              | MINUS factor
#              | LPAREN expression RPAREN
#
# -----------------------------------------------------------------------------

from ply.lex import lex
from ply.yacc import yacc

# --- Tokenizer

# All tokens must be named in advance.
tokens = ( 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'LPAREN', 'RPAREN',
           'NAME', 'NUMBER', 'EQUALS', 'SEMICOLON', 'COMMA' )

# Ignored characters
t_ignore = ' \t'

# Token matching rules are written as regexs
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_EQUALS = r'\='
t_SEMICOLON = r';'
t_COMMA = r','

# A function can be used if there is an associated action.
# Write the matching regex in the docstring.
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Ignored token with an action associated with it
def t_ignore_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')

# Error handler for illegal characters
def t_error(t):
    print(f'Illegal character {t.value[0]!r}')
    t.lexer.skip(1)

# Build the lexer object
lexer = lex()
    
# --- Parser

def p_block(p):
    '''
    block : block statement SEMICOLON
          | statement SEMICOLON
    '''
    if p[1][0] == 'block':
        p[0] = ('block', p[1][1] + [p[2]])
    else:
        p[0] = ('block', [p[1]])
    
def p_varargs(p):
    '''
    varargs : varargs COMMA expression
            | expression
    '''
    if p[1][0] == 'varargs':
        p[0] = ('varargs', p[1][1] + [p[3]])
    else:
        p[0] = ('varargs', [p[1]])

def p_functionargs(p):
    '''
    functionargs : LPAREN varargs RPAREN
    '''
    p[0] = ('functionargs', p[2][1])

def p_functioncall(p):
    '''
    functioncall : NAME functionargs
    '''
    p[0] = ('functioncall', p[1], p[2][1])

def p_statement(p):
    '''
    statement : assignment
              | functioncall
    '''
    p[0] = p[1]

def p_assignment(p):
    '''
    assignment : NAME EQUALS expression
    '''
    p[0] = ('assignment', p[1], p[3])

# Write functions for each grammar rule which is
# specified in the docstring.
def p_expression(p):
    '''
    expression : term PLUS term
               | term MINUS term
    '''
    # p is a sequence that represents rule contents.
    #
    # expression : term PLUS term
    #   p[0]     : p[1] p[2] p[3]
    # 
    p[0] = ('binop', p[2], p[1], p[3])

def p_expression_term(p):
    '''
    expression : term
    '''
    p[0] = p[1]

def p_term(p):
    '''
    term : factor TIMES factor
         | factor DIVIDE factor
    '''
    p[0] = ('binop', p[2], p[1], p[3])

def p_term_factor(p):
    '''
    term : factor
    '''
    p[0] = p[1]

def p_factor_number(p):
    '''
    factor : NUMBER
    '''
    p[0] = ('number', p[1])

def p_factor_name(p):
    '''
    factor : NAME
    '''
    p[0] = ('name', p[1])

def p_factor_unary(p):
    '''
    factor : PLUS factor
           | MINUS factor
    '''
    p[0] = ('unary', p[1], p[2])

def p_factor_grouped(p):
    '''
    factor : LPAREN expression RPAREN
    '''
    p[0] = ('grouped', p[2])

def p_error(p):
    print(f'Syntax error at {p.value!r}')

# Build the parser
parser = yacc()

# Parse an expression
# ast = parser.parse('2 * 3 + 4 * (5 - x)')
# y = 12 + (-56) * 234 + (6 * 7);
ast = parser.parse(
"""
y = 12 + (56) * 234 + 5;
x = y + y * y;
print(x - y);
""")

print(ast)

import calc_interp

# calc_interp.interpret(ast)