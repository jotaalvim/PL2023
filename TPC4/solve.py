from pointfree import *
import json
import re

@pointfree
def fst(l): return l[0]
@pointfree
def media(l): return sum(l)/len(l)
@pointfree
def id(a): return a
@pointfree
def mysplit(p,a): return a.split(p)

@pointfree
def parse(line):
    return re.findall(r'(\w+)(?:{(?:(\d+),)?(\d+)})?(?:::(\w+))?', line)

def fill(field):
    n,i,m,f = field
    i = int (i) if i else 1
    m = int (m) if m else 1
    f = eval(f) if f else (id if m > 1 else fst)
    return n,i,m,f 

@pointfree
def makeDict(cab,linha):
    dic = {}
    linha = linha.strip()
    for n,i,m,f in cab:
        ion = int if m > 1 else id         #int or not
        match = re.match(rf'([^,]*,?){{{i},{m}}}', linha).group()
        parse = f * pfcollect * pfmap (ion) * pffilter(lambda l: l!='') * mysplit (',')
        dic[n] = parse (match)
        linha = linha [len(match):]
    return dic

path = "alunos5.csv"
with open(path,'r') as f:
    head, *lines = f.readlines()
    l1 = pfcollect * pfmap(fill) * parse
    cabecalho = l1 (head)
    ll = [makeDict(cabecalho,line) for line in lines]

with open(path[:-4]+'.json','w') as f:
    json.dump(ll,f)
    #ld = pfcollect *  pfmap( lambda x : makeDict(x) ) * pfmap (lambda l : (cabecalho ,l))
