# https://www.sigmdel.ca/michel/program/delphi/parser/parser1_en.html#:~:text=It%20is%20now%20very%20clear,(unary)%20%2B%20or%20%E2%88%92.


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
    
### STICKY KEYS (literally, ew gross)

def p_start(p):
    "start : expression"
    p[0] = p[1]

def p_expr1(p):
    '''
    expression : term
    '''
    p[0] = p[1]

def p_expr2(p):
    '''
    expression : term PLUS term
               | term MINUS term
    '''
    p[0] = ('binop', p[2], p[1], p[3])

def p_term1(p):
    '''
    term : factor
    '''
    p[0] = p[1]

def p_term2(p):
    '''
    term : factor TIMES factor
         | factor DIVIDE factor
    '''
    p[0] = ('binop', p[2], p[1], p[3])

def p_factor1(p):
    '''
    factor : NUMBER
    '''
    p[0] = p[1]

def p_factor2(p):
    '''
    factor : LPAREN expression RPAREN
    '''
    p[0] = p[2]

def p_factor3(p):
    '''
    factor : PLUS factor
           | MINUS factor
    '''
    p[0] = ('unary', p[1], p[2])

def p_error(p):
    print(f'Syntax error at {p.value!r}')

parser = yacc()

print(parser.parse('1 * 2 * 3'))