from calc_parser import CalcLexer, CalcParser
import calc_interp
import calc_comp
import calc_vm

script = \
"""
y = 1 + 2 * 3 + 4;
x = y + y * y;
print(x - y);
print(sqrt(64));
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
