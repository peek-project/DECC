# import the modules
import decimal
import ply.yacc as yacc

# import lexer output
if __name__ == "__main__": from lexer import tokens
else: from script.lexer import tokens
error_p = False

# define AST Node
class N:
    def __init__(self,type,child,leaf):
        self.type = type
        self.child = child
        self.leaf = leaf

# define rules
def p_proc_proc(p):
    "proc : proc com"
    p[0] = N("proc_proc", [p[1], p[2]], '')

def p_proc_com(p):
    "proc : com"
    p[0] = N("proc_com", [p[1]], '')

def p_com_block(p):
    "com : '{' proc '}'"
    p[0] = N("com_block", [p[2]], '')

def p_com_if(p):
    "com : if"
    p[0] = N("com_if", [p[1]], '')

def p_if_ifelse(p): #crash
    "if : IF '(' expr ')' com ELSE com"
    p[0] = N("if_ifelse", [p[3], "ifelse", p[5], "else", p[7], "endelse"], '')

def p_if_if(p):
    "if : IF '(' expr ')' com"
    p[0] = N("if_if", [p[3], "if", p[5], "end"], '')

def p_com_while(p):
    "com : WHILE '(' expr ')' com"
    p[0] = N("com_while", ['{', p[3], "} while", p[5], "back"], '')

def p_com_until(p):
    "com : UNTIL '(' expr ')' com"
    p[0] = N("com_until", ["{ @ 1 } while", p[5], p[3], "if break end"], '')

def p_com_for(p):
    "com : FOR '(' cexpr cexpr expr ')' com"
    p[0] = N("com_while", [p[3], '{', p[4], "} while", p[7], p[5], "back"], '')

def p_com_define(p):
    "com : DEFINE ID '(' call ')' com"
    p[0] = N("com_define", ["define", p[2], p[4], "define", p[6]], "define")

def p_com_cexpr(p):
    "com : cexpr"
    p[0] = N("com_cexpr", [p[1]], '')

def p_com_none(p):
    "com : ';'"
    p[0] = N("com_none", [], '')

def p_cexpr_expr(p):
    "cexpr : expr ';'"
    p[0] = N("cexpr_expr", [p[1]], '')

def p_expr_substitute(p):
    "expr : substitute"
    p[0] = N("expr_substitute", [p[1]], '')

def p_substitute_set(p):
    "substitute : substitute SET logical"
    p[0] = N("substitute_set", [':', p[1], p[3]], p[2])

def p_substitute_aas(p):
    "substitute : substitute AAS logical"
    p[0] = N("substitute_aas", [':', p[1], p[1], p[3], '+'], '=')

def p_substitute_sas(p):
    "substitute : substitute SAS logical"
    p[0] = N("substitute_sas", [':', p[1], p[1], p[3], '-'], '=')

def p_substitute_mas(p):
    "substitute : substitute MAS logical"
    p[0] = N("substitute_mas", [':', p[1], p[1], p[3], '*'], '=')

def p_substitute_das(p):
    "substitute : substitute DAS logical"
    p[0] = N("substitute_das", [':', p[1], p[1], p[3], '/'], '=')

def p_substitute_ras(p):
    "substitute : substitute RAS logical"
    p[0] = N("substitute_ras", [':', p[1], p[1], p[3], '%'], '=')

def p_substitute_sqs(p):
    "substitute : substitute SQS logical"
    p[0] = N("substitute_sqs", [':', p[1], p[1], p[3], '^'], '=')

def p_substitute_logical(p):
    "substitute : logical"
    p[0] = N("substitute_logical", [p[1]], '')

def p_logical_and(p):
    "logical : logical '&' comparison"
    p[0] = N("logical_and", [p[1], p[3]], p[2])

def p_logical_or(p):
    "logical : logical '|' comparison"
    p[0] = N("logical_or", [p[1], p[3]], p[2])

def p_logical_not(p):
    "logical : '!' comparison"
    p[0] = N("logical_not", [p[2]], p[1])

def p_logical_comparison(p):
    "logical : comparison"
    p[0] = N("logical_comparison", [p[1]], '')

def p_comparison_equ(p):
    "comparison : comparison EQU polynomial"
    p[0] = N("comparison_equ", [p[1], p[3]], p[2])

def p_comparison_boe(p):
    "comparison : comparison BOE polynomial"
    p[0] = N("comparison_boe", [p[1], p[3]], p[2])

def p_comparison_soe(p):
    "comparison : comparison SOE polynomial"
    p[0] = N("comparison_soe", [p[1], p[3]], p[2])

