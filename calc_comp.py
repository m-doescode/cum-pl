
class Compiler():
    locals = {}
    constants = []
    instructions = []
    next_register = 0

    def __init__(self):
        self.locals = {}
        self.constants = []
        self.instructions = []
        self.next_register = 0

    def write_instructions(self, f):
        f.write(".section CONSTANTS:\n")
        pad = len(str(len(self.constants)-1))
        for i, k in enumerate(self.constants):
            f.write(f"\t{str(i).ljust(pad,' ')}: {repr(k)}\n")
        
        f.write("\n")

        f.write(".section INSTRUCTIONS:\n")
        for inst in self.instructions:
            f.write(f"\t{str(inst[0]).ljust(5,' ')} " + ' '.join([str(p).ljust(3,' ') for p in inst[1:]]) + "\n")
        
        f.write("\n.end")

    def push_const(self, value):
        self.constants.append(value)
        return len(self.constants)-1
    
    def load_const(self, const):
        try:
            ki = self.constants.index(const)
        except ValueError:
            ki = self.push_const(const)
        reg = self.next_register
        self.next_register += 1
        self.instructions.append(('loadk', reg, ki))
        return reg

    # Returns the index/address of the register containing the result of the expression
    def c_expr(self, expr):
        match expr[0]:
            case 'number':
                return self.load_const(expr[1])
            case 'string':
                return self.load_const(expr[1])
            case 'name':
                try:
                    return self.locals[expr[1]]
                except KeyError:
                    raise LookupError(f"Undefined local variable '{expr[1]}'")
            case 'binop':
                binops = {'+': 'sum', '-': 'sub', '*': 'mult', '/': 'div'}
                reg = self.next_register
                self.next_register += 1
                self.instructions.append((binops[expr[1]], reg, self.c_expr(expr[2]), self.c_expr(expr[3])))
                return reg
                # return binops[expr[1]](self.i_expr(expr[2]), self.i_expr(expr[3]))
            case 'uminus':
                reg = self.next_register
                self.next_register += 1
                self.instructions.append(('uminus', self.c_expr(expr[1]), reg))
                return reg
            case 'grouped':
                return self.c_expr(expr[1])
            case 'functioncall':
                return self.c_funcc(expr)

    def copy(self, rfrom):
        reg = self.next_register
        self.next_register += 1
        self.instructions.append(('mov', reg, rfrom))
        return reg
    
    def c_varargs(self, varargs):
        # return map(lambda x: self.i_expr(x), varargs)
        # return [ self.i_expr(x) for x in varargs ]
        # List of registers (may not be sequential due to in-between instructions) used by arguments
        regs = []
        for x in varargs:
            regs.append(self.c_expr(x))
        
        # https://stackoverflow.com/a/33575259/16255372
        # Avoid copying if registers are already undirtied
        if sorted(regs) == list(range(min(regs), max(regs)+1)):
            return regs[0], len(varargs)
        
        arg0 = self.next_register
        for reg in regs:
            self.copy(reg)
        return arg0, len(varargs)

    def c_assig(self, assig):
        try:
            reg = self.locals[assig[1]]
        except KeyError:
            reg = self.next_register
            self.next_register += 1
            self.locals[assig[1]] = reg
        self.instructions.append(('mov', reg, self.c_expr(assig[2])))

    def c_funcc(self, funcc):
        name = self.load_const(funcc[1])
        reg = self.next_register
        self.next_register += 1
        arg0, arg1 = self.c_varargs(funcc[2])
        self.instructions.append(('call', reg, name, arg0, arg1))
        return reg


    def c_stat(self, stat):
        if stat[0] == 'assignment':
            self.c_assig(stat)
        elif stat[0] == 'functioncall':
            self.c_funcc(stat)
        else:
            raise f"Unimplemented statement type '{stat[0]}'"

    def c_block(self, block):
        for stat in block[1]:
            self.c_stat(stat)

def compile(ast):
    if ast[0] == 'block':
        compiler = Compiler()
        compiler.c_block(ast)

        with open('compout.txt','w') as f:
            compiler.write_instructions(f)