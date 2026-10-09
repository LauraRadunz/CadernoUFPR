import json,re,os,sys
from PIL import Image
S="/tmp/claude-0/-home-claude/1eed8458-4368-50ee-9a19-1861f667ed10/scratchpad"
QD=S+"/qui"
Q=json.load(open(QD+"/Qall.json"))
CIT=re.compile(r"(Acesso em|Disponível em|^\(.*\)\.?$|^https?://|Adaptado|adaptado|Fonte:|Texto adaptado|Franco Jr|Disponivel em)",re.I)
ITEM=re.compile(r"^(\(\s*[_ ]*\s*\)|[IVX]+\s?[.)\-–]\s?\S|\d{1,2}\s?[.)\-–]\s?\S|[A-E]\)\s\S)")
def clean(s):
    s=re.sub(r"[ \t]+"," ",s); s=re.sub(r" ?\n ?","\n",s)
    s=re.sub(r"([“‘]) ",r"\1",s); s=re.sub(r" ([”’])",r"\1",s)
    return s.strip()
SMALL={"DE","DA","DO","DAS","DOS","E","À","A","O","AS","OS","EM","NA","NO"}
SPEC={"NOX":"Nox","KPS":"Kps","UFPR":"UFPR"}
def tt(t):
    out=[]
    for i,w in enumerate(t.split()):
        core=re.sub(r"\W","",w)
        if re.fullmatch(r"[IVX]{1,5}",w): out.append(w)
        elif core.upper() in SPEC and w.upper()==w: out.append(w.replace(core,SPEC[core.upper()]))
        elif w.upper()!=w: out.append(w)
        elif w in SMALL and i>0: out.append(w.lower())
        else: out.append(w.capitalize())
    return " ".join(out)
def roman(n):
    r="";
    for v,s in [(40,"XL"),(10,"X"),(9,"IX"),(5,"V"),(4,"IV"),(1,"I")]:
        while n>=v:r+=s;n-=v
    return r
def convert(pref,romanize,onlyfrom=0):
    d=Q[pref];qs=[]
    for q in d["Q"]:
        if q["aula"]<onlyfrom or not q.get("ans"): continue
        blocks=[];tag=""
        for k,x in q["blocks"]:
            if k=="img": blocks.append(["img",QD+"/img/"+x]);continue
            x=clean(x)
            if not x: continue
            if not blocks:
                m=re.match(r"^\(([^)]{2,50})\)\s*\.?\s*(.*)$",x,re.S)
                if m: tag=m.group(1);x=m.group(2)
                if not x: continue
            if ITEM.match(x) and "\n" not in x: kind="item"
            elif blocks and len(x)<300 and CIT.search(x) and not x.endswith(":") and not x.endswith("?"): kind="src"
            else: kind="p"
            blocks.append([kind,x])
        for i,b in enumerate(blocks):
            if b[0]=="p" and len(b[1])>140 and i+1<len(blocks) and (blocks[i+1][0]=="src" or b[1][:1] in "“\""): b[0]="text"
        opts=[clean(o) if o else "Ver a figura" for o in q["opts"]]
        t=q.get("type")
        if q.get("qimg"):
            tx=" ".join(b[1] for b in blocks if b[0]!="img")
            tx=(tx+" || "+" ; ".join("%s) %s"%("abcde"[i],o) for i,o in enumerate(opts)))[:1100]
            blocks=[["img",QD+"/img/"+q["qimg"]]];opts=[""]*len(opts)
            ex=dict(imgq=1,tx=tx)
        else: ex={}
        if t=="soma": qs.append(dict(id=q["id"],aula=q["aula"],n=q["n"],tag="",blocks=blocks,opts=opts,ans=q["ans"],type="soma",vals=q["vals"],**ex));continue
        if t=="soma-old": qs.append(dict(id=q["id"],aula=q["aula"],n=q["n"],tag=tag,blocks=blocks,opts=opts,ans=q["ans"],type="soma",vals=q["vals"]))
        elif t=="vf": qs.append(dict(id=q["id"],aula=q["aula"],n=q["n"],tag=tag,blocks=blocks,opts=opts,ans=q["ans"],type="vf"))
        else: qs.append(dict(id=q["id"],aula=q["aula"],n=q["n"],tag=("" if ex else tag),blocks=blocks,opts=opts,ans="abcde".index(q["ans"].lower()),**ex))
    au=[]
    for u in d["units"]:
        if u["n"]<onlyfrom: continue
        c=sum(1 for q in qs if q["aula"]==u["n"])
        if not c: continue
        ns=u["n2"] if isinstance(u["n2"],list) else ([u["n"],u["n2"]] if u["n2"] else [u["n"]])
        lab=("Aulas "+", ".join("%02d"%x for x in ns[:-1])+(" a " if u.get("rng") else " e ")+"%02d"%ns[-1]) if len(ns)>1 else "Aula %02d"%u["n"]
        au.append(dict(n=u["n"],rom=roman(u["n"]) if romanize else "%02d"%u["n"],title=tt(u["title"]),lab=lab,count=c))
    return au,qs