def p_comparison_noe(p):
    "comparison : comparison NOE polynomial"
    p[0] = N("comparison_noe", [p[1], p[3]], p[2])

def p_comparison_big(p):
    "comparison : comparison BIG polynomial"
    p[0] = N("comparison_big", [p[1], p[3]], p[2])

def p_comparison_sma(p):
    "comparison : comparison SMA polynomial"
    p[0] = N("comparison_sma", [p[1], p[3]], p[2])

def p_comparison_polynomial(p):
    "comparison : polynomial"
    p[0] = N("comparison_polynomial", [p[1]], '')

def p_polynomial_add(p):
    "polynomial : polynomial '+' factor"
    p[0] = N("polynomial_add", [p[1], p[3]], p[2])

def p_polynomial_sub(p):
    "polynomial : polynomial '-' factor"
    p[0] = N("polynomial_sub", [p[1], p[3]], p[2])

def p_polynomial_factor(p):
    "polynomial : factor"
    p[0] = N("polynomial_factor", [p[1]], '')

def p_factor_mul(p):
    "factor : factor '*' element"
    p[0] = N("factor_mul", [p[1], p[3]], p[2])

def p_factor_div(p):
    "factor : factor '/' element"
    p[0] = N("factor_div", [p[1], p[3]], p[2])

def p_factor_rem(p):
    "factor : factor '%' element"
    p[0] = N("factor_rem", [p[1], p[3]], p[2])

def p_factor_squ(p): #crash
    "factor : element '^' factor"
    p[0] = N("factor_squ", [p[1], p[3]], p[2])

def p_factor_element(p):
    "factor : element"
    p[0] = N("factor_element", [p[1]], '')

def p_element_break(p):
    "element : BREAK"
    p[0] = N("element_break", [], "break")

def p_element_continue(p):
    "element : CONTINUE"
    p[0] = N("element_continue", [], "continue")

def p_element_minus(p):
    "element : '-' NUMBER"
    p[0] = N("p_element_minus", ['@'], -p[2])

def p_element_number(p):
    "element : NUMBER"
    p[0] = N("element_number", ['@'], p[1])

def p_element_true(p):
    "element : TRUE"
    p[0] = N("element_true", ['@'], decimal.Decimal(1))

def p_element_false(p):
    "element : FALSE"
    p[0] = N("element_false", ['@'], decimal.Decimal(0))

def p_element_string(p):
    "element : STRING"
    p[0] = N("element_string", ['" ', 'a' + p[1].replace(' ', '°').replace('\t', "\\t").replace('\n', "\\n")], '')

def p_element_func(p):
    "element : ID '(' call ')'"
    p[0] = N("element_func", [p[3]], p[1])

def p_element_var(p):
    "element : ID"
    p[0] = N("element_var", [p[1]], "")

def p_element_array(p):
    "element : '{' call '}'"
    p[0] = N("element_array", ['#', p[2]], "array")

def p_element_index(p):
    "element : ID index"
    p[0] = N("element_var", ["index", p[2], p[1], "$$ index"], "")

def p_index_index(p):
    "index : index '[' expr ']'"
    p[0] = N("call_call", [p[1], p[3], '?'], '')
    
def p_index_expr(p):
    "index : '[' expr ']'"
    p[0] = N("index_expr", [p[2], '?'], '')

def p_element_parenthesis(p):
    "element : '(' expr ')'"
    p[0] = N("element_var", [p[2]], '')

def p_call_call(p):
    "call : call ',' expr"
    p[0] = N("call_call", [p[1], p[3]], '')

def p_call_expr(p):
    "call : expr"
    p[0] = N("call_expr", [p[1]], '')

def p_call_none(p):
    "call : "
    p[0] = N("call_none", [], '')

# error
def p_error(p):
    global error_p
    if not error_p: print("Syntax ERROR")
    error_p = True

# build parser
parser = yacc.yacc()

# post DFS
text = ""
def dfs(graph):
    global text
    if isinstance(graph, N):
        for i in graph.child: dfs(i)
        text += str(graph.leaf) + ' '
    else: text += str(graph) + ' '

# compile
def compile(code):
    global error_p
    global text
    text = ""
    endcode = parser.parse(code)
    if error_p: return False
    dfs(endcode)
    endtext = ""
    for i in text.split():
        endtext = endtext + i + ' '
    return endtext

# debug code
if __name__ == "__main__":
    s = ""
    while True:
        t = input('@')
        if t == "run" or t == 'r': break
        s += t
    result = compile(s)
    print(result)
