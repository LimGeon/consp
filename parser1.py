"""
제작자:
유효창 20190551
정설희 20193574
임  건 20192848

파일명: parser1.py
완료 날짜: 2020.12.06
"""
from functools import reduce
import re

parseCnt = 0



def bracket_parser(data): # ( 가 처음오면 잘라주기
    if data[0] == '(': 
        return [data[0], data[1:].upper()]

def quote_parser(data): # ' 가 처음 오면 -> (유무에 따라 심볼 or LIST
    if data[0] == "'": 
        if data[1] == '(': #그 다음에 ( 오면 -> LIST
            tmp = ["'"] # ' 추가해서 LIST 시작을 알림
            tmp2 = list_parser(data[2:]) # 괄호 다음 문자부터 list_parser로 넘겨주기
            tmp.append(tmp2[0]) #tmp2는 [list, index] 형식의 list / tmp에 tmp2[0] append
            return [tmp, data[tmp2[1]+2:]]
        else: #심볼처리
            atom_reg_ex = re.compile('\\w+') #문자 or 숫자
            atom_match = atom_reg_ex.match(data[1:]) #다음것부터.. 공백올때까지
            if atom_match:
                L = []
                L.append(data[0]) # ' 추가
                L.append(data[1:atom_match.end()+1].upper())
                return [L,data[atom_match.end()+1:]]    
            
def list_parser(data): #리스트 생성 # ( 다음 부터 불러옴..
    L = []
    index = 0
    while True:
        if(data[index] == '('): #새로운 리스트
            tmp = list_parser(data[index + 1:]) #괄호 다음부터 list_parser로 새로 돌리기
            T = ["'"]
            T.append(tmp[0])
            L.append(T)
            index = index + tmp[1]
        elif(data[index] == ')'): #리스트 끝
            index = index + 1
            return [L,index]
        elif data[index] not in ('\t','\n','\r','\f','\v'): #공백이 아니면
           list_reg_ex = re.compile('\\w+') #뒤에 문자 올때 쭉 (공백 or 특수기호 오면 cut)
           list_match = list_reg_ex.match(data[index:])
           if list_match:
               L.append(atom(data[index:list_match.end()+index].upper()))
               index = index + list_match.end()-1
        index = index + 1       


def space_parser(data): # 공백으로 시작하면f
    space_reg_ex = re.compile('\\s+') #공백과 매치
    space_match = space_reg_ex.match(data)
    if space_match:
        return [data[:space_match.end()], data[space_match.end():]]

def string_parser(data):
    string_reg_ex = re.compile('".+"')
    string_match = string_reg_ex.match(data)
    if string_match:
        return[data[:string_match.end()], data[string_match.end():]]
        

special_characters = ['#', '\\']
def special_parser(data):
     for item in special_characters:
        if data.startswith(item):
            return [data[:len(item)], data[len(item):]]

def number_parser(data): #숫자로 시작하면
    number_reg_ex = re.compile('\\d+\\.?\\d*')
    if data[0] == '-' and data[1].isdigit():
        data = data[1:]
        number_match = number_reg_ex.match(data)
        if number_match:
            return['-'+data[:number_match.end()], data[number_match.end():]]

    number_match = number_reg_ex.match(data)
    if number_match:
        return[data[:number_match.end()], data[number_match.end():]]

def comment_parser(data):
    commentIdx = data.find(';')
    return data[:commentIdx]

def identifier_parser(data):
    identifier_reg_ex = re.compile('\\w+')
    identifier_match = identifier_reg_ex.match(data)
    if identifier_match:
        return[data[:identifier_match.end()], data[identifier_match.end():]]

keywords_li = ['define', 'lambda', '*', '+', '-', '/', '<', '>', '<=', '>=', '%', 'if', '=',
               'length', 'abs', 'append', 'pow', 'min', 'max', 'round', 'not', 'quote','reverse']

def keyword_parser(data):
    for item in keywords_li:
        if data.startswith(item):
            return key_parser(data)

def declarator_parser(data):
    if data[:6] == 'define':
        return ['define', data[6:]]

def lambda_parser(data):
    if data[:6] == 'lambda':
        return ['lambda', data[6:]]

arithmetic_operators = ['*', '+', '-', '/', '%']

def arithemetic_parser(data):
    for item in arithmetic_operators:
        if data.startswith(item):
            return [data[:len(item)], data[len(item):]]

binary_operations = ['<=', '>=', '<', '>', '=', 'pow', 'append']

def binary_parser(data):
    for item in binary_operations:
        if data.startswith(item):
            return [data[:len(item)], data[len(item):]]

unary_operations = ['length', 'abs', 'round', 'not']

def unary_parser(data):
    for item in unary_operations:
        if data.startswith(item):
            return [data[:len(item)], data[len(item):]]

def if_parser(data):
    if data[:2] == 'if':
        return [data[:2], data[2:]]

def atom(s):
    try: return int(s)
    except TypeError:
        return s
    except ValueError:
        try: return float(s)
        except ValueError:
            return str(s)

def expression_parser(data,*depth):
    res = value_parser(data)
    rest = res.pop(1)
    token = res.pop(0)
    if depth:
        depth = depth[0]

    if token == '(':
        L = []
        try:
            while rest[0] != ')':
                if depth:
                    nex = expression_parser(rest,depth+1)
                else:
                    nex = expression_parser(rest)
                rest = nex.pop(1)
                token = nex.pop(0)

                if token[0] == ' ' or token == '\n':
                    continue
                L.append(atom(token))
        except:
            print("ERROR")
        rest = rest[1:]
        if depth:
            global parseCnt
            
            for i in range(1,3):
                parseCnt = parseCnt + 1
                print(str(parseCnt).rjust(2), "번째:","(파스트리 깊이:",depth,"): ", L[i])
            parseCnt = parseCnt + 1
            print(str(parseCnt).rjust(2), "번째:","(파스트리 깊이:",depth-1,"): ", L)
        return [L, rest]
    else:
        return [token, rest]

def any_one_parser_factory(*args):
    return lambda data: (reduce(lambda f, g: f if f(data)  else g, args)(data))

value_parser = any_one_parser_factory(space_parser, bracket_parser, quote_parser, string_parser, special_parser, 
                                    number_parser, keyword_parser, identifier_parser)
key_parser = any_one_parser_factory(declarator_parser, lambda_parser, if_parser,
                                    binary_parser, arithemetic_parser, unary_parser)

def main():
    while(True):
        global parseCnt
        parseCnt=0
        userInput = input("> ")

        userInput = comment_parser(userInput)
        print("\nparsing 과정 순서: ")
        print("\nparse 결과: ",expression_parser(userInput, 1))

if __name__ == "__main__":
    main()