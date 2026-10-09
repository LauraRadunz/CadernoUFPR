import json,re,difflib,os
import numpy as np
from PIL import Image
d=json.load(open('Qall.json'))
def blank(f):
    p='img/'+f
    if not os.path.exists(p): return True
    a=np.asarray(Image.open(p).convert('L')).astype(float);return (a<200).mean()<0.02
for k in ('g1','g2','g2b','g3'):
    for q in d[k]['Q']: q['blocks']=[b for b in q['blocks'] if not(b[0]=='img' and blank(b[1]))]
def norm(q):
    t=" ".join(b[1] for b in q['blocks'] if b[0]!='img')+" "+" ".join(q['opts'])
    t=re.sub(r"\(.*?\)","",t,count=1)
    return re.sub(r"[^a-z0-9]","",t.lower())[:400]
ref=[norm(q) for k in('g1','g2','g3') for q in d[k]['Q']]
# g2b unit -> (caderno, unidade destino)
MAP={2:('g2',4),3:('g2',7),4:('g2',9),6:('g2',11),8:('g2',15),9:('g2',2),10:('g3',1),12:('g2',18),13:('g2',18),14:('g2',18),17:('g3',1)}
cnt={}
for k in('g2','g3'):
    for q in d[k]['Q']: cnt[(k,q['aula'])]=max(cnt.get((k,q['aula']),0),q['n'])
add={'g2':[],'g3':[]};stat={}
for q in d['g2b']['Q']:
    n=norm(q)
    if max(difflib.SequenceMatcher(None,n,r).ratio() for r in ref)>0.8: continue
    k,u=MAP[q['aula']]
    cnt[(k,u)]=cnt.get((k,u),0)+1
    q=dict(q);q['aula']=u;q['n']=cnt[(k,u)];q['id']="%d-%02d"%(u,q['n'])
    add[k].append(q);stat[(k,u)]=stat.get((k,u),0)+1
for k in add:
    d[k]['Q']+=add[k]
    d[k]['Q'].sort(key=lambda q:(q['aula'],q['n']))
d.pop('g2c',None)
json.dump(d,open('Qall.json','w'),ensure_ascii=False)
print(stat,{k:len(d[k]['Q']) for k in('g1','g2','g3')})
ids=[q['id'] for k in('g2','g3') for q in d[k]['Q']];print(len(ids),len(set(ids)))
