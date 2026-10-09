import pdfplumber,json,re,io,sys,os,statistics,subprocess
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from vec import vec_clusters
from PIL import Image
SUP=dict(zip("0123456789+-−()nx=","⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁻⁽⁾ⁿˣ⁼"))
SUB=dict(zip("0123456789+-−()nxeaoh=","₀₁₂₃₄₅₆₇₈₉₊₋₋₍₎ₙₓₑₐₒₕ₌"))
OBJ={}
def load_obj(pdf,pref):
    import subprocess,glob
    raw="raw/"+pref
    os.makedirs(raw,exist_ok=True)
    if not glob.glob(raw+"/i-*"): subprocess.run(["pdfimages","-all",pdf,raw+"/i"],check=True,capture_output=True)
    lst=subprocess.run(["pdfimages","-list",pdf],capture_output=True,text=True).stdout.split("\n")[2:]
    files=sorted(glob.glob(raw+"/i-*"))
    idx={int(re.search(r"i-(\d+)",f).group(1)):f for f in files}
    for l in lst:
        t=l.split()
        if len(t)>10 and t[2]=="image": OBJ[(pref,int(t[10]))]=idx.get(int(t[1]))
def save_img(im,path,pref):
    try:
        f=OBJ.get((pref,im["stream"].objid))
        if not f: return False
        img=Image.open(f).convert("RGB")
        if img.width>720: img=img.resize((720,round(img.height*720/img.width)),Image.LANCZOS)
        from PIL import ImageStat
        if max(ImageStat.Stat(img.convert("L")).stddev)<7: return False
        img.save(path,"JPEG",quality=82,optimize=True);return True
    except Exception as e:
        print("imgfail",path,e);return False
def build_lines(chars):
    main=[c for c in chars if c["size"]>=8];small=[c for c in chars if 4<=c["size"]<8]
    main.sort(key=lambda c:(c["top"],c["x0"]));L=[]
    for c in main:
        if L and abs(c["top"]-L[-1]["top"])<=3.5: L[-1]["ch"].append(c)
        else: L.append(dict(top=c["top"],ch=[c]))
    for l in L:
        l["base"]=statistics.median(c["bottom"] for c in l["ch"]);l["x0"]=min(c["x0"] for c in l["ch"]);l["x1"]=max(c["x1"] for c in l["ch"])
    for c in small:
        best=None
        for l in L:
            if l["x0"]-3<=c["x0"]<=l["x1"]+3:
                d=abs((c["top"]+c["bottom"])/2-(l["base"]-4))
                if d<8 and (best is None or d<best[0]): best=(d,l)
        if best:
            l=best[1];c=dict(c);cb=c["bottom"]
            c["mode"]="sup" if cb<l["base"]-1.2 else "sub"
            l["ch"].append(c)
    out=[]
    for l in L:
        cs=sorted(l["ch"],key=lambda c:c["x0"]);s="";prev=None
        hassp=any(c["text"].isspace() for c in cs)
        for c in cs:
            t=c["text"]
            if t.isspace():
                if hassp and not s.endswith(" "): s+=" "
                continue
            if not hassp and prev is not None and c["x0"]-prev["x1"]>0.2*c["size"] and not (c.get("mode") and prev.get("mode")==c.get("mode")): s+=" "
            m=c.get("mode")
            if m=="sup": t=SUP.get(t,t)
            elif m=="sub": t=SUB.get(t,t)
            s+=t;prev=c
        out.append((l["top"],l["x1"],s.strip()))
    return out
