# fluxia_parser.py

from typing import List
from dataclasses import dataclass
from fluxia_lexer import Token

# === AST ===

class Node: ...

@dataclass
class Program(Node):
    uses: List[str]
    functions: List["FunctionDef"]
    statements: List[Node]

@dataclass
class FunctionDef(Node):
    name: str
    params: List[str]
    body: List[Node]

@dataclass
class VarDecl(Node):
    name: str
    expr: Node

@dataclass
class Assign(Node):
    name: str
    expr: Node

@dataclass
class If(Node):
    cond: Node
    then_body: List[Node]
    else_body: List[Node]

@dataclass
class While(Node):
    cond: Node
    body: List[Node]

@dataclass
class Return(Node):
    expr: Node

@dataclass
class Number(Node):
    value: float

@dataclass
class String(Node):
    value: str

@dataclass
class Bool(Node):
    value: bool

@dataclass
class Var(Node):
    name: str

@dataclass
class BinaryOp(Node):
    left: Node
    op: str
    right: Node

@dataclass
class Call(Node):
    func: str
    args: List[Node]


class ParserError(Exception):
    pass


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.i = 0

    def current(self) -> Token:
        return self.tokens[self.i]

    def consume(self, type_: str, value: str = None):
        tok = self.current()
        if tok.type != type_:
            raise ParserError(f"Expected {type_}, got {tok.type} at {tok.line}:{tok.col}")
        if value is not None and tok.value != value:
            raise ParserError(f"Expected {value}, got {tok.value} at {tok.line}:{tok.col}")
        self.i += 1
        return tok

    def parse(self) -> Program:
        uses = []
        functions = []
        statements = []
        while self.current().type != "EOF":
            if self.current().type == "USE":
                uses.append(self.parse_use())
            elif self.current().type == "FN":
                functions.append(self.parse_function())
            else:
                statements.append(self.parse_statement())
        return Program(uses, functions, statements)

    def parse_use(self) -> str:
        self.consume("USE")
        tok = self.consume("ID")
        if self.current().type == "SEMICOLON":
            self.consume("SEMICOLON")
        return tok.value

    def parse_function(self) -> FunctionDef:
        self.consume("FN")
        name = self.consume("ID").value
        self.consume("LPAREN")
        params = []
        if self.current().type != "RPAREN":
            while True:
                params.append(self.consume("ID").value)
                if self.current().type == "COMMA":
                    self.consume("COMMA")
                else:
                    break
        self.consume("RPAREN")
        self.consume("LBRACE")
        body = self.parse_block()
        return FunctionDef(name, params, body)

    def parse_block(self) -> List[Node]:
        stmts = []
        while self.current().type != "RBRACE":
            stmts.append(self.parse_statement())
        self.consume("RBRACE")
        return stmts

    def parse_statement(self) -> Node:
        tok = self.current()
        if tok.type == "LET":
            return self.parse_vardecl()
        if tok.type == "IF":
            return self.parse_if()
        if tok.type == "WHILE":
            return self.parse_while()
        if tok.type == "RETURN":
            return self.parse_return()

        # assign
        if tok.type == "ID" and self.tokens[self.i+1].type == "ASSIGN":
            name = self.consume("ID").value
            self.consume("ASSIGN")
            expr = self.parse_expression()
            if self.current().type == "SEMICOLON":
                self.consume("SEMICOLON")
            return Assign(name, expr)

        # expression statement
        expr = self.parse_expression()
        if self.current().type == "SEMICOLON":
            self.consume("SEMICOLON")
        return expr

    def parse_vardecl(self) -> VarDecl:
        self.consume("LET")
        name = self.consume("ID").value
        self.consume("ASSIGN")
        expr = self.parse_expression()
        if self.current().type == "SEMICOLON":
            self.consume("SEMICOLON")
        return VarDecl(name, expr)

    def parse_if(self) -> If:
        self.consume("IF")
        self.consume("LPAREN")
        cond = self.parse_expression()
        self.consume("RPAREN")
        self.consume("LBRACE")
        then_body = self.parse_block()
        else_body = []
        if self.current().type == "ELSE":
            self.consume("ELSE")
            self.consume("LBRACE")
            else_body = self.parse_block()
        return If(cond, then_body, else_body)

    def parse_while(self) -> While:
        self.consume("WHILE")
        self.consume("LPAREN")
        cond = self.parse_expression()
        self.consume("RPAREN")
        self.consume("LBRACE")
        body = self.parse_block()
        return While(cond, body)

    def parse_return(self) -> Return:
        self.consume("RETURN")
        if self.current().type == "SEMICOLON":
            self.consume("SEMICOLON")
            return Return(Number(0.0))
        expr = self.parse_expression()
        if self.current().type == "SEMICOLON":
            self.consume("SEMICOLON")
        return Return(expr)

    # === Expressions ===

    def parse_expression(self) -> Node:
        return self.parse_equality()

    def parse_equality(self) -> Node:
        node = self.parse_comparison()
        while self.current().type in ("EQEQ", "NEQ"):
            op_tok = self.current()
            self.i += 1
            right = self.parse_comparison()
            node = BinaryOp(node, op_tok.type, right)
        return node

    def parse_comparison(self) -> Node:
        node = self.parse_term()
        while self.current().type in ("GT", "LT", "GTE", "LTE"):
            op_tok = self.current()
            self.i += 1
            right = self.parse_term()
            node = BinaryOp(node, op_tok.type, right)
        return node

    def parse_term(self) -> Node:
        node = self.parse_factor()
        while self.current().type in ("PLUS", "MINUS"):
            op_tok = self.current()
            self.i += 1
            right = self.parse_factor()
            node = BinaryOp(node, op_tok.type, right)
        return node

    def parse_factor(self) -> Node:
        node = self.parse_unary()
        while self.current().type in ("MUL", "DIV"):
            op_tok = self.current()
            self.i += 1
            right = self.parse_unary()
            node = BinaryOp(node, op_tok.type, right)
        return node

    def parse_unary(self) -> Node:
        if self.current().type == "MINUS":
            self.consume("MINUS")
            expr = self.parse_unary()
            return BinaryOp(Number(0.0), "MINUS", expr)
        return self.parse_primary()

    def parse_primary(self) -> Node:
        tok = self.current()
        if tok.type == "NUMBER":
            self.i += 1
            return Number(float(tok.value))
        if tok.type == "STRING":
            self.i += 1
            return String(tok.value[1:-1])
        if tok.type == "TRUE":
            self.i += 1
            return Bool(True)
        if tok.type == "FALSE":
            self.i += 1
            return Bool(False)
        if tok.type == "ID":
            name = tok.value
            self.i += 1
            if self.current().type == "LPAREN":
                self.consume("LPAREN")
                args = []
                if self.current().type != "RPAREN":
                    while True:
                        args.append(self.parse_expression())
                        if self.current().type == "COMMA":
                            self.consume("COMMA")
                        else:
                            break
                self.consume("RPAREN")
                return Call(name, args)
            return Var(name)
        if tok.type == "LPAREN":
            self.consume("LPAREN")
            expr = self.parse_expression()
            self.consume("RPAREN")
            return expr
        raise ParserError(f"Unexpected token {tok.type} ({tok.value}) at {tok.line}:{tok.col}")
