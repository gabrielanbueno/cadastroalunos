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


## 📐 Regras de negócio

- **Média** = (Nota 1 + Nota 2) / 2
- **Status**: Média ≥ 7.0 → `Aprovado`; caso contrário → `Reprovado`
- Notas devem estar entre `0.0` e `10.0`
- Matrícula é única (não permite duplicidade)
