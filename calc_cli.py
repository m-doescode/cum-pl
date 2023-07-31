from calc_parser import CalcLexer, CalcParser
import calc_interp
import calc_comp
import calc_vm

## Parsing arguments

from argparse import ArgumentParser

ap = ArgumentParser(prog="CUM-lang CLI",
                    description="Command-line interface for the CUM programming language. Can be used to interpret scripts, compile them, and run the compiled output.")

ap.add_argument('input', help="The input file to process.")
ap.add_argument('--output', help="Output")
action = ap.add_mutually_exclusive_group()
action.add_argument('--compile-asm', action='store_true', help="Compiles the script to a psuedo-assembly language for human reading.")
action.add_argument('--compile', action='store_true', help="Compiles the script to a bytecode file.")
action.add_argument('--bytecode', action='store_true', help="Reads a bytecode file and runs it in a VM.")

args = ap.parse_args()

## Other

class Console(object):
    def write(self, s):
        print(s, end='')

## Main

if __name__ == '__main__':
    # Reading the code
    if args.bytecode:
        print(f":: Reading bytecode from file '{args.input}'")
        k, i = calc_comp.read_bytecode(args.input)

        print(f":: Running")
        calc_vm.run(k, i)
    else:
        print(f":: Parsing file '{args.input}'")
        lexer = CalcLexer()
        parser = CalcParser()

        with open(args.input, 'r') as f:
            ast = parser.parse(lexer.tokenize(f.read()))

        if args.compile:
            if args.output is None:
                raise ValueError(f"Please specify an output file.")
            
            compiler = calc_comp.Compiler()
            compiler.c_block(ast)

            calc_comp.write_bytecode(compiler, args.output)
        elif args.compile_asm:
            # if args.output is None:
            #     raise ValueError(f"Please specify an output file.")
            
            compiler = calc_comp.Compiler()
            compiler.c_block(ast)

            if args.output is None:
                compiler.write_instructions(Console())
            else:
                with open(args.output, 'w') as f:
                    compiler.write_instructions(f)
        else:
            print(f":: Interpreting")

            calc_interp.interpret(ast)