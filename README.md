# 🎓 Sistema Escolar — Gestão de Alunos

Aplicação em **Python + Streamlit + SQLite** para cadastro, consulta, edição e
exclusão de alunos, com cálculo automático de média e status (Aprovado/Reprovado).

## 📁 Estrutura de arquivos

```
escola-app/
├── app.py              # Código completo da aplicação (camadas: Data, Business, Presentation)
├── requirements.txt    # Dependências do projeto
├── assets/
│   └── DS-DIGI.TTF     # (opcional) fonte DS-Digital — ver seção "Fonte" abaixo
└── escola.db           # Criado automaticamente na primeira execução
```

## ▶️ Como rodar localmente

1. Crie e ative um ambiente virtual (recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate      # Linux/Mac
   venv\Scripts\activate         # Windows
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Rode a aplicação:
   ```bash
   streamlit run app.py
   ```

4. O navegador abrirá automaticamente em `http://localhost:8501`.
   O arquivo `escola.db` (SQLite) é criado sozinho na primeira execução, na
   mesma pasta do `app.py`.

## 🔤 Sobre a fonte DS-Digital

O layout usa a fonte **DS-Digital**, de Dusit Supasawat
(https://www.dafont.com/pt/ds-digital.font). Por licença, ela não pode ser
redistribuída automaticamente, então:

1. Baixe a fonte no link acima.
2. Copie o arquivo `.ttf` (ex.: `DS-DIGI.TTF`) para a pasta `assets/`.
3. O `app.py` já referencia `assets/DS-DIGI.TTF` via `@font-face`.

Caso o arquivo não esteja presente, a aplicação usa automaticamente a fonte
**Orbitron** (Google Fonts) como alternativa visual "digital/futurista",
sem quebrar o layout.

## 📤 Publicar no GitHub

1. Crie um repositório novo no GitHub (ex.: `sistema-escolar`).
2. No terminal, dentro da pasta do projeto:
   ```bash
   git init
   git add .
   git commit -m "Sistema de gestão de alunos - versão inicial"
   git branch -M main
   git remote add origin https://github.com/SEU-USUARIO/sistema-escolar.git
   git push -u origin main
   ```
   > Dica: adicione um `.gitignore` com `venv/` e `escola.db` se não quiser
   > versionar o ambiente virtual e o banco local.

## ☁️ Publicar no Streamlit Community Cloud

1. Acesse https://share.streamlit.io/ e faça login com sua conta GitHub.
2. Clique em **"New app"**.
3. Selecione o repositório `sistema-escolar` e a branch `main`.
4. Em **"Main file path"**, informe `app.py`.
5. Clique em **"Deploy"**.
6. Aguarde alguns instantes — o Streamlit Cloud vai instalar as dependências
   do `requirements.txt` e publicar sua aplicação automaticamente.
7. Toda vez que você der `git push` para a branch `main`, o app é atualizado
   sozinho na nuvem.

> ⚠️ Observação: o SQLite no Streamlit Community Cloud **não é persistente**
> entre reinicializações do app (o sistema de arquivos é efêmero). Para uso
> em produção real, considere migrar para um banco externo (ex. Postgres via
> Supabase/Neon) no futuro — para fins de estudo/demonstração, o SQLite local
> funciona perfeitamente.

## 📐 Regras de negócio

- **Média** = (Nota 1 + Nota 2) / 2
- **Status**: Média ≥ 7.0 → `Aprovado`; caso contrário → `Reprovado`
- Notas devem estar entre `0.0` e `10.0`
- Matrícula é única (não permite duplicidade)
