#interpreter
#xxeol test
import math
import operator as op
from functools import reduce
from parser1 import expression_parser

lisp_to_python_dic = {
    '+':lambda *x: reduce(op.add, *x), '-':lambda *x: reduce(op.sub, *x),
    '*':lambda *x: reduce(op.mul, *x), '/':lambda *x: reduce(op.truediv, *x),
    '>':lambda *x: reduce(op.gt, *x), '<':lambda *x: reduce(op.lt, *x),
    '>=':lambda *x: reduce(op.ge, *x), '<=':lambda *x: reduce(op.le, *x),
    '=':lambda *x: reduce(op.eq, *x),
    'abs':     abs,
    'append':  lambda *x: reduce(op.add, *x),
    'apply':   lambda x: x[0](x[1:]),
    'begin':   lambda *x: x[-1],
    'car':     lambda x: x[0],
    'cdr':     lambda x: x[1:],
    'cons':    lambda x, y: [x] + y,
    'eq?':     op.is_,
    'equal?':  op.eq,
    'length':  len,
    'list':    lambda *x: list(x),
    'list?':   lambda x: isinstance(x, list),
    'map':     map,
    'max':     max,
    'min':     min,
    'not':     op.not_,
    'null?':   lambda x: x == [],
    'number?': lambda x: isinstance(x, int) or isinstance(x, float),
    'procedure?': callable,
    'round':   round,
    'symbol?': lambda x: isinstance(x, str),
    'LIST' : 3,
    }

lisp_to_python_dic.update(vars(math))

dic_new2 = {}

mem = {}

def CAR_procedure(carList, dic):
    if isList(eval(carList,dic))[0]: #true 이면
        if isList(eval(carList,dic))[1] == 0: # 직접 입력
            return eval(carList,dic)[1][0]
        elif isList(eval(carList,dic))[1] == 1: #저장된 리스트
            return mem[eval(carList,dic)][1][0]

def CDR_procedure(cdrList, dic):
    if isList(eval(cdrList,dic))[0]: #true 이면
        if isList(eval(cdrList,dic))[1] == 0: # 직접 입력
            T = ["'"]
            T.append(eval(cdrList,dic)[1][1:])
            return T
        elif isList(eval(cdrList,dic))[1] == 1: #저장된 리스트
            T = ["'"]
            T.append(mem[eval(cdrList,dic)][1][1:])
            return T

def addQuote(vlist):
    reList = ["'",]
    reList.append(vlist)
    return reList

def isList(vlist):
    if isinstance(vlist, list):
        if vlist[0] == "'":
            if isinstance(vlist[1], list):
                return [True,0] #직접 list 입력
    elif isinstance(vlist, str):
        if vlist in mem:
            if mem[vlist][0] == "'" and isinstance(mem[vlist][1],list):
                return [True,1] #mem에 저장되어있는 list
def lambda_procedure(parms, body, *args):
    dic_new = {}
    for k, v in list(zip(parms, list(*args))):
        dic_new[k] = v
    dic_new2.update(lisp_to_python_dic)
    dic_new2.update(dic_new)
    return eval(body, dic_new2)

def list_procedure(*args):
    T = ["'"]
    L = []
    #print("args 제대로 출력: ", args)
    for k in args: #차례로 받아오기
        #print("k이다 임마!: ", k)
        L.append(eval(k,lisp_to_python_dic))
            
        #print("이건 L이다", L)
    T.append(L)
    return T

def numberp_procedure(var):
    if isinstance(var,int) or isinstance(var,float):
        return True
    elif isinstance(var,str):
        if var in mem:
            if isinstance(mem[var],int) or isinstance(mem[var],float):
                return True
    return False

def zerop_procedure(var):
    if isinstance(var,int):
        if var == 0:
            return True
    elif isinstance(var,float): #int일때랑 합쳐줘도 되나?
        if var == 0:
            return True
    elif isinstance(var,str):
        if var in mem:
            if mem[var] == 0:
                return True
    else: #숫자가 아닐 때.. 사실 나중에 Error 처리 해줘야하는데 일단 False로
        return False        

