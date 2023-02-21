import matplotlib.pyplot as plt
import re

file = open("myheart.csv", "r")

content = file.read()

linhas = content.splitlines()[1:]

def parse(linhas):
    lista = []
    for line in linhas:
        idade,sexo,tensao,colesterol,batimento,temDoenca = line.split(',')
        dic = dict()
        dic["idade"]      = int(idade)
        dic["sexo"]       = sexo
        dic["tensao"]     = int(tensao)
        dic["colesterol"] = int(colesterol)
        dic["batimento"]  = int(batimento)
        dic["temDoenca"]  = bool(int(temDoenca))
        lista.append(dic)
    return lista


def draw(names):
    def _draw(values):
        plt.figure(figsize=(8, 3))
        plt.bar(names, values)
        #plt.suptitle('sexo por doença')
        return plt.show()
    return _draw

             # todos :: [dict]
def exercicio1(todos: list) -> (list,list):
    #print(re.findall(r'\d+,([MF]),\d+,\d+,\d+,(\d)',content))
    s = {'M':0,'F':0}
    for dic in todos:
        sexo = dic["sexo"]
        doenca = dic["temDoenca"]
        if doenca:
            s[sexo] +=1

    return s.keys(),s.values()
    #awk -F, '$2 == "M" {a++} END {print a}' myheart.csv
    #670

    #awk -F, '$2 == "M" {a+=$6} END {print a}' myheart.csv
    #428

    #grep M myheart.csv | grep -P -c '1\s*$'

def exercicio2(todos:list) -> (list, list):
    aux = {}
    for dic in todos:
        idade = dic["idade"]
        doenca = dic["temDoenca"]
        if doenca:
            i = idade // 5
            aux[i] = aux[i] + 1 if i in aux else 1

    names = []
    mk = max(aux.keys())
    values = [ aux.get(n,0)   for n in range(mk) ]
    a = 0
    while a < mk * 5:
        names.append( str([a,a+4]) )
        a+= 5

    return names, values

def exercicio3(todos:list) -> (list, list):
    aux = {}
    for dic in todos:
        col = dic["colesterol"]
        doenca = dic["temDoenca"]
        if doenca:
            i = col // 10
            aux[i] = aux[i] + 1 if i in aux else 1
    names = []
    mk = max(aux.keys())
    aux[0] = 0               # não vale ter colesterol a 0
    values = [ aux.get(n,0)   for n in range(mk) ]
    a = 0
    while a < mk * 10:
        names.append( str([a,a+9]) )
        a+= 10
    return names, values


todos = parse(linhas)

#a,b = exercicio1(todos)

a,b = exercicio2(todos)

#a,b = exercicio3(todos)

draw(a) (list(b))
