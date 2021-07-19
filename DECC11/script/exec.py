# set memory
stack = []
data = [{}]
file = {}
file_num = 0

# import the modules
import os
import sys
import decimal
import script.parser
from decimal import Decimal

# define command functions
def ADD():
    global stack
    y = stack.pop()
    x = stack.pop()
    stack.append(x + y)
    return

def SUB():
    global stack
    y = stack.pop()
    x = stack.pop()
    stack.append(x - y)
    return

def MUL():
    global stack
    y = stack.pop()
    x = stack.pop()
    stack.append(x * y)
    return

def DIV():
    global stack
    y = stack.pop()
    x = stack.pop()
    stack.append(x / y)
    return

def REM():
    global stack
    y = stack.pop()
    x = stack.pop()
    stack.append(x % y)
    return

def SQU():
    global stack
    y = stack.pop()
    x = stack.pop()
    stack.append(x ** y)
    return

def AND():
    global stack
    y = stack.pop()
    x = stack.pop()
    stack.append(decimal.Decimal(x and y))
    return

def OR():
    global stack
    y = stack.pop()
    x = stack.pop()
    stack.append(decimal.Decimal(x or y))
    return

def NOT():
    global stack
    x = stack.pop()
    stack.append(decimal.Decimal(not x))
    return

def EQU():
    global stack
    y = stack.pop()
    x = stack.pop()
    stack.append(decimal.Decimal(x == y))
    return

def BOE():
    global stack
    y = stack.pop()
    x = stack.pop()
    stack.append(decimal.Decimal(x >= y))
    return

def SOE():
    global stack
    y = stack.pop()
    x = stack.pop()
    stack.append(decimal.Decimal(x <= y))
    return

def BIG():
    global stack
    y = stack.pop()
    x = stack.pop()
    stack.append(decimal.Decimal(x > y))
    return

def SMA():
    global stack
    y = stack.pop()
    x = stack.pop()
    stack.append(decimal.Decimal(x < y))
    return

def NOE():
    global stack
    y = stack.pop()
    x = stack.pop()
    stack.append(decimal.Decimal(x != y))
    return

def SET():
    global stack
    global data
    y = stack.pop()
    x = stack.pop()
    a = x
    if type(x) == type([]): a = x[0]
    if a in data[0]:
        if type(x) == type([]):
            if type(y) == type(decimal.Decimal(10)): exec("data[0]['" + x[0] + "']" + x[1] + " = Decimal(" + str(y) + ')')
            elif type(y) == type([]): exec("data[0]['" + x[0] + "']" + x[1] + " = " + str(y))
            else: exec("data[0]['" + x[0] + "']" + x[1] + " = \"" + str(y) + '"')
        else: data[0][x] = y
        return
    if type(x) == type([]):
        if type(y) == type(decimal.Decimal(10)): exec("data[-1]['" + x[0] + "']" + x[1] + " = Decimal(" + str(y) + ')')
        elif type(y) == type([]): exec("data[-1]['" + x[0] + "']" + x[1] + " = " + str(y))
        else: exec("data[-1]['" + x[0] + "']" + x[1] + " = \"" + str(y) + '"')
    else: data[-1][x] = y
    return

def ARRAY():
    global stack
    global data
    ret = []
    po = stack.pop()
    while po != '#':
        ret.append(po)
        po = stack.pop()
    ret.reverse()
    stack.append(ret)
    return

def QUIT():
    os._exit(stack.pop())

def WRITE():
    global stack
    if not stack: return
    print(stack.pop(), end='')
    return

def READ():
    global stack
    try:
        stack.append(input())
    except:
        exit(1)
    return

def FOPEN():
    global stack
    global file
    global file_num
    x = stack.pop()
    y = stack.pop()
    f = open(y, x)
    file[file_num] = f;
    stack.append(file_num)
    file_num += 1
    return

def FCLOSE():
    global stack
    global file
    global file_num
    file[stack.pop()].close()
    return

def FWRITE():
    global stack
    global file
    x = stack.pop()
    y = stack.pop()
    file[y].write(x)
    return

def FREAD():
    global stack
    global file
    stack.append(file[stack.pop()].read())
    return

def PYTHON():
    global stack
    exec(stack.pop())
    return

def EXEC():
    global stack
    x = stack.pop()
    execd(script.parser.compile(x))
    return

def SYSTEM():
    global stack
    os.system(stack.pop())
    return

def NUM():
    global stack
    stack.append(decimal.Decimal(stack.pop()))
    return

def STR():
    global stack
    stack.append(str(stack.pop()))
    return

def ARR():
    global stack
    stack.append([decimal.Decimal(0) for i in range(int(stack.pop()))])
    return

def LEN():
    global stack
    stack.append(len(stack.pop()))
    return

def CHR():
    global stack
    stack.append(chr(stack.pop()))
    return

def ORD():
    global stack
    stack.append(ord(stack.pop()))
    return

