import re
import ply.lex as lex

sample1 = """
/* factorial.p
-- 2023-03-20 
-- by jcr
*/

int i;

// Função que calcula o factorial dum número n
function fact(n){
  int res = 1;
  while res > 1 {
    res = res * n;
    res = res - 1;
  }
}

// Programa principal
program myFact{
  for i in [1..10]{
    print(i, fact(i));
  }
}
"""

sample2 = """
/* max.p: calcula o maior inteiro duma lista desordenada
-- 2023-03-20 
-- by jcr
*/

int i = 10, a[10] = {1,2,3,4,5,6,7,8,9,10};

// Programa principal
program myMax{
  int max = a[0];
  for i in [1..9]{
    if max < a[i] {
      max = a[i];
    }
  }
  print(max);
}
"""

tokens = (
   'NUMBER',
   'PLUS',
   'FUNCTION',
   'MINUS',
   'TIMES',
   'DIVIDE',
   'LPAREN',
   'RPAREN',
   'LBRACKET',
   'RBRACKET',
   'LLIST',
   'RLIST',
   'PALAVRA',
   'ATRIB',
)

t_PLUS     = r'\+'
t_MINUS    = r'-'
t_TIMES    = r'\*'
t_DIVIDE   = r'/'
t_LPAREN   = r'\('
t_RPAREN   = r'\)'
t_LBRACKET = r'\{'
t_RBRACKET = r'\}'
t_LLIST    = r'\['
t_RLIST    = r'\]'
t_PALAVRA  = r'\w+'
t_ATRIB    = r'='

t_ignore = "\n \t"
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)    
    return t

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

def rmComments(code):
    code = re.sub( r'/\*(.|\n)*?\*/', r'',code)
    code = re.sub( r'//.*', r'',code)
    return code

abc = rmComments(sample1)

lexer = lex.lex()
lexer.input(abc)

# Tokenize
while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input
    print(tok)
