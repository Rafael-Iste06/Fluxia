# fluxia.py

import sys
from fluxia_lexer import lex
from fluxia_parser import Parser, ParserError
from fluxia_compiler import Compiler, CompilerError
from fluxia_vm import FluxiaVM, VMError

def run_fluxia_file(path: str):
    with open(path, "r", encoding="utf-8") as f:
        code = f.read()

    try:
        tokens = lex(code)
        parser = Parser(tokens)
        program = parser.parse()
        compiler = Compiler()
        functions, uses = compiler.compile(program)
        vm = FluxiaVM(functions, uses)
        vm.run()
    except (ParserError, CompilerError, VMError, Exception) as e:
        print("Error:", e)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fluxia.py <file.fx>")
        sys.exit(1)
    run_fluxia_file(sys.argv[1])