# command dict
dic = {
    '+' : ADD,
    '-' : SUB,
    '*' : MUL,
    '/' : DIV,
    '%' : REM,
    '^' : SQU,
    '&' : AND,
    '|' : OR,
    '!' : NOT,
    "==" : EQU,
    ">=" : BOE,
    "<=" : SOE,
    '>' : BIG,
    '<' : SMA,
    "!=" : NOE,
    '=' : SET,
    "array" : ARRAY,
    "quit" : QUIT,
    "write" : WRITE,
    "read" : READ,
    "fopen" : FOPEN,
    "fclose" : FCLOSE,
    "fwrite" : FWRITE,
    "fread" : FREAD,
    "python" : PYTHON,
    "exec" : EXEC,
    "system" : SYSTEM,
    "num" : NUM,
    "str" : STR,
    "arr" : ARR,
    "len" : LEN,
    "chr" : CHR,
    "ord" : ORD,
}

# exec code
def execd(code, argv=[]):
    global stack
    global data
    global dic
    data[0]["argc"] = decimal.Decimal(len(sys.argv))
    data[0]["argv"] = list(sys.argv)
    WHILE = []
    com = code.split()
    if com[0] == '{' and com[-1] == '}': com = com[1:-1]
    ptr = 0
    end = len(com)
    while ptr < end:
        state = com[ptr]
        if state in dic:
            if type(dic[state]) == type([]):
                data.append({})
                for i in dic[state][0]:
                    data[-1][i] = stack.pop()
                execd(dic[state][1], argv)
                data.pop()
            else: dic[state]()
        elif state in data[0]: stack.append(data[0][state])
        elif state in data[-1]: stack.append(data[-1][state])
        elif state == '#': stack.append('#')
        elif state == '@':
            ptr += 1
            stack.append(decimal.Decimal(com[ptr]))
        elif state == ':':
            ptr += 1
            if com[ptr] == "index":
                ret = []
                ptr += 1
                while com[ptr] != "index":
                    inx = ""
                    while com[ptr] != '?' and com[ptr] != "$$":
                        inx += str(com[ptr]) + ' '
                        ptr += 1
                    if com[ptr] != "$$":
                        execd(inx)
                        ret.append(stack.pop())
                    else:
                        ret.append(inx[:-1])
                    ptr += 1
                save = ret.pop()
                eval_text = ""
                for i in ret: eval_text = eval_text + '[' + str(i) + ']'
                stack.append([save, eval_text])
            else:
                stack.append(com[ptr])
        elif state == '"':
            ptr += 1
            t = com[ptr]
            t = t.replace('°', ' ')
            t = t.replace("\\n", '\n')
            t = t.replace("\\t", '\t')
            t = t.replace("\\'", '\'')
            t = t.replace("\\\"", '\"')
            t = t.replace("\\\\", '\\')
            stack.append(t[1:])
        elif state == "define":
            ptr += 1
            name = com[ptr]
            ptr += 1
            fac = []
            while com[ptr] != "define":
                fac += com[ptr]
                ptr += 1
            dic[name] = []
            fac.reverse()
            dic[name].append(fac)
            ptr += 1
            fac = ""
            while com[ptr] != "define":
                fac += str(com[ptr]) + ' '
                ptr += 1
            dic[name].append(fac)
        elif state == "if":
            if not stack.pop():
                block = 1
                while block > 0:
                    ptr += 1
                    if com[ptr] == "if": block += 1
                    elif com[ptr] == "end": block -= 1
        elif state == "ifelse":
            if not stack.pop():
                block = 1
                while block > 0:
                    ptr += 1
                    if com[ptr] == "ifelse": block += 1
                    elif com[ptr] == "else": block -= 1
        elif state == "else":
            block = 1
            while block > 0:
                ptr += 1
                if com[ptr] == "else": block += 1
                elif com[ptr] == "endelse": block -= 1
        elif state == "endelse": pass
        elif state == "while":
            WHILE.append([stack.pop(), ptr])
            execd(WHILE[-1][0])
            if not stack.pop():
                ptr += 1
                block = 1
                while block > 0:
                    ptr += 1
                    if com[ptr] == "while": block += 1
                    elif com[ptr] == "back": block -= 1
        elif state == "back" or state == "continue":
            dup = WHILE.pop()
            ptr = dup[1] - 1
            stack.append(dup[0])
        elif state == "break":
            block = 1
            while block > 0:
                ptr += 1
                if com[ptr] == "while": block += 1
                elif com[ptr] == "back": block -= 1
        elif state == "index":
            ret = []
            ptr += 1
            while com[ptr] != "index":
                inx = ""
                while com[ptr] != '?' and com[ptr] != "$$":
                    inx += str(com[ptr]) + ' '
                    ptr += 1
                if com[ptr] != "$$":
                    execd(inx)
                    ret.append(stack.pop())
                else:
                    if inx[:-1] in data[0]: ret.append(data[0][inx[:-1]])
                    else: ret.append(data[-1][inx[:-1]])
                ptr += 1
            save = ret.pop()
            for i in ret:
                save = save[int(i)]
            stack.append(save)
        elif state == "return": return
        elif state == "end": pass
        elif state == '{':
            block = 1
            ptr += 1
            t = ""
            while block != 0:
                if com[ptr] == '}': block -= 1
                elif com[ptr] == '{': block += 1
                if block != 0:
                    t = t + ' ' + com[ptr]
                    ptr += 1
            stack.append(t)
        else:
            print("Segmentation ERROR")
            os._exit(0)
        ptr += 1
    return
