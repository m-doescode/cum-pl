from calc_parser import CalcLexer, CalcParser
import calc_comp
import calc_vm

script = \
"""

x1 = 2;
y1 = 5;
x2 = 10;
y2 = 12;

dist = sqrt((y2-y1)*(y2-y1)+(x2-x1)*(x2-x1));
print(dist);

"""

if __name__ == '__main__':
    lexer = CalcLexer()
    parser = CalcParser()

    print(":: Parsing...")

    ast = parser.parse(lexer.tokenize(script))
    print(ast)

    print("\n:: Compiling...")
    
    compiler = calc_comp.Compiler()
    compiler.c_block(ast)
    print(compiler.constants, compiler.instructions)
    calc_comp.write_bytecode(compiler, 'compbc')

    print("\n:: Reading...")


    k, i = calc_comp.read_bytecode('compbc')
    print(k, i)

    print("\n:: Running VM...")

    calc_vm.run(k, i)
