from calc_parser import CalcLexer, CalcParser
import calc_interp
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
    print("\n === Test 1: Parse === ")
    lexer = CalcLexer()
    parser = CalcParser()

    ast = parser.parse(lexer.tokenize(script))
    print(ast)

    print("\n === Test 2: Interpret === ")
    calc_interp.interpret(ast)

    print("\n === Test 3: Compile === ")
    calc_comp.compile(ast)
    print("Compiled output to compout.txt")

    print("\n === Test 4: VM === ")
    compiler = calc_comp.Compiler()
    compiler.c_block(ast)
    calc_vm.run(compiler.constants, compiler.instructions)
