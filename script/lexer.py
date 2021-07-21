# import the modules
import decimal
import ply.lex as lex
from sys import exit

# declare tokens
tokens = [
"ID",
"COMMENT",
"NUMBER",
"STRING",
"EQU",
"BOE",
"SOE",
"NOE",
"BIG",
"SMA",
"SET",
"AAS",
"SAS",
"MAS",
"DAS",
"RAS",
"SQS",
]

reserved = {
"if" : "IF",
"else" : "ELSE",
"while" : "WHILE",
"until" : "UNTIL",
"for" : "FOR",
"break" : "BREAK",
"continue" : "CONTINUE",
"define" : "DEFINE",
"true" : "TRUE",
"false" : "FALSE",
}

literals = ['+','-','*','/', '%', '^', '&', '|', '!', '(', ')', '{', '}', '[', ']', ';', ',']

# tokens = tokens + reserved
tokens = tokens + list(reserved.values())

# define tokens
def t_NUMBER(t):
    r'\d+\.?\d*([eE]\d+)?'
    t.value = decimal.Decimal(t.value)
    return t

def t_STRING(t):
    r'("(\\"|[^"])*")|(\'(\\\'|[^\'])*\')'
    t.value = t.value[1:-1]
    return t

def t_EQU(t):
    r'=='
    return t

def t_BOE(t):
    r'>='
    return t

def t_SOE(t):
    r'<='
    return t

def t_NOE(t):
    r'!='
    return t

def t_BIG(t):
    r'>'
    return t

def t_SMA(t):
    r'<'
    return t

def t_SET(t):
    r'='
    return t

def t_AAS(t):
    r'\+='
    return t

def t_SAS(t):
    r'-='
    return t

def t_MAS(t):
    r'\*='
    return t

def t_DAS(t):
    r'/='
    return t

def t_RAS(t):
    r'%='
    return t

def t_SQS(t):
    r'\^='
    return t

# reserved, line, error, comment, ignore
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')
    return t

def t_COMMENT(t):
    r'\#.*'
    pass

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t): t.lexer.skip(1)

t_ignore    = ' \t'

# build lexer
lexer = lex.lex()

# debug code
if __name__ == "__main__":
    lexer.input(input('@'))
    while True:
        tok = lexer.token()
        if not tok: break
        print(":", tok)
