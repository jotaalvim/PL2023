import re

def parse(data,state,value): #False = OFF #True  = ON
    if not data: return state,value

    if re.search(r'^[oO][fF]{2}',data):
        data = data[3:]
        state = False

    if re.search(r'^[oO][nN]',data):
        data = data[2:]
        state = True

    if re.search(r'^=',data):
        data = data[1:]
        print("value =",value)

    match = re.match(r'^(-?\d+\.?\d*)',data)

    if state and (match != None):
        value += float(match.group(0))
        return parse(data[len(match.group(0)):],state,value)
    else: 
        return parse(data[1:],state,value)

a,b = True,0
while True:
    try:
        i = input()
        a,b = parse(i,a,b)
    except:
        break;
