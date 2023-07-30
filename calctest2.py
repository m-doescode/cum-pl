# FROM https://github.com/dabeaz/sly

# -----------------------------------------------------------------------------
# calc.py
# -----------------------------------------------------------------------------

from sly import Lexer, Parser

class CalcLexer(Lexer):
    tokens = { NAME, NUMBER, PLUS, TIMES, MINUS, DIVIDE, ASSIGN, LPAREN, RPAREN }
    ignore = ' \t'

    # Tokens
    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    NUMBER = r'\d+'

    # Special symbols
    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'
    ASSIGN = r'='
    LPAREN = r'\('
    RPAREN = r'\)'

    # Ignored pattern
    ignore_newline = r'\n+'

    # Extra action for newlines
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1

from pprint import pprint

class CalcParser(Parser):
    tokens = CalcLexer.tokens

    def __init__(self):
        self.names = { }

    # @_('NAME ASSIGN expr')
    # def statement(self, p):
    #     self.names[p.NAME] = p.expr

    @_('expr')
    def statement(self, p):
        pprint(p.expr)

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

if __name__ == '__main__':
    lexer = CalcLexer()
    parser = CalcParser()
    while True:
        try:
            text = input('calc > ')
        except EOFError:
            break
        if text:
            parser.parse(lexer.tokenize(text))