def eval(x, dic):
    if isinstance(x, str):
        if x in mem:
            return mem[x]
        elif x in lisp_to_python_dic:
            return lisp_to_python_dic[x]
    elif not isinstance(x, list):
        return x
    elif x[0] == "'": # ["'" , "X"]
        if not isinstance(x[1],list):
            (_, exp) = x
            return exp
        else:
            return x

    elif x[0] == 'IF':
        (_, test, conseq, *alt) = x #alt 2개 이상이면 에러처리
        if eval(test, dic):
            exp = eval(conseq, dic)
        elif alt is None:
            return False
        else:
            exp = eval(alt, dic)
        return eval(exp, dic)
    
    elif x[0] == 'PRINT':
        (_, val) = x
        val = eval(val, dic)
        print(val)

    elif x[0] == 'define':
        (_, var, exp) = x
        dic[var] = eval(exp, dic)
    elif x[0] == 'SETQ':
        (_, var, exp) = x
        if isinstance(eval(exp,dic), list):
            mem[var] = eval(exp,dic)
            return mem[var]
        else:
            mem[var]=eval(exp,dic)
            return mem[var]
    elif x[0] == 'LIST':

        #print("리스트입니다!")
        (_, *args) = x
        #print("들어가는 args: ", args)
        return list_procedure(*args)
   

    elif x[0] == 'REVERSE':
        (_, reverseList) = x
        L = ["'"]
        exp = eval(reverseList, dic)
        if isList(exp)[0]:
            exp[1].reverse()
            L.append(exp[1])
            return L

    elif x[0] == 'ATOM':
        (_, exp) = x
        exp = eval(exp, dic)
        if isinstance(exp, list):
            return False
        elif isinstance(exp, int) or isinstance(exp, float):
            return True
        elif isinstance(exp,str):
            return True

    elif x[0] == 'NTH':
        (_, exp, nthList) = x
        if isList(eval(nthList, dic))[0]:  # true 이면
            if isList(eval(nthList, dic))[1] == 0:  # 직접 입력
                return eval(nthList, dic)[1][eval(exp, dic)]
            elif isList(eval(nthList, dic))[1] == 1:  # 저장된 리스트
                return mem[eval(nthList, dic)][eval(exp, dic)]
    elif x[0]=='CONS':
        (_, var, consList) = x
        T=["'"]
        L=[]
        var = eval(var, dic)
        consList = eval(consList, dic)
        print(var)
        if isinstance(var,int) or isinstance(var,float):
            L.append(var)
        elif isinstance(var, str):
            if var in mem:
                L.append(mem[var])
            L.append(var)
        elif isinstance(var, list):
            L.append(var)
            
        if isinstance(consList, str):
            if consList in mem:
                if mem[consList][0] == "'":
                    if isinstance(mem[consList][1], list):
                        L.extend(mem[consList][1])
                elif isinstance(mem[consList],int) or isinstance(mem[consList],float):
                    L.extend(mem[consList])
        elif isList(consList)[0]:  # true 이면
            if isList(consList)[1] == 0:  # 직접 입력
                L.extend(consList[1])
            elif isList(consList)[1] == 1:  # 저장된 리스트
                L.extend(mem[consList][1])
        T.append(L)
        return T

    elif x[0] == 'MEMBER':
        (_, word, memberList) = x
        if memberList in mem:
            memberList = mem[memberList][1]
            startIndex = memberList.index(word[1])
            return memberList[startIndex:]
    
    elif x[0]=='REMOVE':
        (_, var, exp)=x
        word=eval(var,dic)
        removeList=eval(exp,dic)
        print(removeList[1])
        while(True):
            try:
                removeList[1].remove(word)
            except ValueError:
                return removeList[1]
    
    elif x[0] == 'ASSOC':
        (_, key, assocList) = x 
        # assocList 예시 ["'", [["'", ['ONE', 1]], ["'", ['TWO', 2]], ["'", ['THREE', 3]]]]
        key = eval(key, dic)
        #assocTuple 예시 [["'", ['ONE', 1]]
        for assocTuple in assocList[1]:
            if key == assocTuple[1][0]:
                return assocTuple[1][1]
    
    elif x[0] == 'SUBST':
        (_, word, word_sub, substList) = x
        word = eval(word, dic)
        word_sub = eval(word_sub, dic)
        sub_idx = substList[1].index(word_sub)
        substList[1][sub_idx] = word
        return substList
    #     else:
    #         print("Error")
    
    
    elif x[0] == 'CAR':
        (_, carList) = x
        return CAR_procedure(carList, dic)
    
    elif x[0] == 'CDR':
        (_, cdrList) = x
        return CDR_procedure(cdrList, dic)

    elif x[0] == 'CADDR':
        (_, caddrList) = x
        return CAR_procedure(CDR_procedure(CDR_procedure ( caddrList, dic) , dic), dic)

    elif x[0] == 'REVERSE':
        (_, reverseList) = x
        L = ["'"]
        exp = eval(reverseList, dic)
        if isList(exp)[0]:
            exp[1].reverse()
            L.append(exp[1])
            return L
    elif x[0]=='LENGTH':
        (_,lengthList)=x
        if isList(lengthList)[0]:
            if isList(lengthList)[1]==0:
                return len(lengthList[1])
            elif isList(lengthList)[1]==1:
                return len(mem[lengthList][1])
        else :
            return False
    elif x[0] == 'NUMBERP':
        (_, var) = x
        return numberp_procedure(var)
    elif x[0] == 'ZEROP':
        (_, var) = x
        return zerop_procedure(var)
    elif x[0] == 'APPEND':
        (_, *args) = x
        appendedList = [] #들어온 리스트들을 모두 담아줄 리스트
        for exp in args:
            if isList(eval(exp,dic))[0]: #True면..
                if isList(eval(exp,dic))[1] == 0: # 직접 입력
                    for val in eval(exp,dic)[1]:
                        appendedList.append(val)
                elif isList(eval(exp,dic))[1]==1: #저장된 리스트
                    for val in mem[eval(exp,dic)][1]:
                        appendedList.append(val)
        T = ["'"]
        T.append(appendedList)
        return T
     ########## Predicate 함수 ############

    elif x[0] == 'NULL':
        (_, exp) = x
        if exp=='':
            return True
        L=eval(exp,dic)
        if isList(L)[0]:
            return L[1]==[]
        else:
            return False
    elif x[0] == 'MINUSP':
        (_, exp) = x
        exp = eval(exp, dic)
        if numberp_procedure(exp) == True:
            if exp < 0:
                return True
            else:
                return False
        else:
            print("Error")
    
    elif x[0] == 'EQUAL':
        (_, var1, var2)=x
        try:
            return eval(var1,dic)==eval(var2,dic)
        except TypeError:
            return False

    elif x[0] == '<':
        (_, var1, var2)=x
        try:
            return eval(var1,dic)<eval(var2,dic)
        except TypeError:
            return False

    elif x[0] == '>=':
        (_, var1, var2)=x
        try:
            return eval(var1,dic)>=eval(var2,dic)
        except TypeError:
            return False
        
            
    elif x[0] == 'lambda':
        (_, parms, body, *args) = x
        return lambda_procedure(parms, body, args)

    elif x[0] == 'STRINGP':
        (_,var)=x
        if isinstance(eval(x,dic),str):
            return True
        else:
            return False

    else:
        proc = eval(x[0], dic)
        args = [eval(exp, dic) for exp in x[1:]]
        try: return proc(args)
        except TypeError:
            args=[eval(exp,dic) for exp in x[0:]]
            return args

    

def main():
    while(True):
        userInput = input("> ")
        print(eval(expression_parser(userInput).pop(0), lisp_to_python_dic))

if __name__ == "__main__":
    main()