data=json.load(open("data_all.bak.json"))
cads=[c for c in data["cadernos"]]
byid={c["id"]:c for c in cads}
# --- Química
QI=[("q1","quim1","Química I","Química · Frente I","I","Matéria, atomística, ligações, inorgânica e soluções","Da classificação da matéria à química ambiental: modelos atômicos, tabela periódica, ligações, funções inorgânicas, soluções, propriedades coligativas e radioatividade.",["#0d4f66","#e4f4f8","#7fe0f0"]),
    ("q2","quim2","Química II","Química · Frente II","II","Estequiometria, gases, termoquímica, eletroquímica, cinética e equilíbrio","Relações de massa, mol, gases, reações e estequiometria, termoquímica, pilhas e eletrólise, cinética, equilíbrio químico, pH, hidrólise, tampão e Kps.",["#3a2f78","#ece8fb","#c5b6ff"]),
    ("q3","quim3","Química III","Química · Frente III","III","Química orgânica","Introdução à orgânica, cadeias, hidrocarbonetos, funções, isomeria, propriedades, reações orgânicas, polímeros e bioquímica.",["#7a3d12","#fbefe0","#ffc36b"])]
newq=[]
for pref,cid,nome,tit,emb,sub,lede,card in QI:
    au,qs=convert(pref,False)
    newq.append(dict(id=cid,theme="quimica",grupo="quimica",key=f"caderno-{cid}-v1",nome=nome,titulo=tit,emblema=emb,orn="⚗",un="Aula",unPl="Aulas",nesta="nesta aula",art="as aulas",comecar="Começar a aula",
      eyebrow=tit.replace("·","·")+" · Aulas 1 a %d"%max(a["n"] for a in au),lede=lede+" Responda, confirme e veja a alternativa correta. As questões seguem a ordem do material e um aviso marca cada mudança de aula.",sub=sub,card=card,aulas=au,qs=qs))
# --- Física
FI=[("p1","fis1","Física I","Física · Frente I","I","Mecânica: cinemática, dinâmica, energia e hidrostática","Análise dimensional, vetores, cinemática, lançamentos, movimento circular, leis de Newton, equilíbrio, gravitação, trabalho e energia, impulso e colisões, hidrostática.",["#27307a","#e8eaff","#8fb8ff"]),
    ("p2","fis2","Física II","Física · Frente II","II","Termologia, óptica e ondas","Termometria, dilatação, calor, gases e termodinâmica, óptica geométrica, espelhos e lentes, ondulatória, acústica, efeito Doppler e MHS.",["#7a2433","#ffeee6","#ffa07a"]),
    ("p3","fis3","Física III","Física · Frente III","III","Eletricidade, magnetismo e física moderna","Eletrostática, circuitos, capacitores, magnetismo, indução, radiação de corpo negro, efeito fotoelétrico e relatividade.",["#1b3a5c","#e6f1fb","#ffe14d"])]
