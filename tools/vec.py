import math
BLUE=(0.0,0.447,0.753)
def _bb(o):return [o["x0"],o["top"],o["x1"],o["bottom"]]
def vec_clusters(pg,gtop=None,gcol=None,natives=()):
    objs=[]
    for o in pg.lines+pg.rects+pg.curves:
        if o["top"]<52 or o["bottom"]>795 or o["x1"]-o["x0"]>300 or o["bottom"]-o["top"]>400: continue
        nsc=o.get("non_stroking_color");sc=o.get("stroking_color")
        if o["object_type"]=="rect" and (o["x1"]-o["x0"])>150 and nsc in (1.0,(1.0,1.0,1.0),[1.0,1.0,1.0],1): continue
        def isblue(c):
            try:return c is not None and len(c)==3 and all(abs(a-b)<0.02 for a,b in zip(c,BLUE))
            except Exception:return False
        if isblue(nsc) or isblue(sc): continue
        col=0 if o["x0"]<298 else 1
        if gtop is not None and col==gcol and o["top"]>=gtop-3: continue
        w=o["x1"]-o["x0"];h=o["bottom"]-o["top"]
        if w<0.3 and h<0.3: continue
        objs.append(o)
    # union-find by expanded bbox overlap
    n=len(objs);par=list(range(n))
    def f(i):
        while par[i]!=i:par[i]=par[par[i]];i=par[i]
        return i
    E=7
    for i in range(n):
        a=objs[i]
        for j in range(i+1,n):
            b=objs[j]
            if a["x0"]-E<=b["x1"] and b["x0"]-E<=a["x1"] and a["top"]-E<=b["bottom"] and b["top"]-E<=a["bottom"]:
                par[f(i)]=f(j)
    cl={}
    for i,o in enumerate(objs):cl.setdefault(f(i),[]).append(o)
    out=[]
    for os_ in cl.values():
        x0=min(o["x0"] for o in os_);x1=max(o["x1"] for o in os_);t=min(o["top"] for o in os_);b=max(o["bottom"] for o in os_)
        def diag(o):
            w=o["x1"]-o["x0"];h=o["bottom"]-o["top"]
            return o["object_type"]=="curve" or (w>0.8 and h>0.8 and o["object_type"]=="line")
        nd=sum(1 for o in os_ if diag(o));nh=sum(1 for o in os_ if (o["bottom"]-o["top"])<0.8 and (o["x1"]-o["x0"])>2);nv=sum(1 for o in os_ if (o["x1"]-o["x0"])<0.8 and (o["bottom"]-o["top"])>2)
        ok=(nd>=1 and len(os_)>=3) or (nh>=3 and nv>=3 and len(os_)>=10)
        if nh>=5 and nd==0 and nv<=3 and (x1-x0)>180: ok=False   # caixa de rascunho
        if (x1-x0)<8 and (b-t)<8: ok=False
        if not ok: continue
        if any(not(x1<nb[0] or x0>nb[2] or b<nb[1] or t>nb[3]) for nb in natives): continue
        out.append((x0-4,t-4,x1+4,b+4))
    return out
