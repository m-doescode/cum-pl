# FROM https://github.com/dabeaz/sly

# -----------------------------------------------------------------------------
# calc.py
# -----------------------------------------------------------------------------

from sly import Lexer, Parser

class CalcLexer(Lexer):
    tokens = { NAME, NUMBER, PLUS, TIMES, MINUS, DIVIDE, EQUALS, LPAREN, RPAREN, SEMICOLON, COMMA }
    ignore = ' \t'

    # Tokens
    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    NUMBER = r'\d+'

    # Special symbols
    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'
    EQUALS = r'='
    LPAREN = r'\('
    RPAREN = r'\)'
    SEMICOLON = r';'
    COMMA = r','

    # Ignored pattern
    ignore_newline = r'\n+'

    # Extra action for newlines
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1

class CalcParser(Parser):
    tokens = CalcLexer.tokens

    def __init__(self):
        self.names = { }

    # @_('NAME ASSIGN expr')
    # def statement(self, p):
    #     self.names[p.NAME] = p.expr

    @_('block')
    def script(self, p):
        return p.block
    
    @_('{ statement SEMICOLON }')
    def block(self, p):
        stats = [stat for stat, _ in p[0]]
        return ('block', stats)
    
    @_('assignment')
    def statement(self, p):
        return p[0]
    
    @_('function_call')
    def statement(self, p):
        return p[0]

    @_('NAME EQUALS expr')
    def assignment(self, p):
        return ('assignment', p.NAME, p.expr)
    
    @_('expr { COMMA expr }')
    def varargs(self, p):
        args = [p.expr0] + [expr for _, expr in p[1]]
        return args

    @_('LPAREN varargs RPAREN')
    def funcargs(self, p):
        return p.varargs

    @_('NAME funcargs')
    def function_call(self, p):
        return ('functioncall', p.NAME, p.funcargs)

    @_('function_call')
    def expr(self, p):
        return p.function_call

    @_('term { PLUS|MINUS term }')
    def expr(self, p):
        lval = p.term0
        for op, rval in p[1]:
            lval = ('binop', op, lval, rval)
        return lval

    @_('factor { TIMES|DIVIDE factor }')
    def term(self, p):
        lval = p.factor0
        for op, rval in p[1]:
            lval = ('binop', op, lval, rval)
        return lval

    @_('MINUS factor')
    def factor(self, p):
        return ('uminus', p.factor)

    @_('LPAREN expr RPAREN')
    def factor(self, p):
        return p.expr

    @_('NUMBER')
    def factor(self, p):
        return ('number', int(p.NUMBER))

    @_('NAME')
    def factor(self, p):
        return ('name', p.NAME)

# script = \
# """
# y = 1 + 2 * 3 + 4;
# x = y + y * y;
# print(x - y);
# print(sqrt(64));
# """

script = \
"""
print(sqrt(64));
"""

import calc_interp

if __name__ == '__main__':
    lexer = CalcLexer()
    parser = CalcParser()

    ast = parser.parse(lexer.tokenize(script))
    print(ast)
    calc_interp.interpret(ast)