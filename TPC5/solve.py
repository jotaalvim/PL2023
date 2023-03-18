import ply.lex as lex
import sys
import re
#ply usa o módulo re em modo VERBOSE por default
# ordena as expressoes regulares pelo cumprimento por ordem decrescentemente

#(euros,centimos)
money = (0,0)

def liga(custo):
    global money
    em,cm = money
    e,c = custo
    nc = cm - c
    if cm - c < 0:
        nc = cm - c + 100
        ne = em - e -1
    else:
        nc = abs(cm - c)
        ne = em - e 
    money = (ne,nc)
    return  f'saldo : {ne}e{nc}c'

def saldo(euro:list,cent:list):
    global money
    a,b = money
    c = (sum(cent) + b) % 100
    e = sum(euro) + c  // 100
    money = (e+a,c) 
    return  f'saldo : {e+a}e{c}c'

tokens = (
    'LEVANTAR',
    'POUSAR',
    'MOEDA',
    'TELEMOVEL'
)

t_ANY_ignore= "\n \t"

states = ( ('ligado' ,'exclusive'),)

def t_INITIAL_LEVANTAR(t) :  
    r'LEVANTAR'
    print("Bem vindo!")
    t.lexer.begin('ligado')

def t_ligado_POUSAR(t):  
    r'POUSAR'
    print("Até à próxima")
    ne,nc = money
    print( 'vou devolver: ' + f'{ne}e{nc}c')
    t.lexer.begin('INITIAL')


def t_ligado_MOEDA(t):  
    r'MOEDA.*'
    print("a ler moedas...")
    cent  = [ int(i)  for i,c in re.findall(r'\b(50|20|10|5|2|1)(c)', t.value) ]
    euro  = [ int(i)  for i,c in re.findall(r'\b(2|1)(e)', t.value) ]
    print(saldo(euro,cent))

def t_ligado_TELEMOVEL(t):  
    r'T=\d+'
    num = re.findall(r'T=(\d+)',t.value)[0]
    a,b = money
    custo = (0,0)
    if len(num) != 11 and num[0:2] == "00":
        print("número inválido")
    elif len(num) != 9 and num[0:2] != "00":
        print("número inválido")
    elif num[0:3] in ["601","604"]:
        print("Chamada bloqueada, volte a colocar um número")
    elif num[0:2] == "00" and (a+(b/100) < 1.5):
        print("Precisa no mínimo de 1.5 euros")
    elif num[0]   == "2" and (a+(b/100) < 0.25):
        print("Precisa no mínimo de 25 centimos")
    elif num[0:3] == "808":
        custo = (0,10)
        print(liga(custo))
    elif num[0:2] == "00" : 
        custo = (1,50)
        print(liga(custo))
    elif num[0]   == "2"  : 
        custo = (0,25)
        print(liga(custo))
    else:
        print(liga(custo))

def t_ANY_error(t): print(f'Syntax error in input!, "{t.value}" ')

lexer = lex.lex()

#for linha in sys.stdin:
#    lexer.input(linha)
#    lexer.token()

data = """
LEVANTAR
MOEDA 20c, 2c 10c, 1e, 3e 25c
MOEDA 1e.
T=00934662832
T=00934662832
POUSAR"""

lexer.input(data)
lexer.token()

