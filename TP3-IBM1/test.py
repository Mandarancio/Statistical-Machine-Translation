import json
import ibm1
with open('tetas.json') as f:
    tetas = json.load(f)

t = "those guidelines are presented below .".split()
s = "más abajo figuran dichas directrices .".split()

print(tetas[s[0]][t[-1]])

tm = ibm1.IBM1(tetas)

print(tm.best_alignment(s,t))
