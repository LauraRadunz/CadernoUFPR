import json,re
S="/tmp/claude-0/-home-claude/1eed8458-4368-50ee-9a19-1861f667ed10/scratchpad"
t=open("template.html").read();head=t[:t.index("<script>\n(function")]
js=open("newjs2.txt").read();css=open("themes.css").read()
j=json.dumps(json.load(open("data_all.json")),ensure_ascii=False).replace("</","<\\/")
html=(head+js).replace("</style>",css+"</style>",1)
html=re.sub(r"<title>.*?</title>","<title>Cadernos de Estudo</title>",html,count=1)
html=re.sub(r'family=Cinzel[^"]*display=swap','family=Cinzel:wght@500;700&family=Cormorant+Garamond:wght@500;600;700&family=Crimson+Pro:ital,wght@0,400;0,500;0,600;1,400&family=Source+Serif+4:ital,wght@0,400;0,600;1,400&family=Fraunces:wght@600;700&family=Space+Grotesk:wght@500;700&family=Exo+2:wght@600;700&family=Playfair+Display:wght@600;700&family=Sora:wght@600;700;800&family=Karla:ital,wght@0,400;0,600;1,400&family=Lora:ital,wght@0,400;0,600;1,400&family=Lato:ital,wght@0,400;0,700;1,400&family=IBM+Plex+Sans:ital,wght@0,400;0,600;1,400&family=Nunito+Sans:ital,wght@0,400;0,600;0,700;1,400&display=swap',html,count=1)
html=html.replace("__DATA__",j);open("index.html","w").write(html)
open(S+"/chk.js","w").write(html[html.rindex("<script>\n(function")+8:html.rindex("</script>")])
