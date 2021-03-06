"""
제작자:
유효창 20190551
정설희 20193574
임  건 20192848

파일명: interpreter.py
완료 날짜: 2020.12.06
"""

# interpreter
#import module
import sys
import math
import operator as op
from functools import reduce
from parser1 import expression_parser

mem = {}  # SETQ를 통한 변수 저장을 위한 딕셔너리



def CAR_procedure(carList):
    if isList(eval(carList))[0]:  # true 이면
        if isList(eval(carList))[1] == 0:  # 직접 입력
            return eval(carList)[1][0]  # 리스트의 첫번째 원소 return (원소)
        elif isList(eval(carList))[1] == 1:  # 저장된 리스트
            return mem[eval(carList)][1][0]  # 리스트의 첫번째 원소 return (원소)


def CDR_procedure(cdrList):
    if isList(eval(cdrList))[0]:  # true 이면
        if isList(eval(cdrList))[1] == 0:  # 직접 입력
            T = ["'"]  # 리스트임을 나타내기 위한 quote
            T.append(eval(cdrList)[1][1:])  # 리스트의 두번째 원소부터 return (리스트 형식)
            return T  # 리스트 return
        elif isList(eval(cdrList))[1] == 1:  # 저장된 리스트
            T = ["'"]  # 리스트임을 나타내기 위한 quote
            T.append(mem[eval(cdrList)][1][1:])  # 리스트의 두번째 원소부터 return (리스트 형식)
            return T  # 리스트 return

def isList(vlist):  # 리스트인지 확인하기 위한 함수 -> 리스트 형식이고 첫번째 원소 값이 '인 경우에 -> 심볼인지 리스트인지
    if isinstance(vlist, list):  # 리스트 형식이면
        if vlist[0] == "'":
            if isinstance(vlist[1], list):
                return [True, 0]  # 직접 list 입력
    elif isinstance(vlist, str):  # str 형식이면 -> mem에 저장된 변수인지 확인 -> 저장되어있다면 그에 맞는 value값 list형인지 확인
        if vlist in mem:
            if mem[vlist][0] == "'" and isinstance(mem[vlist][1], list):
                return [True, 1]  # mem에 저장되어있는 list


def list_procedure(*args):
    T = ["'"]
    L = []
    # print("args 제대로 출력: ", args)
    for k in args:  # 차례로 받아오기
        if eval(k) == None:
            print("ERROR : 잘못된 입력값")
            main()
        L.append(eval(k))
    T.append(L)
    return T


def numberp_procedure(var):
    if isinstance(var, bool):
        return False
    elif isinstance(var, int) or isinstance(var, float):
        return True
    elif isinstance(var, str):
        if var in mem:
            if isinstance(mem[var], int) or isinstance(mem[var], float):
                return True
    return False


def zerop_procedure(var):  # var이 0인지 판별
    # int나 float 형일때는 그 자체를 0과 비교
    if isinstance(var, int):
        if var == 0:
            return True
    elif isinstance(var, float):
        if var == 0:
            return True
    elif isinstance(var, str):  # str 형식이면 -> mem에 저장된 변수인지 확인 -> 저장되어있다면 그의 value값 0인지 check
        if var in mem:
            if mem[var] == 0:
                return True
    else:  # 숫자 및 스트링이 아닐 때.. 사실 나중에 Error 처리 해줘야하는데 일단 False로
        return False

    ########################### eval 함수 - 핵심 ###########################################


