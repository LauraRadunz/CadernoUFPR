import json,re,difflib
d=json.load(open('Qall.json'))
def norm(q):
    t=" ".join(b[1] for b in q['blocks'] if b[0]!='img')+" "+" ".join(q['opts'])
    t=re.sub(r"\(.*?\)","",t,count=1)
    return re.sub(r"[^a-z0-9]","",t.lower())[:300]
ref=[norm(q) for q in d['m2']['Q']]
units=d['m2']['units']
def target(n):
    for u in units:
        if u['n']==n or (u['n2'] and n in u['n2']): return u['n']
    return None
cnt={}
for q in d['m2']['Q']: cnt[q['aula']]=max(cnt.get(q['aula'],0),q['n'])
add=[];info=[]
for q in d['m2b']['Q']:
    if not q.get('ans'): continue
    n=norm(q);best=max(difflib.SequenceMatcher(None,n,r).ratio() for r in ref)
    if best>0.8: continue
    t=target(q['aula'])
    if t is None: info.append(('sem destino',q['id']));continue
    cnt[t]=cnt.get(t,0)+1
    q=dict(q);info.append((q['id'],'->',t,round(best,2)));q['aula']=t;q['n']=cnt[t];q['id']="%d-%02d"%(t,q['n']);add.append(q)
d['m2']['Q']+=add;d['m2']['Q'].sort(key=lambda q:(q['aula'],q['n']))
json.dump(d,open('Qall.json','w'),ensure_ascii=False)
print(info)
