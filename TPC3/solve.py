import os
import json
import re

with open('processos.txt','r') as f:
    data = f.readlines()

registos = []
for linha in data:
    m =  re.match( 
    r'(?P<pasta>[^:]*)::(?P<data>[^:]*)::(?P<nome>[^:]*)::(?P<pai>[^:]*)::(?P<mae>[^:]*)::(?P<observacoes>.*)::', linha)
    if m == None:
        print(linha)
    else :
        registos.append(m.groupdict())

# exercício a
os.system("awk -F:: '{print $2}' processos.txt | awk -F- '{print $1}' | sort | uniq -c")

# exercício b

seculos = {}
for reg in registos:
    ano = int( re.match(r'\d+', reg['data']).group())
    sec = ( ano // 100 ) + 1
    if sec not in seculos:
        seculos[sec] = {"proprio":{} , "apelido":{} }

    for nome in [ reg['nome'], reg['pai'], reg['mae'] ]:
        l = re.findall('(\w+)(?:\s+\w+\.?)*\s(\w+)',nome)
        if len(l) > 1:
            a,b = l[0]
            c,d = l[-1] #antigo l = [('Joaquina', 'Lages'), ('ou', 'Vilela')]
            l = [(a,d)] #novo l = [('Joaquina', 'Vilela')]

        if len(l) == 1:
            [(p,a)] = l
            if p not in seculos[sec]['proprio']:
                seculos[sec]['proprio'][p] = 1
            else:
                seculos[sec]['proprio'][p] += 1
            if a not in seculos[sec]['apelido']:
                seculos[sec]['apelido'][a] = 1
            else:
                seculos[sec]['apelido'][a] += 1

def pretyprint(s):
    for sec in s.keys():
        print('------------ Séc.',sec, '-------------')
        np = s[sec]['proprio']
        na = s[sec]['apelido']
        sna = sorted(na.items(),key=lambda x:x[1])
        snp = sorted(np.items(),key=lambda x:x[1])
        print('>>> Nomes próprios:')
        for nome,x in snp[-5:][::-1]:
            print(nome,"-",x)
        print('>>> Apelidos:')
        for nome,x in sna[-5:][::-1]:
            print(nome,"-",x)
        
pretyprint(seculos)
#print(seculos)

# exercício c FIXME
parentes = {}
for reg in registos:
    #print(reg['observacoes'])
    # modo não greedy
    l = re.findall(r'\,(\w+)(?:\s+\w+\.?)*\s(\w+)', reg['observacoes'])
    for gp in l:
        if gp in parentes:
            parentes[gp] += 1
        else:
            parentes[gp] = 1
#print(parentes)

    #"Sobrinho"
    #"Tio Materno"
    #"Tio Paterno"
    #"Tio Avo Materno"
    #"Tio Avo Paterno"
    #"Avo Materno"
    #"Avo Materno"
    #"Irmao"
    #"Irmaos"

# exercício d
with open("processos.json","w") as f:
    json.dump(registos[:20],f)
