import json
d=json.load(open('Qall.json'))
Q=d['l2']['Q']
for q in Q: q['blocks']=[b for b in q['blocks'] if b[0]!='img']
TAG="(Inédita – modelo UFPR) "
VF5=["V – F – V – F","F – V – F – V","V – V – F – F","F – F – V – V","V – F – F – V"]
def mk(aula,n,stem,opts,ans,items=None,after=None):
    bl=[["p",TAG+stem]]
    if items: bl+= [["p",x] for x in items]
    if after: bl.append(["p",after])
    return dict(id=f"{aula}-{n:02d}",aula=aula,n=n,blocks=bl,opts=opts,ans=ans,imgopts=False)
X=[]
# ---- Noite na Taverna (aula 2)
X.append(mk(2,16,"Sobre a estrutura narrativa de Noite na Taverna, de Álvares de Azevedo, assinale a alternativa correta.",[
"A obra é um romance realista em terceira pessoa, no qual um narrador onisciente descreve com neutralidade a vida urbana do século XIX.",
"A obra se organiza em moldura: jovens reunidos numa taverna, entre bebida e devaneios, narram, um a um, episódios de suas vidas marcados por paixão, crime e morte.",
"A obra é composta por poemas líricos independentes, sem personagens nem enredo, reunidos apenas por um tema sentimental e idealizado.",
"A obra é uma sátira de costumes que critica a ascensão da burguesia e defende o ideal de progresso científico.",
"A obra é um texto dramático em cinco atos, escrito para ser encenado nos teatros da Corte."],"B"))
X.append(mk(2,17,"Considere as afirmativas a seguir sobre Noite na Taverna e o Ultrarromantismo brasileiro.",[
"I e II, apenas.","II e III, apenas.","I, II e IV, apenas.","I, III e IV, apenas.","I, II, III e IV."],"C",items=[
"I. A obra expressa o chamado “mal do século”: as personagens vivem o tédio, o pessimismo e uma atração pela morte.",
"II. A influência de Lord Byron aparece no gosto pelo satânico, pelo macabro e pela transgressão das normas morais e religiosas.",
"III. Álvares de Azevedo toma o indígena como herói nacional e, por meio dele, constrói o projeto de uma identidade brasileira idealizada.",
"IV. A noite e os cenários europeus reforçam uma atmosfera fantástica, distanciada da realidade social brasileira."],
after="Estão corretas:"))
X.append(mk(2,18,"Em relação a Noite na Taverna, marque as afirmativas abaixo com V (verdadeiro) ou F (falso).",[
"V – F – V – F","F – V – F – V","V – V – F – F","F – F – V – V","V – F – F – V"],"A",items=[
"( ) A obra pertence à prosa da segunda geração romântica brasileira, chamada de geração ultrarromântica.",
"( ) O livro apresenta um amor idealizado e espiritual, em que a mulher é figura pura e inatingível e o desfecho é sempre feliz.",
"( ) Entre os temas recorrentes das narrativas estão a morte, o crime, o incesto e a necrofilia, tratados sem o véu moralizante comum à prosa romântica anterior.",
"( ) A linguagem é predominantemente objetiva e científica, com descrições exatas, em oposição ao excesso de emoção típico do Romantismo."],
after="Assinale a alternativa que apresenta a sequência correta, de cima para baixo."))
X.append(mk(2,19,"Sobre Álvares de Azevedo e sua obra, assinale a alternativa correta.",[
"Publicou em vida inúmeros romances de sucesso e foi um dos principais críticos do Ultrarromantismo.",
"Viveu até idade avançada e abandonou o Romantismo ao aderir à estética realista.",
"Dedicou-se exclusivamente à poesia indianista, retratando o índio como símbolo da nação.",
"Estudante de Direito em São Paulo, morreu muito jovem; sua obra, em boa parte publicada depois da morte, reúne poesia (Lira dos vinte anos), prosa (Noite na Taverna) e teatro (Macário).",
"Foi o fundador do Parnasianismo brasileiro e defendeu a impessoalidade e a perfeição formal do verso."],"D"))
X.append(mk(2,20,"Quanto ao modo como Noite na Taverna constrói suas personagens, é correto afirmar:",[
"Representam grupos sociais do Brasil Império e servem para criticar diretamente a escravidão.",
"São heróis exemplares que vencem os obstáculos pela virtude e dão ao leitor uma lição moral explícita.",
"São personagens planas, sem conflito interior, definidas apenas pela profissão que exercem.",
"Representam, de forma alegórica, as três raças formadoras do povo brasileiro.",
"Dominadas por paixões extremas, agem de modo transgressor e fatalista, o que aproxima a obra do gótico e do byronismo, e não de um projeto nacionalista."],"E"))
# ---- Poema Sujo (aula 5)
X.append(mk(5,16,"Sobre a composição de Poema sujo, de Ferreira Gullar, assinale a alternativa correta.",[
"Foi escrito em Paris, em 1950, em sonetos de métrica rigorosa, seguindo o ideal parnasiano de perfeição formal.",
"Foi escrito em São Luís, sob proteção do governo, e é um conjunto de haicais sobre a natureza.",
"Foi escrito no exílio, em Buenos Aires, em 1975; em versos livres e linguagem coloquial, reconstitui a memória do poeta, da infância em São Luís à situação política do país.",
"É um poema épico em decassílabos e oitava rima, que narra a fundação do Maranhão por heróis portugueses.",
"É uma coletânea de poemas concretos, em que a disposição gráfica das palavras na página substitui a linguagem verbal."],"C"))
X.append(mk(5,17,"Considere as afirmativas a seguir sobre Poema sujo.",[
"I e II, apenas.","II e IV, apenas.","I e III, apenas.","I, III e IV, apenas.","I, II, III e IV."],"D",items=[
"I. Trata-se de um poema longo, em versos livres, que mistura memória pessoal, vida cotidiana e reflexão política.",
"II. O poema obedece à métrica e à rima do Parnasianismo, com vocabulário erudito e alheio ao cotidiano.",
"III. O adjetivo “sujo” pode ser associado à recusa de uma poesia “limpa” e idealizada, em favor da experiência concreta, do corpo, das coisas e da vida social.",
"IV. A circulação do poema no Brasil começou por gravações de sua leitura, o que reforça a oralidade do texto."],
after="Estão corretas:"))
X.append(mk(5,18,"Em Poema sujo, são frequentes as repetições, as onomatopeias e os ritmos próximos da fala e do canto. Esses recursos",[
"reforçam a oralidade e a dimensão corporal e sensorial da memória, afastando o poema de uma linguagem de gabinete.",
"mostram a influência do Barroco, pelo uso de jogos conceituais e de antíteses religiosas.",
"revelam a adesão do poeta à métrica e à rima do Arcadismo.",
"caracterizam o poema como epopeia clássica, com invocação às musas e narração de feitos heroicos.",
"indicam que o poema é exemplo de poesia concreta, de rígida organização gráfica e sem sentido referencial."],"A"))
X.append(mk(5,19,"Antes de escrever Poema sujo, Ferreira Gullar teve uma trajetória marcada por diferentes momentos. Assinale a alternativa que a descreve corretamente.",[
"Manteve-se sempre afastado da política e produziu apenas poesia de caráter puramente formal.",
"Foi um dos fundadores do Parnasianismo no Brasil e rejeitou qualquer experimentação.",
"Foi poeta simbolista e viveu toda a vida em São Luís, sem nunca deixar o Maranhão.",
"Participou do Modernismo de 1922 e, depois, abandonou a literatura para atuar como diplomata.",
"Integrou o Neoconcretismo e, depois, o Centro Popular de Cultura (CPC), aproximando-se de uma poesia de função social; perseguido pela ditadura, exilou-se em vários países."],"E"))
X.append(mk(5,20,"A publicação de Poema sujo, em 1976, dialoga com o contexto da ditadura militar brasileira. Assinale a alternativa correta.",[
"O poema ignora o contexto político e se limita a uma exaltação da natureza maranhense.",
"O poema, escrito no exílio, une a memória individual à experiência coletiva de repressão e resistência, o que faz dele um texto de testemunho e denúncia sem abandonar a dimensão lírica.",
"O poema foi escrito para apoiar o governo militar e celebrar o “milagre econômico”.",
"O poema é uma crônica jornalística em prosa, sem recursos poéticos, escrita para ser publicada em jornais.",
"O poema defende a volta ao ideal arcádico de fuga da cidade e de retorno à vida pastoril."],"B"))
# ---- O Demônio Familiar (aula 7)
X.append(mk(7,11,"Quanto ao gênero e à época de O demônio familiar, de José de Alencar, assinale a alternativa correta.",[
"É uma tragédia em verso, de tema mitológico, escrita segundo os modelos do Classicismo.",
"É uma comédia de costumes em quatro atos, que critica, com humor, hábitos da sociedade fluminense do Segundo Reinado.",
"É um romance indianista em que o herói nativo simboliza a formação da nação brasileira.",
"É um poema épico sobre a colonização do sertão, escrito em oitava rima.",
"É um auto religioso de inspiração medieval, destinado à catequese."],"B"))
X.append(mk(7,12,"Sobre a personagem Pedro, de O demônio familiar, assinale a alternativa correta.",[
"É um fidalgo arruinado que tenta recuperar a fortuna da família por meio de um casamento vantajoso.",
"É um médico idealista que se dedica a combater a escravidão e a defender os pobres.",
"É um padre que aconselha as personagens e representa a moral da Igreja Católica.",
"É um moleque, escravo doméstico de Eduardo, que, movido pelo desejo de tornar-se cocheiro, passa a intrigar e a manipular as relações do senhor.",
"É um jornalista que denuncia, nas páginas do jornal, os desmandos do governo imperial."],"D"))
X.append(mk(7,13,"Considere as afirmativas a seguir sobre O demônio familiar.",[
"I, II e III, apenas.","I e IV, apenas.","II e IV, apenas.","III e IV, apenas.","I, II, III e IV."],"A",items=[
"I. O título é irônico: o “demônio” é o criado de confiança que, dentro da casa, provoca confusões e desordem.",
"II. A peça questiona, de modo indireto, os efeitos da escravidão doméstica sobre senhores e escravos, sem propor claramente o fim do sistema.",
"III. O conflito gira em torno de casamentos e dinheiro: arranjos matrimoniais, interesses e aparências movimentam o enredo.",
"IV. O texto é escrito em versos alexandrinos e linguagem solene, como nas tragédias clássicas."],
after="Estão corretas:"))
X.append(mk(7,14,"Em relação a O demônio familiar, marque as afirmativas abaixo com V (verdadeiro) ou F (falso).",VF5,"C",items=[
"( ) A ação se passa em ambiente doméstico urbano do Rio de Janeiro, ligado à burguesia do Segundo Reinado.",
"( ) A linguagem é rebuscada e poética, e o texto é escrito em versos decassílabos.",
"( ) As intrigas de Pedro produzem desentendimentos entre os casais e revelam interesses ocultos das personagens.",
"( ) A peça foi escrita para exaltar o indígena como herói nacional."],
after="Assinale a alternativa que apresenta a sequência correta, de cima para baixo."))
X.append(mk(7,15,"O demônio familiar está ligado ao teatro realista, que se difundiu em meados do século XIX. Esse teatro propunha",[
"temas mitológicos, personagens de linhagem divina e linguagem distante da fala cotidiana.",
"o abandono do enredo em favor de cenas oníricas, sem relação lógica entre si.",
"a exaltação de heróis medievais em lutas pela fé e pela honra.",
"a recusa de qualquer finalidade social, em nome da arte pela arte.",
"o retrato de costumes contemporâneos, em linguagem próxima da fala, com intenção moralizadora e crítica a vícios sociais."],"E"))
X.append(mk(7,16,"A relação entre Pedro e Eduardo, em O demônio familiar, mostra que",[
"a convivência afetuosa entre os dois elimina a diferença de condição, e Pedro é tratado como igual em todos os aspectos.",
"a proximidade doméstica e o tom de falsa cordialidade escondem a desigualdade: Pedro depende do senhor e usa a esperteza para obter vantagens, sem deixar de ser propriedade.",
"Eduardo teme Pedro e age sempre sob suas ordens, o que inverte a hierarquia social da época.",
"Pedro é um escravo de eito, sem contato com a família, e atua apenas na lavoura.",
"os dois são irmãos de criação e partilham a mesma herança."],"B"))
X.append(mk(7,17,"Na peça, Pedro age como uma espécie de “corretor de casamentos”. A crítica de Alencar, nesse ponto, recai sobre",[
"a ausência de casamentos na sociedade brasileira da época.",
"o desprezo das famílias pelo trabalho manual.",
"a proibição de casamentos entre pessoas de classes diferentes.",
"o casamento tratado como negócio, em que dote, interesse e aparência pesam mais que o afeto.",
"a influência da Igreja nas escolhas matrimoniais dos jovens."],"D"))
X.append(mk(7,18,"Sobre a obra de José de Alencar, assinale a alternativa correta.",[
"Escreveu romances urbanos (Lucíola, Senhora), indianistas (Iracema, O Guarani) e peças de teatro (O demônio familiar, Mãe).",
"Produziu exclusivamente romances indianistas e nunca escreveu para o teatro.",
"Foi poeta parnasiano e sua obra limita-se a sonetos de métrica rigorosa.",
"Escreveu apenas obras de crítica literária e de jornalismo esportivo.",
"Foi um dos fundadores do Simbolismo e recusou o projeto de construção de uma literatura nacional."],"A"))
Q+=X
Q.sort(key=lambda q:(q['aula'],q['n']))
json.dump(d,open('Qall.json','w'),ensure_ascii=False)
print(len(Q))