def eval(x):
    if isinstance(x, str):
        #print("dfj",x[:7])
        if x in mem:
            return mem[x]
        #elif x in lisp_to_python_dic:
            #return lisp_to_python_dic[x]
        elif x[0] == '"' and x[-1] == '"':
            return x
        else:
            return False
            # else: #quote가 붙여져 있지도 않고, mem에 저장도 안된것..
        #     print("ERROR : 저장된 변수가 아닙니다..ㅠ"
    elif not isinstance(x, list):
        return x
    elif x[0] == "'":  # ["'" , "X"]
        if not isinstance(x[1], list):
            (_, exp) = x
            return exp
        else:
            return x
    elif x[0] == '+':
        (_, *args) = x
        tmp = 0
        for i in args:
            i = eval(i)
            if isinstance(i, int) or isinstance(i, float):  # 숫자일때
                tmp = tmp + i
            else:
                print("ERROR : 올바르지 않은 자료형!")
                main()
        return tmp

    elif x[0] == '-':
        (_, *args) = x
        tmp = 0
        index = 0
        for i in args:
            index = index + 1
            i = eval(i)
            if isinstance(i, int) or isinstance(i, float):  # 숫자일때
                if index == 1:  # 첫번째 원소일때
                    tmp = tmp + i
                else:
                    tmp = tmp - i
            else:
                print("ERROR : 올바르지 않은 자료형!")
                main()
        return tmp

    elif x[0] == '*':
        (_, *args) = x
        tmp = 0
        index = 0
        for i in args:
            index = index + 1
            i = eval(i)
            if isinstance(i, int) or isinstance(i, float):  # 숫자일때
                if index == 1:  # 첫번째 원소일때
                    tmp = tmp + i
                else:
                    tmp = tmp * i
            else:
                print("ERROR : 올바르지 않은 자료형!")
                main()
        return tmp


    elif x[0] == '/':
        (_, *args) = x
        tmp = 0
        index = 0
        for i in args:
            index = index + 1
            i = eval(i)
            if isinstance(i, int) or isinstance(i, float):  # 숫자일때
                if index == 1:  # 첫번째 원소일때
                    tmp = tmp + i
                else:
                    if i == 0:
                        print("ERROR : 0으로 나눌 순 없어용")
                        main()
                    else:
                        tmp = tmp / i
            else:
                print("ERROR : 올바르지 않은 자료형!")
                main()
        return tmp

    elif x[0] == 'IF':  
        (_, test, conseq, *alt) = x
        if len(alt) >= 2:  # alt 2개 이상이면 에러처리
            print("ERROR : 입력값이 너무 많아요 ㅠㅠ")
            main()
        if not isinstance(eval(test), bool):
            print("ERROR : 조건문에 잘못된 조건식이 들어가있어요~")
            main()
        if eval(test): # 조건문이 참이라면 아래 명령 수행
            return eval(conseq)
        elif alt == []: # 위의 eval에서 True가 안나오면 Else에 가야하는데 alt가 없을 때는 FALSE를 반환
            return False 
        else: # else를 실행해야하고 alt가 있는 경우에는 alt 내용을 수행
            exp = eval(alt[0])
        return eval(exp)
    
    elif x[0] == 'COND':
        (_, *ifexp) = x
        if(len(ifexp)<1):
            print("ERROR : 조건식이 없어요")
            main()
        for exp in ifexp:
            test = exp[0]
            if not isinstance(eval(test), bool):
                print("ERROR : 조건문에 잘못된 조건식이 들어가있어요~")
                main()
            conseq = exp[1]
            if eval(test):
                return eval(conseq)

    elif x[0] == 'PRINT':
        (_, val) = x
        val = eval(val)
        print(val)
        return val


    elif x[0] == 'SETQ':  # argument 2개 아니면 error
        # 입력값 2개 아니면 에러 처리
        (_, *inputcheck) = x
        if len(inputcheck) < 2:
            print("ERROR : 입력값이 너무 적어요 ㅠㅠ")
            main()
        elif len(inputcheck) > 2:
            print("ERROR : 입력값이 너무 많아요 ㅠㅠ")
            main()
        (_, var, exp) = x
        if not isinstance(var, str):  # 스트링이 아니면 에러처리
            print("ERROR : 입력값이 잘못됐어요.. (변수)")
            main()
        mem[var] = eval(exp)
        return mem[var]

    elif x[0] == 'LIST':
        (_, *args) = x
        return list_procedure(*args)

    elif x[0] == 'ATOM':
        (_ , *args) = x
        if (len(args) != 1):
            return "ERROR : 입력 값은 1개여야 합니다."
        (_, exp ,*args) = x

        exp = eval(exp)
        if isinstance(exp, list):
            return False
        elif isinstance(exp, int) or isinstance(exp, float):
            return False
        elif isinstance(exp, str):
            return True
    elif x[0] == 'NTH':
        (_ , *args) = x
        if (len(args) != 2):
            return "ERROR : 입력 값의 개수가 잘못되었습니다."
        (_, exp, nthList) = x
        if not isinstance(eval(exp), int):
            print("ERROR : index 입력이 잘못되었습니다")
            main()
        elif not isList(eval(nthList)):
            print("ERROR : 입력 형태가 잘못되었습니다.")
            main()
        elif isList(eval(nthList))[0]:  # true 이면
            if isList(eval(nthList))[1] == 0:  # 직접 입력
                try:
                    return eval(nthList)[1][eval(exp)]
                except IndexError:
                    return False
            elif isList(eval(nthList))[1] == 1:  # 저장된 리스트
                try:
                    return mem[eval(nthList)][eval(exp)]
                except IndexError:
                    print("ERROR: Index에 벗어났습니다")
                    main()

    elif x[0] == 'CONS':
        (_, *args) = x
        if(len(args)!=2):
            return "ERROR : 입력이 잘못되었습니다"
        (_, var, consList) = x

        T = ["'"]
        L = []
        var = eval(var)
        consList = eval(consList)
        # print(var)
        if (var == None) or (consList == None):
            print("ERROR : 잘못된 입력값!")
            main()
        else:
            L.append(var)
        if isList(consList)[0]:
            if isList(consList)[1] == 0:
                for val in consList[1]:
                    L.append(val)
            elif isList(consList)[1] == 1:
                for val in consList[1]:
                    L.append(val)
        T.append(L)
        return T
    elif x[0] == 'MEMBER':
        (_, *args) = x
        if(len(args) != 2):
            return "ERROR : 입력 인자의 개수가 잘못되었습니다."
        (_, word, memberList) = x
        T = ["'"]
        word = eval(word)
        memberList = eval(memberList)
        try:
            startIndex = memberList[1].index(word)
            T.append(memberList[1][startIndex:])
            return T
        except:
            return False

    elif x[0] == 'REMOVE':
        (_, *args) = x
        if(len(args)!=2):
            return "ERROR : 입력된 인자의 개수가 잘못되었습니다."
        (_, var, exp) = x
        L = ["'"]
        word = eval(var)
        removeList = eval(exp)
        while (True):
            try:
                removeList[1].remove(word)
            except ValueError:
                L.append(removeList[1])
                return L

    elif x[0] == 'ASSOC':
        (_, *args) = x
        if (len(args)!= 2):
            return "ERROR : 입력된 인자의 개수가 잘못되었습니다."
        (_, key, assocList) = x
        # assocList 예시 ["'", [["'", ['ONE', 1]], ["'", ['TWO', 2]], ["'", ['THREE', 3]]]]
        key = eval(key)
        assocList = eval(assocList)
        #assocTuple 예시 [["'", ['ONE', 1]]
        for assocTuple in assocList[1]:
            if key == eval(assocTuple)[1][0]:
                return eval(assocTuple)
        print("ERROR : 리스트 안에 찾고자하는 key 값이 없네요........")
        main()
    
    elif x[0] == 'SUBST':
        (_,*args) = x
        if(len(args)!=3):
            return "ERROR : 입력된 인자의 개수가 잘못되었습니다."
        (_, word, word_sub, substList) = x
        word = eval(word)
        word_sub = eval(word_sub)
        substList = eval(substList)
        try:
            sub_idx = substList[1].index(word_sub)
            substList[1][sub_idx] = word
            return substList
        except:
            print("ERROR : 대체하고자 하는 단어가 리스트 안에 없네요.....")
            main()
    #     else:
    #         print("Error")

    elif x[0] == 'CAR':
        (_, carList) = x
        return CAR_procedure(carList)

    elif x[0] == 'CDR':
        (_, cdrList) = x
        return CDR_procedure(cdrList)

    elif x[0] == 'CADDR':
        (_, caddrList) = x
        return CAR_procedure(CDR_procedure(CDR_procedure(caddrList)))

    elif x[0] == 'REVERSE':
        (_, *args) = x
        if(len(args)!=1):
            return "ERROR : 입력 인자의 개수가 잘못되었습니다."
        (_, reverseList) = x
        exp = eval(reverseList)
        if not isList(exp):
            print("ERROR : 입력이 잘못 되었습니다")
            #main()
        L = ["'"]
        if isList(exp)[0]:
            exp[1].reverse()
            L.append(exp[1])
            return L

    elif x[0] == 'LENGTH':
        (_, *args) = x
        if(len(args) != 1):
            return "ERROR : 입력 인자의 개수가 잘못되었습니다"
        (_, lengthList) = x
        if not isList(eval(lengthList)):
            print("ERROR : 입력이 잘못되었습니다")
            main()
        if isList(eval(lengthList))[0]:
            if isList(eval(lengthList))[1] == 0:
                return len(eval(lengthList)[1])
            elif isList(eval(lengthList))[1] == 1:
                return len(mem[eval(lengthList)][1])
    elif x[0] == 'NUMBERP':
        (_, var) = x
        return numberp_procedure(var)
    elif x[0] == 'ZEROP':
        (_, var) = x
        return zerop_procedure(var)
    elif x[0] == 'APPEND':
        (_, *args) = x
        if len(args)==0: #입력값이 0개일 때
            print("ERROR : 입력이 너무 적습니다")
            main()
        appendedList = []  # 들어온 리스트들을 모두 담아줄 리스트
        for exp in args:
            if (eval(exp)) == None:
                print("ERROR : 리스트가 아닌 다른 값이 입력되었습니다")
                main()
            elif isList(eval(exp))[0]:  # True면..
                if isList(eval(exp))[1] == 0:  # 직접 입력
                    for val in eval(exp)[1]:
                        appendedList.append(val)
                elif isList(eval(exp))[1] == 1:  # 저장된 리스트
                    for val in mem[eval(exp)][1]:
                        appendedList.append(val)
        T = ["'"]
        T.append(appendedList)
        return T
    ########## Predicate 함수 ############
    elif x[0] == 'NULL':
        (_, exp) = x
        exp = eval(exp)
        if exp == False:
            return True
        if type(exp) == LIST:
            if isList(exp)[0]:
                return exp[1] == []
        else:
            return False
    elif x[0] == 'MINUSP':
        (_, exp) = x
        exp = eval(exp)
        if numberp_procedure(exp) == True:
            if exp < 0:
                return True
            else:
                return False
        else:
            print("ERROR : 숫자를 입력하세요")
            main()

    elif x[0] == 'EQUAL':
        (_, var1, var2, *args) = x
        if(len(args)>0):
            print("ERROR : 인자 입력이 잘못되었습니다")
            main()
        try:
            if eval(var1) == eval(var2):
                return True
            else:
                return False
        except TypeError:
            print("ERROR : 맞는 형태가 아닙니다")
            main()

    elif x[0] == '<':
        (_, var1, var2, *args) = x
        if (len(args) > 0):
            print("ERROR : 인자 입력이 잘못되었습니다")
            main()
        try:
            if eval(var1) < eval(var2):
                return True
            else:
                return False
        except TypeError:
            print("ERROR : 맞는 형태가 아닙니다")
            main()

    elif x[0] == '>':
        (_, var1, var2, *args) = x
        if (len(args) > 0):
            print("ERROR : 인자 입력이 잘못되었습니다")
            main()
        try:
            if eval(var1) > eval(var2):
                return True
            else:
                return False
        except TypeError:
            print("ERROR : 맞는 형태가 아닙니다")
            main()

    elif x[0] == '=':
        (_, var1, var2, *args) = x
        if (len(args) > 0):
            print("ERROR : 인자 입력이 잘못되었습니다")
            main()
        try:
            if eval(var1) == eval(var2):
                return True
            else:
                return False
        except TypeError:
            print("ERROR : 맞는 형태가 아닙니다")
            main()

    elif x[0] == '>=':
        (_, var1, var2, *args) = x
        if (len(args) > 0):
            print("ERROR : 인자 입력이 잘못되었습니다")
            main()
        try:
            if eval(var1) >= eval(var2):
                return True
            else:
                return False
        except TypeError:
            print("ERROR : 맞는 형태가 아닙니다")
            main()

    elif x[0] == 'STRINGP':
        (_, *var) = x
        if (len(var) >= 2):
            return False
        if isinstance(eval(var[0]), str):
            if len(eval(var[0])) > 2:
                if eval(var[0])[0] == '"' and eval(var[0])[-1] == '"':
                    return True
        return False

    # else:
    #     print("ERROR : 올바르지 않은 자료형!"
    # proc = eval(x[0], dic)
    # args = [eval(exp, dic) for exp in x[1:]]
    # try: return proc(args)
    # except TypeError:
    #     args=[eval(exp,dic) for exp in x[0:]]
    #     return args


