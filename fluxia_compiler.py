# fluxia_compiler.py

from typing import List, Dict, Tuple
from fluxia_parser import (
    Program, FunctionDef, VarDecl, Assign, If, While, Return,
    Number, String, Bool, Var, BinaryOp, Call, Node
)

class CompilerError(Exception):
    pass

class Compiler:
    def __init__(self):
        self.functions: Dict[str, Tuple[List[str], List[Tuple]]] = {}
        self.current_code: List[Tuple] = []
        self.current_function: str = "__main__"

    def compile(self, program: Program):
        # Top-level => __main__
        self.current_code = []
        self.current_function = "__main__"
        for stmt in program.statements:
            self.compile_stmt(stmt)
        # retour implicite
        self.current_code.append(("PUSH_CONST", None))
        self.current_code.append(("RETURN",))
        self.functions["__main__"] = ([], self.current_code)

        # fonctions déclarées
        for fn in program.functions:
            self.compile_function(fn)

        return self.functions, program.uses

    def compile_function(self, fn: FunctionDef):
        prev_code = self.current_code
        prev_name = self.current_function

        self.current_code = []
        self.current_function = fn.name

        for stmt in fn.body:
            self.compile_stmt(stmt)
        self.current_code.append(("PUSH_CONST", None))
        self.current_code.append(("RETURN",))

        self.functions[fn.name] = (fn.params, self.current_code)

        self.current_code = prev_code
        self.current_function = prev_name

    def compile_stmt(self, node: Node):
        if isinstance(node, VarDecl):
            self.compile_expr(node.expr)
            self.current_code.append(("STORE_VAR", node.name))
        elif isinstance(node, Assign):
            self.compile_expr(node.expr)
            self.current_code.append(("STORE_VAR", node.name))
        elif isinstance(node, If):
            self.compile_expr(node.cond)
            jmp_false_index = len(self.current_code)
            self.current_code.append(("JUMP_IF_FALSE", None))
            for s in node.then_body:
                self.compile_stmt(s)
            jmp_end_index = len(self.current_code)
            self.current_code.append(("JUMP", None))
            else_start = len(self.current_code)
            self.current_code[jmp_false_index] = ("JUMP_IF_FALSE", else_start)
            for s in node.else_body:
                self.compile_stmt(s)
            end_pos = len(self.current_code)
            self.current_code[jmp_end_index] = ("JUMP", end_pos)
        elif isinstance(node, While):
            loop_start = len(self.current_code)
            self.compile_expr(node.cond)
            jmp_false_index = len(self.current_code)
            self.current_code.append(("JUMP_IF_FALSE", None))
            for s in node.body:
                self.compile_stmt(s)
            self.current_code.append(("JUMP", loop_start))
            after_loop = len(self.current_code)
            self.current_code[jmp_false_index] = ("JUMP_IF_FALSE", after_loop)
        elif isinstance(node, Return):
            self.compile_expr(node.expr)
            self.current_code.append(("RETURN",))
        else:
            # expression seule
            self.compile_expr(node)
            self.current_code.append(("POP",))

    def compile_expr(self, node: Node):
        if isinstance(node, Number):
            self.current_code.append(("PUSH_CONST", node.value))
        elif isinstance(node, String):
            self.current_code.append(("PUSH_CONST", node.value))
        elif isinstance(node, Bool):
            self.current_code.append(("PUSH_CONST", node.value))
        elif isinstance(node, Var):
            self.current_code.append(("LOAD_VAR", node.name))
        elif isinstance(node, BinaryOp):
            self.compile_expr(node.left)
            self.compile_expr(node.right)
            op_map = {
                "PLUS": "BINARY_ADD",
                "MINUS": "BINARY_SUB",
                "MUL": "BINARY_MUL",
                "DIV": "BINARY_DIV",
                "GT": "BINARY_GT",
                "LT": "BINARY_LT",
                "GTE": "BINARY_GTE",
                "LTE": "BINARY_LTE",
                "EQEQ": "BINARY_EQ",
                "NEQ": "BINARY_NEQ",
            }
            if node.op not in op_map:
                raise CompilerError(f"Unknown binary operator {node.op}")
            self.current_code.append((op_map[node.op],))
        elif isinstance(node, Call):
            for arg in node.args:
                self.compile_expr(arg)
            self.current_code.append(("CALL", node.func, len(node.args)))
        else:
            raise CompilerError(f"Unknown expression node {type(node).__name__}")