for pref,cid,nome,tit,emb,sub,lede,card in FI:
    if pref not in Q: continue
    au,qs=convert(pref,False)
    newq.append(dict(id=cid,theme="fisica",grupo="fisica",key=f"caderno-{cid}-v1",nome=nome,titulo=tit,emblema=emb,orn="✦",un="Aula",unPl="Aulas",nesta="nesta aula",art="as aulas",comecar="Começar a aula",
      eyebrow=tit+" · Aulas 1 a %d"%max(a["n"] for a in au),lede=lede+" Responda, confirme e veja a alternativa correta. As questões seguem a ordem do material e um aviso marca cada mudança de aula.",sub=sub,card=card,aulas=au,qs=qs))


# --- Geografia (grupo, 3 cadernos; Geo II = lista 2026 + complemento sem repetidas)
GEO=[("g1","geo1","Geografia I","Geografia · Frente I","I","Geografia física: movimentos da Terra, cartografia e geologia","Movimentos da Terra, cartografia (escalas, coordenadas, projeções, fusos e sensoriamento) e geologia.",["#9a3f0a","#fff1de","#ffd27a"]),
     ("g2","geo2","Geografia II","Geografia · Frente II","II","Brasil e mundo: população, indústria, urbanização, campo e geopolítica","Território e regionalização do Brasil, demografia, industrialização, urbanização, setor primário, conflitos por terra, globalização, geopolítica e aspectos humanos mundiais.",["#c4570b","#fff3e3","#ffe08a"]),
     ("g3","geo3","Geografia III","Geografia · Frente III","III","Economia global, blocos econômicos e atualidades","Economia geral e cenário político-econômico, fronteiras problemáticas, blocos econômicos e atualidades.",["#6b3a12","#fdecd0","#ffb347"])]
for pref,cid,nome,tit,emb,sub,lede,card in GEO:
    if pref not in Q: continue
    au,qs=convert(pref,False)
    newq.append(dict(id=cid,theme="geografia",grupo="geografia",key=f"caderno-{cid}-v1",nome=nome,titulo=tit,emblema=emb,orn="⊕",un="Aula",unPl="Aulas",nesta="nesta aula",art="as aulas",comecar="Começar a aula",
      eyebrow=tit+(" · Lista 2026 " if False else ""),lede=lede+" Responda, confirme e veja a alternativa correta. As questões seguem a ordem do material e um aviso marca cada mudança de aula."+(" Inclui questões da lista antiga que não se repetiam na lista 2026, já no assunto certo." if pref in ("g2","g3") else ""),sub=sub,card=card,pdfNote="",aulas=au,qs=qs))


# --- Matemática (grupo, 3 cadernos; Mat II recebe as questões da lista extra que não se repetem)
MAT=[("m1","mat1","Matemática I","Matemática · Frente I","I","Álgebra: conjuntos, funções, exponencial, logaritmo, trigonometria e sequências","Conjuntos e numéricos, múltiplos e divisores, potenciação e radiciação, funções (afim, quadrática, modular, exponencial, logarítmica), inequações, trigonometria e progressões.",["#8a5a00","#fff8d6","#ffe27a"]),
     ("m2","mat2","Matemática II","Matemática · Frente II","II","Geometria plana, espacial e analítica","Ângulos, triângulos, quadriláteros e polígonos, áreas, semelhança, trigonometria, círculos, poliedros, prismas, pirâmides, cilindro, cone, esfera e geometria analítica.",["#a8480f","#fff3dc","#ffd08a"]),
     ("m3","mat3","Matemática III","Matemática · Frente III","III","Matemática financeira, estatística, contagem, probabilidade e álgebra","Razão e proporção, porcentagem, juros, estatística, análise combinatória, probabilidade, matrizes, determinantes, sistemas, polinômios e números complexos.",["#5f4300","#fdf3c8","#ffc933"])]
for pref,cid,nome,tit,emb,sub,lede,card in MAT:
    if pref not in Q: continue
    au,qs=convert(pref,False)
    newq.append(dict(id=cid,theme="matematica",grupo="matematica",key=f"caderno-{cid}-v1",nome=nome,titulo=tit,emblema=emb,orn="∑",un="Aula",unPl="Aulas",nesta="nesta aula",art="as aulas",comecar="Começar a aula",
      eyebrow=tit,lede=lede+" Cada questão aparece como no PDF, com as fórmulas intactas; você marca a letra, confirma e vê a correta. As questões seguem a ordem do material e um aviso marca cada mudança de aula."+(" Inclui as questões da lista extra que não se repetiam, já na aula certa." if pref=="m2" else ""),sub=sub,card=card,pdfNote="",aulas=au,qs=qs))