def run(pdf,pref,outdir):
    os.makedirs(outdir+"/img",exist_ok=True)
    recs=[];nimg=0;load_obj(pdf,pref)
    with pdfplumber.open(pdf) as p:
        for pi,pg in enumerate(p.pages[2:],start=3):
            ch=[c for c in pg.chars if not c["fontname"].split("+")[-1].startswith("Helvetica") and c["top"]<795]
            ws=pg.extract_words(extra_attrs=["fontname"])
            nh=lambda w:not w["fontname"].split("+")[-1].startswith("Helvetica")
            g=[w for w in ws if w["text"].upper().startswith("GABARITO") and nh(w)]
            gtop=g[0]["top"] if g else None;gcol=(0 if g[0]["x0"]<298 else 1) if g else None
            if gtop:
                gw=[w for w in ws if (w["x0"]<298)==(gcol==0) and w["top"]>=gtop-2 and nh(w)]
                txt=" ".join(w["text"] for w in sorted(gw,key=lambda w:(round(w["top"]/3),w["x0"])))
                recs.append(dict(p=pi,c=gcol,top=gtop-1,t="=GAB= "+txt,x1=0))
                ch=[c for c in ch if not(((c["x0"]<298)==(gcol==0)) and c["top"]>=gtop-2)]
            nat=[]
            for im in pg.images:
                if int(im["srcsize"][0]) in (2480,2481) or im["x1"]-im["x0"]>560 or im["bottom"]-im["top"]<12: continue
                nat.append((im["x0"],im["top"],im["x1"],im["bottom"]))
            vcs=vec_clusters(pg,gtop,gcol,nat) if os.environ.get("VEC","1")=="1" else []
            vi=0
            def merge_clusters(vcs,ch):
                res=[]
                for col in (0,1):
                    cs=sorted([c for c in vcs if (0 if c[0]<298 else 1)==col],key=lambda c:c[1]);grp=[]
                    for c in cs:
                        if grp and c[1]-grp[-1][3]<26:
                            g=grp[-1];y0,y1=g[3]-3,c[1]+3
                            gap=[x for x in ch if (0 if x["x0"]<298 else 1)==col and y0<=(x["top"]+x["bottom"])/2<=y1 and x["size"]>=8 and not x["text"].isspace()]
                            lines={}
                            for x in gap: lines.setdefault(round(x["top"]/3),[]).append(x)
                            if all(len(v)<=6 for v in lines.values()):
                                grp[-1]=[min(g[0],c[0]),g[1],max(g[2],c[2]),max(g[3],c[3])];grp[-1].append(1);continue
                        grp.append(list(c))
                    for g in grp:
                        if len(g)>4: g=g[:4];g[0]=min(g[0],22 if col==0 else 303);g[2]=max(g[2],290 if col==0 else 574)
                        res.append(tuple(g[:4]))
                return res
            vcs=merge_clusters(vcs,ch)
            for bb in vcs:
                inside=[c for c in ch if bb[0]-6<=(c["x0"]+c["x1"])/2<=bb[2]+6 and bb[1]-10<=(c["top"]+c["bottom"])/2<=bb[3]+10]
                # linhas de prosa (longas) não fazem parte da figura: ficam como texto
                ls={}
                for c in inside:
                    if not c["text"].isspace(): ls.setdefault(round(c["top"]/3),[]).append(c)
                def ltxt(v): return "".join(c["text"] for c in sorted(v,key=lambda c:c["x0"]))
                allprose=[v for v in ls.values() if len(v)>38 or re.match(r"^\s*0?\d{1,2}\s?\.\s?[\(A-ZÀ-Úa-z“\"]",ltxt(v))];prose=list(allprose)
                changed=True
                while changed and prose:
                    changed=False
                    for v in list(prose):
                        t0=min(c["top"] for c in v);b0=max(c["bottom"] for c in v)
                        if t0<=bb[1]+14: bb=(bb[0],max(bb[1],b0+1),bb[2],bb[3]);prose.remove(v);changed=True
                        elif b0>=bb[3]-14: bb=(bb[0],bb[1],bb[2],min(bb[3],t0-1));prose.remove(v);changed=True
                pids={id(c) for v in allprose for c in v}
                inside=[c for c in inside if id(c) not in pids and bb[1]-3<=(c["top"]+c["bottom"])/2<=bb[3]+3]
                if inside: bb=(min(bb[0],min(c["x0"] for c in inside)-3),min(bb[1],min(c["top"] for c in inside)-3),max(bb[2],max(c["x1"] for c in inside)+3),max(bb[3],max(c["bottom"] for c in inside)+3))
                txt="".join(c["text"] for c in sorted(inside,key=lambda c:(round(c["top"]/3),c["x0"])))
                if "RASCUNHO" in txt.replace(" ",""): continue
                if not inside and ((bb[2]-bb[0])>200 or (bb[3]-bb[1])<25): continue
                ch=[c for c in ch if c not in inside]
                lets="".join(sorted(set(re.findall(r"([a-e])\)",txt))))
                if not os.path.exists(outdir+"/pg"): os.makedirs(outdir+"/pg",exist_ok=True)
                pf=f"{outdir}/pg/{pref}_{pi}.png"
                if not os.path.exists(pf): subprocess.run(["pdftoppm","-f",str(pi),"-l",str(pi),"-r","130","-png","-singlefile",pdf,pf[:-4]],check=True)
                im=Image.open(pf).convert("RGB");sc=130/72
                crop=im.crop((max(0,int(bb[0]*sc)),max(0,int(bb[1]*sc)),min(im.width,int(bb[2]*sc)),min(im.height,int(bb[3]*sc))))
                if crop.width>720: crop=crop.resize((720,round(crop.height*720/crop.width)),Image.LANCZOS)
                name=f"{pref}_{pi}_v{vi}.jpg";vi+=1;crop.save(outdir+"/img/"+name,"JPEG",quality=84,optimize=True)
                c0=0 if bb[0]<298 else 1
                recs.append(dict(p=pi,c=c0,top=bb[1],x1=0,t="[[IMG:%s]]"%name))
                if lets: recs.append(dict(p=pi,c=c0,top=bb[1]+0.1,x1=0,t="[[L:%s]]"%lets))
            for ci,col in enumerate(([c for c in ch if c["x0"]<298],[c for c in ch if c["x0"]>=298])):
                for top,x1,t in build_lines(col): recs.append(dict(p=pi,c=ci,top=top,x1=x1,t=t))
            k=0;seen=[]
            for im in pg.images:
                if int(im["srcsize"][0]) in (2480,2481) or im["x1"]-im["x0"]>560 or im["bottom"]-im["top"]<12 or im["x1"]-im["x0"]<12: continue
                bb=(round(im["x0"]),round(im["top"]),round(im["x1"]),round(im["bottom"]))
                if bb in seen: continue
                seen.append(bb)
                name=f"{pref}_{pi}_{k}.jpg";k+=1
                if save_img(im,outdir+"/img/"+name,pref):
                    c=0 if im["x0"]<298 else 1
                    if not(gtop and c==gcol and im["top"]>=gtop-2):
                        recs.append(dict(p=pi,c=c,top=im["top"]-0.5,x1=0,t="[[IMG:%s]]"%name));nimg+=1
    json.dump(recs,open(outdir+f"/rec_{pref}.json","w"),ensure_ascii=False)
    print(pref,len(recs),nimg)
if __name__=="__main__": run(sys.argv[1],sys.argv[2],sys.argv[3])
