# fluxia_lexer.py

import re

TOKEN_SPEC = [
    ("NUMBER",   r"\d+(\.\d+)?"),
    ("STRING",   r"\"(\\.|[^\"])*\""),
    ("ID",       r"[A-Za-z_][A-Za-z0-9_]*"),
    ("LPAREN",   r"\("),
    ("RPAREN",   r"\)"),
    ("LBRACE",   r"\{"),
    ("RBRACE",   r"\}"),
    ("COMMA",    r","),
    ("SEMICOLON",r";"),
    ("PLUS",     r"\+"),
    ("MINUS",    r"-"),
    ("MUL",      r"\*"),
    ("DIV",      r"/"),
    ("EQEQ",     r"=="),
    ("NEQ",      r"!="),
    ("GTE",      r">="),
    ("LTE",      r"<="),
    ("GT",       r">"),
    ("LT",       r"<"),
    ("ASSIGN",   r"="),
    ("NEWLINE",  r"\n"),
    ("SKIP",     r"[ \t\r]+"),
    ("COMMENT",  r"//[^\n]*"),
]

TOK_REGEX = "|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPEC)

KEYWORDS = {
    "let": "LET",
    "fn": "FN",
    "return": "RETURN",
    "if": "IF",
    "else": "ELSE",
    "while": "WHILE",
    "use": "USE",
    "true": "TRUE",
    "false": "FALSE",
}

class Token:
    def __init__(self, type_, value, line, col):
        self.type = type_
        self.value = value
        self.line = line
        self.col = col

    def __repr__(self):
        return f"Token({self.type}, {self.value}, {self.line}:{self.col})"

def lex(code: str):
    tokens = []
    line = 1
    col = 1
    for m in re.finditer(TOK_REGEX, code):
        kind = m.lastgroup
        value = m.group()
        if kind == "NEWLINE":
            line += 1
            col = 1
            continue
        if kind in ("SKIP", "COMMENT"):
            col += len(value)
            continue
        if kind == "ID" and value in KEYWORDS:
            kind = KEYWORDS[value]
        tokens.append(Token(kind, value, line, col))
        col += len(value)
    tokens.append(Token("EOF", "", line, col))
    return tokens
