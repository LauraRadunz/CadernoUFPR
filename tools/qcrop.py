import json,sys,os,subprocess,glob
from PIL import Image
import numpy as np
DPI=150;S=DPI/72
XR={0:(22,292),1:(304,572)}
def render(pref):
    d=f"pg2/{pref}";os.makedirs(d,exist_ok=True)
    if not glob.glob(d+"/p-*.png"): subprocess.run(["pdftoppm","-r",str(DPI),"-gray","-png",f"{pref}.pdf",d+"/p"],check=True)
def page(pref,p):
    f=glob.glob(f"pg2/{pref}/p-{p:02d}.png")+glob.glob(f"pg2/{pref}/p-{p:03d}.png")+glob.glob(f"pg2/{pref}/p-{p}.png")
    return Image.open(f[0]).convert("L")
def trim(a):
    rows=np.where((a<140).any(1))[0]
    if len(rows)==0: return None
    return a[max(0,rows[0]-5):rows[-1]+7]
def main(pref,key):
    render(pref)
    d=json.load(open("Qall.json"));cache={}
    os.makedirs("img",exist_ok=True);miss=0
    for q in d[key]["Q"]:
        if not q.get("seg"): miss+=1;continue
        parts=[]
        for p,c,y0,y1 in q["seg"]:
            if p not in cache: cache[p]=np.asarray(page(pref,p))
            im=cache[p];x0,x1=XR[c]
            a=im[int(max(0,y0)*S):int(y1*S),int(x0*S):int(x1*S)]
            t=trim(a)
            if t is not None and t.shape[0]>8: parts.append(t)
        if not parts: miss+=1;continue
        w=max(p.shape[1] for p in parts)
        parts=[np.pad(p,((0,0),(0,w-p.shape[1])),constant_values=255) for p in parts]
        out=np.vstack(parts)
        name=f"{key}_{q['id']}.jpg"
        Image.fromarray(out).convert("RGB").save("img/"+name,"JPEG",quality=78,optimize=True)
        q["qimg"]=name;q["qsize"]=[out.shape[1],out.shape[0]]
    json.dump(d,open("Qall.json","w"),ensure_ascii=False)
    print(pref,len(d[key]["Q"]),"miss",miss)
if __name__=="__main__": main(sys.argv[1],sys.argv[2])
