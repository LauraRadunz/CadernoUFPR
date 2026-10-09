import json,re,sys
BR="↵"
HDR=re.compile(r"^AULAS? (\d\d)((?:, \d\d)*)(?: ([EeAa]) (\d\d))?(?:\s?:|\s?–)\s*(.*)$")
def join_par(ls):
    ls=[l for l in ls if l.replace(BR,"").strip()]
    out=""
    for i,l in enumerate(ls):
        hard=l.endswith(BR);l=l.replace(BR,"").strip()
        nxt=ls[i+1].replace(BR,"").strip() if i+1<len(ls) else ""
        if not out: out=l
        elif out.endswith("\n"): out+=l
        elif out.endswith("-") and l[:1].islower() and not out.endswith(" -"): out+=l
        else: out+=" "+l
        if hard and nxt and (re.search(r"[.:;?!”\")]$",l) or not nxt[:1].islower()): out+="\n"
    return out.strip()
def parse(pref):
    recs=sorted(json.load(open(f"rec_{pref}.json")),key=lambda r:(r["p"],r["c"],r["top"]))
    mx={}
    for r in recs:
        if r["x1"]: mx[(r["p"],r["c"])]=max(mx.get((r["p"],r["c"]),0),r["x1"])
    lines=[];prev=None;lp=[]
    for r in recs:
        t=r["t"].strip();key=(r["p"],r["c"])
        P=(r["p"],r["c"],r["top"])
        if t.startswith("=GAB="): lines.append(t);lp.append(P);prev=None;continue
        if t.startswith("[[L:"): lines.append(t);lp.append(P);continue
        if not t or re.fullmatch(r"[A-Z]",t) or t=="RASCUNHO": continue
        if prev and prev[0]==key and r["top"]-prev[1]>15.5: lines.append("");lp.append(P)
        if r["x1"] and r["x1"]<mx[key]-28 and not t.startswith("[[IMG"): t+=BR
        lines.append(t);lp.append(P);prev=(key,r["top"])
    units=[];cur=None;i=0
    while i<len(lines):
        l=lines[i]
        m=HDR.match(l.replace(BR,""))
        if m:
            title=m.group(5).strip();j=i+1
            while j<len(lines) and lines[j] and not re.match(r"^\d{1,2}\s?\.",lines[j]) and lines[j]==lines[j].upper() and not lines[j].startswith(("=GAB","[[")) and len(lines[j])<60:
                title+=" "+lines[j].replace(BR,"").strip();j+=1
            cur=dict(n=int(m.group(1)),n2=([int(m.group(1))]+[int(x) for x in re.findall(r"\d\d",m.group(2) or "")]+([int(m.group(4))] if m.group(4) else [])) if (m.group(2) or m.group(4)) else None,rng=(m.group(3) or "").lower()=="a",title=title,body=[],bpos=[],hpos=lp[i],gpos=None,gab={});units.append(cur);i=j;continue
        if cur is not None:
            if l.startswith("=GAB="): cur["gpos"]=lp[i];cur["gab"].update({k.zfill(2):v for k,v in re.findall(r"(?<!\d)(\d{1,2})\s?\.\s*([A-E*]|\d{1,3}(?:[,.]\d+)?[A-Za-z]*|[VF]{2,})",l)})
            else: cur["body"].append(l);cur["bpos"].append(lp[i])
        i+=1
    Q=[];bad=[];nogab=[];skipped=[];segmap={}
    MK=re.compile(r"(?:(?<=\s)|^)([a-eA-E])\)(?=\s|$)")
    for ui,u in enumerate(units):
        if (pref,u["n"])==("p1",6): u["gab"].update({"01":"VFFVF","02":"B"})
        if (pref,u["n"])==("p1",23):
            for ix,l in enumerate(u["body"]):
                if l.startswith("corda de 0,05 m"): u["body"].insert(ix,"09. [O início deste enunciado não veio no PDF.] Um carrinho…↵");break
        body=[re.sub(r"^(\d)\s(\d)(?=\s?[.(])",r"\1\2",l) if not l.startswith("[[") else l for l in u["body"]]
        starts=[];k=1;single=None;lastit=0;used=set();nums=[]
        for ii,l in enumerate(body):
            l2=l.replace(BR,"")
            hit=False
            pg=u["gab"].get("%02d"%(k-1),"")
            mi=re.match(r"^(01|02|04|08|16|32|64)\s?\.\s*\S",l2)
            if mi and pg.isdigit() and starts and int(mi.group(1))>lastit and (lastit>0 or mi.group(1)=="01") and not re.match(r"^\d+\s?\.\s*\(",l2) and not any(re.match(r"^[a-e]\)",x.replace(BR,"").strip()) for x in body[starts[-1]:ii]):
                lastit=int(mi.group(1));continue
            if mi and not (pg.isdigit() and starts): pass
            if re.match(rf"^0?{k}\s?\.\s*(\S|$)",l2) and (k>=10 or l2.startswith("0%d"%k) or re.match(rf"^{k}\s?\.\s*\(",l2)): hit=True
            elif re.match(rf"^0?{k}\s?\(",l2): hit=True
            elif not pref.startswith("l") and k<10 and re.match(rf"^0{k}\s+[A-ZÀ-Ú]",l2): hit=True
            elif not pref.startswith("l") and k>=10 and re.match(rf"^{k}\s+[“\"(A-ZÀ-Ú]",l2): hit=True
            elif k==1 and single is None and re.match(r"^1\s?\.\s*\S",l2): hit=True;single=True
            elif single and re.match(rf"^{k}\s?\.\s*\S",l2): hit=True
            hn=k
            if not hit and pref.startswith("m"):
                mo=re.match(r"^(0\d|[1-9]\d)\s?\.\s+\S",l2)
                if mo and int(mo.group(1))>k and int(mo.group(1)) not in used and mo.group(1) in u["gab"]: hit=True;hn=int(mo.group(1))
            if hit:
                if k==1 and single is None: single=l2.startswith("1")and not l2.startswith("01")
                starts.append(ii);used.add(hn);nums.append(hn);lastit=0
                k=1
                while k in used: k+=1
        starts.append(len(body))
        for qi,(a,b) in enumerate(zip(starts,starts[1:])):
            ql=body[a:b];xl="".join(re.findall(r"\[\[L:([a-e]+)\]\]","".join(ql)));ql=[x for x in ql if not x.startswith("[[L:")];ql[0]=re.sub(r"^0?\d+\s?(\.\s*)?","",ql[0],count=1)
            ql[0]=re.sub(r"^0?\d+\s?\.\s*","",ql[0]) if False else ql[0]
            qn="%02d"%nums[qi]
            segs=None
            bp=u["bpos"]
            if len(bp)==len(u["body"]):
                grp={};order=[]
                for P in bp[a:b]:
                    k2=(P[0],P[1])
                    if k2 not in grp: grp[k2]=[P[2],P[2]];order.append(k2)
                    else: grp[k2][0]=min(grp[k2][0],P[2]);grp[k2][1]=max(grp[k2][1],P[2])
                segs=[]
                for gi,k2 in enumerate(order):
                    y0=grp[k2][0]-3;y1=792
                    if gi==len(order)-1:
                        if b<len(bp):
                            if (bp[b][0],bp[b][1])==k2: y1=bp[b][2]-3
                        else:
                            c=[]
                            if u["gpos"] and (u["gpos"][0],u["gpos"][1])==k2 and u["gpos"][2]>y0: c.append(u["gpos"][2]-2)
                            if ui+1<len(units):
                                hp=units[ui+1]["hpos"]
                                if (hp[0],hp[1])==k2 and hp[2]>y0: c.append(hp[2]-2)
                            if c: y1=min(c)
                    segs.append([k2[0],k2[1],round(y0,1),round(y1,1)])
            segmap[f"{u['n']}-{qn}"]=segs
            ans=u["gab"].get(qn)
            if ans and ans.isdigit():
                it=[i for i,l in enumerate(ql) if re.match(r"^(01|02|04|08|16|32|64)\s?[.)]\s*\S",l.replace(BR,""))]
                if it and any(re.match(r"^0[3567]\s?\)",l.replace(BR,"")) for l in ql): it=[]
                if it:
                    vals=[];txt=[]
                    for i in range(it[0],len(ql)):
                        l=ql[i].replace(BR,"").strip()
                        m=re.match(r"^(01|02|04|08|16|32|64)\s?[.)]\s*(.*)$",l)
                        if m and (not vals or int(m.group(1))>vals[-1]): vals.append(int(m.group(1)));txt.append(m.group(2))
                        elif l and not l.startswith("[["): txt[-1]+=" "+l
                    stl=ql[:it[0]]
                    paras=[];cu=[]
                    for l in stl:
                        if l=="":
                            if cu:paras.append(cu);cu=[]
                        elif l.startswith("[[IMG"):
                            if cu:paras.append(cu);cu=[]
                            paras.append([l])
                        else: cu.append(l)
                    if cu:paras.append(cu)
                    blocks=[["img",p[0][6:-2]] if p[0].startswith("[[IMG") else ["p",join_par(p)] for p in paras]
                    Q.append(dict(id=f"{u['n']}-{qn}",aula=u["n"],n=nums[qi],blocks=blocks,opts=txt,vals=vals,ans=int(ans),type="soma",imgopts=False));continue
                nm=[i for i,l in enumerate(ql) if re.match(r"^0[1-9]\s?\)",l.replace(BR,"").strip())]
                if nm:
                    txt=" ".join(l.replace(BR,"").strip() for l in ql[nm[0]:] if not l.startswith("[["))
                    ms=list(re.finditer(r"(?:(?<=\s)|^)(0[1-9])\s?\)\s*",txt))
                    seg={}
                    for j,m in enumerate(ms):
                        e=ms[j+1].start() if j+1<len(ms) else len(txt)
                        seg.setdefault(int(m.group(1)),txt[m.end():e].strip())
                    n=len(seg)
                    if n>=2 and 1<=int(ans)<=n and all(i in seg for i in range(1,n+1)):
                        paras=[];cu=[]
                        for l in ql[:nm[0]]:
                            if l=="":
                                if cu:paras.append(cu);cu=[]
                            elif l.startswith("[[IMG"):
                                if cu:paras.append(cu);cu=[]
                                paras.append([l])
                            else: cu.append(l)
                        if cu:paras.append(cu)
                        blocks=[["img",p[0][6:-2]] if p[0].startswith("[[IMG") else ["p",join_par(p)] for p in paras]
                        Q.append(dict(id=f"{u['n']}-{qn}",aula=u["n"],n=nums[qi],blocks=blocks,opts=[seg[i] for i in range(1,n+1)],ans="ABCDE"[int(ans)-1],imgopts=False));continue
                skipped.append(f"{u['n']}-{qn}:{ans}");continue
            if ans and not re.fullmatch(r"[A-E*]",ans) and not re.fullmatch(r"[VF]{2,}",ans):
                skipped.append(f"{u['n']}-{qn}:{ans}");continue
            if ans and re.fullmatch(r"[VF]{2,}",ans) and any(l.replace(BR,"").startswith("( )") for l in ql):
                ii=[i for i,l in enumerate(ql) if l.replace(BR,"").startswith("( )")]
                txt=[]
                for i in range(ii[0],len(ql)):
                    l=ql[i].replace(BR,"").strip()
                    if l.startswith("( )"): txt.append(l[3:].strip())
                    elif l and not l.startswith("[["): txt[-1]+=" "+l
                if len(txt)==len(ans):
                    paras=[];cu=[]
                    for l in ql[:ii[0]]:
                        if l=="":
                            if cu:paras.append(cu);cu=[]
                        elif l.startswith("[[IMG"):
                            if cu:paras.append(cu);cu=[]
                            paras.append([l])
                        else: cu.append(l)
                    if cu:paras.append(cu)
                    blocks=[["img",p[0][6:-2]] if p[0].startswith("[[IMG") else ["p",join_par(p)] for p in paras]
                    Q.append(dict(id=f"{u['n']}-{qn}",aula=u["n"],n=nums[qi],blocks=blocks,opts=txt,ans=ans,type="vf",imgopts=False));continue
            first=[i for i,l in enumerate(ql) if re.match(r"^a\)",l.replace(BR,"").strip(),re.I)]
            if not first:
                for i,l in enumerate(ql):
                    mm=re.search(r"(?:^|\s)(a\)\s)",l.replace(BR,""))
                    if mm and "b)" in " ".join(ql[i:i+4]):
                        t=l.replace(BR,"");ql[i:i+1]=[t[:mm.start(1)].rstrip(),t[mm.start(1):]];first=[i+1];break
            if not first:
                first=[i for i,l in enumerate(ql) if re.match(r"^a\)\s*b\)",l.strip())]
            stem=ql[:first[0]] if first else ql
            seg={};order=[];last=None;after=[]
            if first:
                for l in ql[first[0]:]:
                    if l.startswith("[[IMG"): after.append(l);continue
                    l=l.replace(BR,"")
                    ms=list(MK.finditer(l))
                    if not ms:
                        if last and l.strip(): seg[last]=(seg[last]+" "+l.strip()).strip()
                        continue
                    if ms[0].start()>0 and last and l[:ms[0].start()].strip(): seg[last]=(seg[last]+" "+l[:ms[0].start()].strip()).strip()
                    for j,m in enumerate(ms):
                        e=ms[j+1].start() if j+1<len(ms) else len(l)
                        let=m.group(1).lower()
                        if let in seg: last=None;continue
                        seg[let]=l[m.end():e].strip();last=let
            letters=[x for x in "abcde" if x in seg or x in xl]
            no=max([ord(x)-96 for x in letters]+[0])
            if no<4 and ans in ("A","B","C","D","E") and ans!="E": no=max(no,4)
            if not first: no=5
            opts=[seg.get(x,"") for x in "abcde"[:no]]
            imgopts=(not first) or sum(1 for o in opts if o)<=len(opts)//2
            if imgopts:
                opts=["Ver a figura"]*no;bad.append((u["n"],qn,len(letters)))
            else: opts=[o or "Ver a figura" for o in opts]
            paras=[];cu=[]
            for l in stem+after:
                if l=="":
                    if cu:paras.append(cu);cu=[]
                elif l.startswith("[[IMG"):
                    if cu:paras.append(cu);cu=[]
                    paras.append([l])
                else: cu.append(l)
            if cu:paras.append(cu)
            blocks=[["img",p[0][6:-2]] if p[0].startswith("[[IMG") else ["p",join_par(p)] for p in paras]
            if not ans: nogab.append(f"{u['n']}-{qn}")
            if ans=='*': continue
            d=dict(id=f"{u['n']}-{qn}",aula=u["n"],n=nums[qi],blocks=blocks,opts=opts,ans=ans,imgopts=imgopts)
            if ans and re.fullmatch(r"[VF]{2,}",ans):
                if len(ans)!=len([o for o in opts if o]) or imgopts: skipped.append(f"{u['n']}-{qn}:{ans}");continue
                d["type"]="vf"
            Q.append(d)
        ng=len(starts)-1
        if ng!=len(u["gab"]): print("  count mismatch",pref,u["n"],ng,len(u["gab"]))
    print('  skipped',pref,skipped)
    for q in Q: q['seg']=segmap.get(q['id'])
    return units,Q,bad,nogab
if __name__=="__main__":
    out={}
    for pref in sys.argv[1:]:
        u,Q,bad,ng=parse(pref)
        out[pref]=dict(units=[dict(n=x["n"],n2=x["n2"],rng=x.get("rng",False),title=x["title"]) for x in u],Q=Q)
        print(pref,len(u),len(Q),"imgopts",bad[:12],len(bad),"nogab",ng)
    json.dump(out,open("Qall.json","w"),ensure_ascii=False)
