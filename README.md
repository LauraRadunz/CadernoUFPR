# Cadernos de Estudo

> Este projeto veio em 2 zips por causa do limite de envio. Extraia os dois **na mesma pasta** (`cadernos-de-estudo`, mesclando): a parte 2 só completa a pasta `atl4`.

Site de questões do Extensivo UFPR: você responde, confirma e vê a alternativa correta. Tem caderno de erros, revisão por tópico, "Finalizar estudo" (guarda onde parou) e um botão **Explicar com o Gemini**.

Matérias: História, Filosofia, Biologia, Química, Física, Geografia, Matemática, Sociologia e Literatura.

## Como colocar no ar (link para sua amiga, sem baixar nada)

1. Crie um repositório novo no GitHub (por exemplo `cadernos-de-estudo`), **público**.
2. Envie o conteúdo desta pasta para a raiz do repositório. Pelo terminal:
   ```
   cd cadernos-de-estudo
   git init
   git add .
   git commit -m "Cadernos de estudo"
   git branch -M main
   git remote add origin https://github.com/SEU_USUARIO/cadernos-de-estudo.git
   git push -u origin main
   ```
   (Pelo site do GitHub, o upload aceita até 100 arquivos por vez; a pasta `atl4` tem 107, então envie em duas levas, ou use o GitHub Desktop.)
3. No repositório: **Settings → Pages → Build and deployment → Deploy from a branch → `main` / `(root)` → Save**.
4. Em 1 ou 2 minutos o site abre em `https://SEU_USUARIO.github.io/cadernos-de-estudo/`. É só mandar esse link: ela abre no navegador do celular ou do computador, sem instalar nada.

## Onde ficam os dados

Tudo que você responde (acertos, erros, onde parou) fica no **localStorage do navegador**, em cada aparelho. Isso significa:

- cada pessoa tem o próprio histórico (o da sua amiga não mistura com o seu);
- trocar de navegador/aparelho ou limpar os dados do site começa do zero;
- na tela inicial há **Exportar progresso** e **Importar progresso**: use para levar o histórico de um lugar para outro. O seu histórico atual está no link antigo (claude.ai), então exporte lá e importe no novo endereço. Se o botão de exportar não baixar dentro do claude.ai, avise.

## Botão "Explicar com o Gemini"

Ao tocar no botão, o site chama o Gemini direto do navegador e manda o enunciado completo (texto, alternativas, gabarito, sua resposta e as imagens da questão). Cada pessoa precisa colar a própria chave grátis do Gemini uma vez (aistudio.google.com/apikey). A chave fica só no navegador de quem colou e não entra no backup nem no repositório. A explicação gerada fica guardada no aparelho.

O modelo usado está em `GMODEL` (hoje `gemini-2.5-flash`), dentro de `index.html` e de `tools/newjs2.txt`.

## O que tem aqui

- `index.html`, `atl4/`, `img/`: o site pronto (é isso que o GitHub Pages serve).
- `tools/`: o código-fonte usado para gerar tudo (referência). `template.html` + `newjs2.txt` + `themes.css` são a base do site; `build_new.py` e `rebuild.py` montam os dados e o HTML; `make_pages.py` gera esta pasta; `ext3.py`, `parse3.py` e companhia leem os PDFs. Esses scripts têm caminhos da máquina onde foram criados e precisam dos PDFs originais, então servem de consulta; para usar o site você não precisa deles.