# --- Sociologia (1 caderno)
if "s1" in Q:
    au,qs=convert("s1",True)
    TS={1:"Um toque de clássicos – Émile Durkheim",5:"Um toque de clássicos – Max Weber",8:"Um toque de clássicos – Karl Marx",11:"Clássicas do pensamento social",20:"Pacto da branquitude",26:"Quem tem medo do gênero?",30:"Sobre o autoritarismo brasileiro"}
    for a in au: a["title"]=TS[a["n"]]
    newq.append(dict(id="socio",theme="sociologia",key="caderno-socio-v1",nome="Sociologia",titulo="Caderno de Sociologia",emblema="Σ",orn="◌",un="Tema",unPl="Temas",nesta="neste tema",art="os temas",comecar="Começar o tema",
      eyebrow="UFPR · Sete temas",lede="Durkheim, Weber, Marx, as clássicas do pensamento social, branquitude, gênero e autoritarismo brasileiro. Responda, confirme e veja a alternativa correta. As questões seguem a ordem do material e um aviso marca cada mudança de tema.",
      sub="Durkheim, Weber, Marx e temas contemporâneos",card=["#4a4d54","#efeff1","#d4b27a"],pdfNote="",aulas=au,qs=qs))
# --- Literatura (1 caderno, cada "aula" = um livro)
if "l2" in Q:
    au,qs=convert("l2",False)
    TT={1:"A Falência – Júlia Lopes de Almeida",2:"Noite na Taverna – Álvares de Azevedo",3:"O Drible – Sérgio Rodrigues",4:"O Sol na Cabeça – Geovani Martins",5:"Poema Sujo – Ferreira Gullar",6:"Eu – Augusto dos Anjos",7:"O Demônio Familiar – José de Alencar",8:"O Quinze – Rachel de Queiroz"}
    for a in au: a["title"]=TT[a["n"]];a["lab"]="Livro %02d"%a["n"]
    newq.append(dict(id="lit",theme="literatura",key="caderno-lit-v1",nome="Literatura",titulo="Caderno de Literatura",emblema="❝",orn="❦",un="Livro",unPl="Livros",nesta="neste livro",art="os livros",comecar="Começar o livro",
      eyebrow="UFPR · Oito livros",lede="Os livros da lista: de A Falência a O Quinze. Responda, confirme e veja a alternativa correta. As questões seguem a ordem do material, um aviso marca cada mudança de livro e as marcadas “Inédita” foram criadas no modelo UFPR.",
      sub="Oito obras da lista de leituras",card=["#5a1230","#f8ece4","#e8b560"],pdfNote="",aulas=au,qs=qs))
# --- História I (nova) e II (acrescenta aulas 14+)
au,qs=convert("h1",True)
h1=dict(id="historia1",theme="historia",grupo="historia",key="caderno-historia1-v1",nome="História · Frente I",titulo="Caderno de História I",emblema="I",orn="❖",un="Aula",unPl="Aulas",nesta="nesta aula",art="as aulas",comecar="Começar a aula",
  eyebrow="Frente I · História do Brasil",lede="Do período pré-colonial ao patrimônio histórico-cultural brasileiro. Responda, confirme e veja a alternativa correta. As questões seguem a ordem do material e um aviso marca cada mudança de aula.",
  sub="História do Brasil, da Colônia à Nova República",card=["#5c3a17","#f6ecd6","#e8c27a"],aulas=au,qs=qs)
