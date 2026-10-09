"""Gera a pasta dist/ pronta para o GitHub Pages (index.html completo + imagens)."""
import os,shutil,re,glob
src=open("index.html",encoding="utf-8").read()
m=re.search(r"<title>.*?</title>",src,re.S)
title=m.group(0) if m else "<title>Cadernos de Estudo</title>"
body=src.replace(title,"",1)
doc=('<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">'
 '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'+title+
 '<style>*,*::before,*::after{box-sizing:border-box}html,body{margin:0}body{min-height:100vh}</style></head><body>'+body+'</body></html>')
shutil.rmtree("dist",ignore_errors=True);os.makedirs("dist/img")
open("dist/index.html","w",encoding="utf-8").write(doc)
open("dist/.nojekyll","w").close()
for d in sorted(glob.glob("atl*")):
    if d=="atl_old": continue
shutil.copytree("atl4","dist/atl4")
for f in ("mapa-roma.jpg","iluminura.jpg"): shutil.copy("img/"+f,"dist/img/"+f)
print("ok",sum(os.path.getsize(os.path.join(r,f)) for r,_,fs in os.walk("dist") for f in fs)/1e6,"MB")