def printlist(l):
    if l[0] == "'" and isinstance(l[1], list):
        tmp = "("
        index = 0
        for i in l[1]:
            index = index + 1
            if not isinstance(i, list):  # 리스트가 아닌 경우
                if isinstance(i, str):
                    if index != 1:
                        tmp = tmp + " " + i
                    else:
                        tmp = tmp + i
                else:
                    if index != 1:
                        tmp = tmp + " " + str(i)
                    else:
                        tmp = tmp + str(i)
            else:  # 리스트인 경우
                if index != 1:
                    tmp = tmp + " " + printlist(i)
                else:
                    tmp = tmp + printlist(i)

        tmp = tmp + ")"
        return tmp
        
def rightPrint(rv):
    if isinstance(rv, list):  # 리스트면
        print(printlist(rv))
    elif isinstance(rv, bool):
        if rv == False:
            print("NIL")
        elif rv == True:
            print("T")
    elif rv == None:
        print("Error : 잘못된 입력 값!")
    else:  # 리스트가 아니면
        print(rv)

f = "input file"
savedLine = 0
eof = False

def main():
    
    try: #명령어를 파일로 입력받을 시
        f=open(sys.argv[1],'r', encoding='UTF8')
        datas = f.readlines()
        nowLine = 0
        global eof
        global savedLine
        for line in datas:
            if savedLine <= nowLine:
                savedLine = savedLine + 1
                if line[-1] == '\n' or line[-1] == '\t':
                    line=line[:-1]
                if line:
                    print(">",line)
                    rv = eval(expression_parser(line).pop(0))
                    if not eof:
                        rightPrint(rv)
            nowLine = nowLine + 1
        eof = True
        f.close()
    except: #파일 없이 실행시킬 경우 인터프리터 작동
        while True:
            line = input('> ')
            rv = eval(expression_parser(line).pop(0))
            rightPrint(rv)

if __name__ == "__main__":
    main()