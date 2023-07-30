
def func_print(str):
    print(str)

class Interpreter:
    # Standard library
    stdlib = { 'print': func_print }
    
    # Variables
    vars = {}

    def i_expr(self, expr):
        match expr[0]:
            case 'number':
                return expr[1]
            case 'binop':
                binops = {
                    '+': lambda x, y: x + y,
                    '-': lambda x, y: x - y,
                    '*': lambda x, y: x * y,
                    '/': lambda x, y: x / y
                }

                return binops[expr[1]](self.i_expr(expr[2]), self.i_expr(expr[3]))
            case 'name':
                print(self.vars.get(expr[1]))
                return self.vars.get(expr[1])
            case 'unary':
                if expr[1] == '+':
                    return self.i_expr(expr[2])
                elif expr[1] == '-':
                    return -self.i_expr(expr[2])
            case 'grouped':
                return self.i_expr(expr[1])

    
    def i_varargs(self, varargs):
        # return map(lambda x: self.i_expr(x), varargs)
        return [ self.i_expr(x) for x in varargs ]

    def i_assig(self, assig):
        print(assig[1])
        self.vars[assig[1]] = self.i_expr(assig[2])

    def i_funcc(self, funcc):
        func = self.stdlib[funcc[1]]
        if func is None:
            raise f"Unknown function '{funcc[1]}'"
        func(*self.i_varargs(funcc[2]))

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