au2,qs2=convert("h2",True,onlyfrom=14)
H=byid["historia"]
H["aulas"]=[a for a in H["aulas"] if a["n"]<14]+au2
H["qs"]=[q for q in H["qs"] if q["aula"]<14]+qs2
H["eyebrow"]="Frente II · Aulas I a %s"%roman(max(a["n"] for a in H["aulas"]))
H["sub"]="Da Antiguidade ao século XXI"
H["lede"]="Do patrimônio histórico e da Antiguidade ao século XXI. Responda, confirme e veja se acertou, com a alternativa correta. As questões seguem a ordem do material e um aviso marca cada mudança de aula."
for a in H["aulas"]: a.setdefault("lab","Aula %02d"%a["n"])
cads=[c for c in cads if c["id"] not in ("historia1",)]
ids=[c["id"] for c in cads if not c["id"].startswith("quim")]
cads=[c for c in cads if not c["id"].startswith(("quim","fis","geo","mat"))]
hi=[i for i,c in enumerate(cads) if c["id"]=="historia"][0]
cads.insert(hi,h1)
cads+=newq
data["cadernos"]=cads
gr=[g for g in data["grupos"] if g["id"] not in ("quimica","fisica","geografia","matematica")]
gr.append(dict(id="quimica",nome="Química",emblema="⚗",theme="quimica",sub="Frentes I, II e III",card=["#0d4f66","#e4f4f8","#7fe0f0"],eyebrow="Matéria",lede="Escolha a frente. Cada caderno guarda o seu histórico, os erros e o ponto onde você parou."))
gr.append(dict(id="fisica",nome="Física",emblema="⚛",theme="fisica",sub="Frentes I, II e III",card=["#27307a","#e8eaff","#ffd166"],eyebrow="Matéria",lede="Escolha a frente. Cada caderno guarda o seu histórico, os erros e o ponto onde você parou."))
gr.append(dict(id="geografia",nome="Geografia",emblema="⊕",theme="geografia",sub="Frentes I, II e III",card=["#b34a0a","#fff1de","#ffd27a"],eyebrow="Matéria",lede="Escolha a frente. Cada caderno guarda o seu histórico, os erros e o ponto onde você parou."))
gr.append(dict(id="matematica",nome="Matemática",emblema="∑",theme="matematica",sub="Frentes I, II e III",card=["#8a5a00","#fff8d6","#ffd23f"],eyebrow="Matéria",lede="Escolha a frente. Cada caderno guarda o seu histórico, os erros e o ponto onde você parou."))
for g in gr:
    if g["id"]=="historia": g["sub"]="Frentes I e II"
data["grupos"]=gr
# --- atlas de imagens
os.makedirs("atl4",exist_ok=True)
for f in os.listdir("atl4"): os.remove("atl4/"+f)
refs=[];seen={}
def path_of(x): return x if x.startswith("/") else "/home/claude/site/"+x
for c in cads:
    for q in c["qs"]:
        for b in q["blocks"]:
            if b[0]=="img" and len(b)==2:
                p=path_of(b[1])
                if p not in seen: seen[p]=None;refs.append(p)
atl=[];cur=[];h=0
def flush():
    global cur,h
    if not cur: return
    n=len(atl);im=Image.new("RGB",(720,h),(255,255,255));y=0;pos={}
    for p,i in cur:
        im.paste(i,(0,y));pos[p]=(i.width,i.height,y);y+=i.height
    name="atl4/a%02d.jpg"%n;im.save(name,"JPEG",quality=84,optimize=True)
    for p,(w,hh,yy) in pos.items(): seen[p]=(name,w,hh,yy,h)
    atl.append(name);cur=[];h=0
for p in refs:
    try: i=Image.open(p).convert("RGB")
    except Exception as e: print("missing",p);continue
    if h+i.height>6500 and cur: flush()
    cur.append((p,i));h+=i.height
flush()
miss=0
for c in cads:
    for q in c["qs"]:
        nb=[]
        for b in q["blocks"]:
            if b[0]=="img" and len(b)==2:
                s=seen.get(path_of(b[1]))
                if s: nb.append(["img",s[0],s[1],s[2],s[3],s[4]])
                else: miss+=1
            else: nb.append(b)
        q["blocks"]=nb
json.dump(data,open("data_all.json","w"),ensure_ascii=False)
print("atlases",len(atl),"missing",miss,[ (c["id"],len(c["qs"]),len(c["aulas"])) for c in cads])
print(sum(os.path.getsize("atl4/"+f) for f in os.listdir("atl4"))/1e6,"MB")
