import logging
log = logging.getLogger()
log.setLevel('INFO')
def expValue(exp):
    global index
    result = termValue(exp)
    if index >= len(exp):
        return result
    more = True
    while more:
        op = exp[index]
        if op in '+-':
            index += 1
            value = termValue(exp)
            if op == '+':
                result += value
                if index>=len(exp):
                    more = False
            else:
                result -= value
                if index>=len(exp):
                    more = False
        else:
            more = False
    return result
def factorValue(exp):
    global index
    result = 0
    c = exp[index]
    if c == '(':
        index += 1
        result = expValue(exp)
        index += 1
    else:
        while c.isdigit():
            result = 10 * result + int(c) - 0
            index += 1
            if index>=len(exp):
                break
            c = exp[index]
            if exp[index]=='-' or exp[index]=='+':
                return result
    return result
def termValue(exp):
    global index
    result = factorValue(exp)
    if index >= len(exp):
        return result
    while True:
        if index >= len(exp):
            break
        op = exp[index]
        if op in '*/':
            index += 1
            value = factorValue(exp)
            if op == '*':
                result *= value
            else:
                result /= value
        else:
            break
    return result
def GetExpValue(L,P,H,exp):
    global index
    index = 0
    if not isinstance(L,str):
        L = str(int(L))
    if not isinstance(P, str):
        P = str(int(P))
    if not isinstance(H, str):
        H = str(int(H))
    log.info('EXP1= '+str(exp))
    EXP = exp.replace('L',L).replace('P',P).replace('H',H)
    result = expValue(EXP)
    log.info('result= '+str(result))
    return result
def main():
    GetExpValue(200, 540, 2100, 'L-18--1-20')