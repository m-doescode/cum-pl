
def func_print(str):
    print(str)

def func_sqrt(sq):
    return sq**0.5

class Interpreter:
    # Standard library
    stdlib = { 'print': func_print, 'sqrt': func_sqrt }
    
    # Variables
    vars = {}

    def i_expr(self, expr):
        match expr[0]:
            case 'number':
                return expr[1]
            case 'string':
                return expr[1]
            case 'name':
                return self.vars.get(expr[1])
            case 'binop':
                binops = {
                    '+': lambda x, y: x + y,
                    '-': lambda x, y: x - y,
                    '*': lambda x, y: x * y,
                    '/': lambda x, y: x / y
                }

                return binops[expr[1]](self.i_expr(expr[2]), self.i_expr(expr[3]))
            case 'uminus':
                return -self.i_expr(expr[2])
            case 'grouped':
                return self.i_expr(expr[1])
            case 'functioncall':
                return self.i_funcc(expr)

    
    def i_varargs(self, varargs):
        # return map(lambda x: self.i_expr(x), varargs)
        return [ self.i_expr(x) for x in varargs ]

    def i_assig(self, assig):
        self.vars[assig[1]] = self.i_expr(assig[2])

    def i_funcc(self, funcc):
        func = self.stdlib.get(funcc[1])
        if func is None:
            raise LookupError(f"Unknown function '{funcc[1]}'")
        return func(*self.i_varargs(funcc[2]))

    def i_stat(self, stat):
        if stat[0] == 'assignment':
            self.i_assig(stat)
        elif stat[0] == 'functioncall':
            self.i_funcc(stat)
        else:
            raise f"Unimplemented statement type '{stat[0]}'"

    def i_block(self, block):
        for stat in block[1]:
            self.i_stat(stat)

def interpret(ast):
    if ast[0] == 'block':
        interp = Interpreter()
        interp.i_block(ast)