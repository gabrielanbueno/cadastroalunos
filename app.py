"""
================================================================================
 SISTEMA DE GESTÃO DE ALUNOS - ESCOLA
 Streamlit + SQLite | Arquitetura em Camadas (tudo em um único arquivo)
================================================================================

Camadas:
  1. DATA LAYER        -> Acesso e persistência no SQLite (escola.db)
  2. BUSINESS LAYER     -> Regras de negócio (cálculo de média/status, validações)
  3. PRESENTATION LAYER -> Interface Streamlit (sidebar, formulários, tabelas)

Autor: Gerado com auxílio de IA
================================================================================
"""

import sqlite3
import re
from contextlib import contextmanager

import pandas as pd
import streamlit as st

# ==============================================================================
# CONFIGURAÇÃO GERAL DA PÁGINA
# ==============================================================================

st.set_page_config(
    page_title="Sistema Escolar | Gestão de Alunos",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

DB_NAME = "escola.db"


# ==============================================================================
# 1. DATA LAYER — Camada de Persistência (SQLite)
# ==============================================================================

@contextmanager
def get_connection():
    """
    Context manager que abre e fecha a conexão com o SQLite automaticamente,
    garantindo que a conexão seja sempre liberada mesmo em caso de erro.
    """
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # permite acessar colunas pelo nome
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def criar_tabela():
    """Cria a tabela 'alunos' automaticamente caso ela não exista."""
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS alunos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_completo TEXT NOT NULL,
                email TEXT NOT NULL,
                matricula TEXT NOT NULL UNIQUE,
                curso TEXT NOT NULL,
                nota1 FLOAT NOT NULL,
                nota2 FLOAT NOT NULL,
                media FLOAT NOT NULL,
                status TEXT NOT NULL
            )
            """
        )


def inserir_aluno(nome, email, matricula, curso, nota1, nota2, media, status):
    """Insere um novo aluno no banco. Levanta exceção se a matrícula já existir."""
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO alunos (nome_completo, email, matricula, curso, nota1, nota2, media, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (nome, email, matricula, curso, float(nota1), float(nota2), float(media), status),
        )


def listar_alunos():
    """Retorna todos os alunos cadastrados como DataFrame do pandas."""
    with get_connection() as conn:
        df = pd.read_sql_query("SELECT * FROM alunos ORDER BY nome_completo", conn)
    return df


def buscar_aluno_por_id(aluno_id):
    """Retorna os dados de um único aluno pelo ID."""
    with get_connection() as conn:
        cur = conn.execute("SELECT * FROM alunos WHERE id = ?", (aluno_id,))
        row = cur.fetchone()
    return dict(row) if row else None


def atualizar_aluno(aluno_id, nome, email, matricula, curso, nota1, nota2, media, status):
    """Atualiza os dados de um aluno existente."""
    with get_connection() as conn:
        conn.execute(
            """
            UPDATE alunos
               SET nome_completo = ?, email = ?, matricula = ?, curso = ?,
                   nota1 = ?, nota2 = ?, media = ?, status = ?
             WHERE id = ?
            """,
            (nome, email, matricula, curso, float(nota1), float(nota2), float(media), status, aluno_id),
        )


def excluir_aluno(aluno_id):
    """Remove um aluno do banco de dados pelo ID."""
    with get_connection() as conn:
        conn.execute("DELETE FROM alunos WHERE id = ?", (aluno_id,))


# ==============================================================================
# 2. BUSINESS LAYER — Regras de Negócio
# ==============================================================================

def calcular_media(nota1: float, nota2: float) -> float:
    """Média = (Nota 1 + Nota 2) / 2"""
    return round((float(nota1) + float(nota2)) / 2, 2)


def calcular_status(media: float) -> str:
    """Se Média >= 7.0 -> Aprovado, caso contrário -> Reprovado."""
    return "Aprovado" if media >= 7.0 else "Reprovado"


def validar_email(email: str) -> bool:
    """Validação simples de formato de e-mail."""
    padrao = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return re.match(padrao, email) is not None


def validar_dados_aluno(nome, email, matricula, curso, nota1, nota2):
    """
    Valida os dados de entrada do formulário.
    Retorna uma lista de mensagens de erro (vazia se tudo estiver ok).
    """
    erros = []

    if not nome or not nome.strip():
        erros.append("O nome completo é obrigatório.")

    if not email or not validar_email(email.strip()):
        erros.append("Informe um e-mail válido.")

    if not matricula or not matricula.strip():
        erros.append("A matrícula é obrigatória.")

    if not curso or not curso.strip():
        erros.append("O curso é obrigatório.")

    try:
        n1 = float(nota1)
        if not (0.0 <= n1 <= 10.0):
            erros.append("Nota 1 deve estar entre 0.0 e 10.0.")
    except (TypeError, ValueError):
        erros.append("Nota 1 deve ser um número válido.")

    try:
        n2 = float(nota2)
        if not (0.0 <= n2 <= 10.0):
            erros.append("Nota 2 deve estar entre 0.0 e 10.0.")
    except (TypeError, ValueError):
        erros.append("Nota 2 deve ser um número válido.")

    return erros


# ==============================================================================
# 3. PRESENTATION LAYER — Interface Streamlit
# ==============================================================================

def aplicar_tema_dark_futurista():
    """
    Injeta CSS customizado para um layout dark futurista.
    A fonte DS-Digital (estilo display digital) é carregada via @font-face.
    Para funcionar, baixe a fonte gratuita em:
    https://www.dafont.com/pt/ds-digital.font (autor: Dusit Supasawat)
    e salve o arquivo .ttf em: assets/DS-DIGI.TTF
    Caso o arquivo não esteja presente, o navegador usa a fonte de fallback
    ('Orbitron', monospace) automaticamente, sem quebrar a aplicação.
    """
    st.markdown(
        """
        <style>
        @font-face {
            font-family: 'DS-Digital';
            src: url('assets/DS-DIGI.TTF') format('truetype');
            font-weight: normal;
            font-style: normal;
        }

        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'Orbitron', 'DS-Digital', monospace;
        }

        .stApp {
            background: radial-gradient(circle at top left, #0d1321 0%, #05060a 70%);
            color: #e6faff;
        }

        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0a0f1c 0%, #05070d 100%);
            border-right: 1px solid #00f0ff33;
        }

        h1, h2, h3 {
            font-family: 'DS-Digital', 'Orbitron', monospace;
            color: #00f0ff;
            text-shadow: 0 0 8px #00f0ff88, 0 0 20px #00f0ff33;
            letter-spacing: 1px;
        }

        .stButton > button {
            background: linear-gradient(90deg, #00f0ff22, #00f0ff11);
            color: #00f0ff;
            border: 1px solid #00f0ff88;
            border-radius: 6px;
            box-shadow: 0 0 10px #00f0ff33;
            transition: all 0.2s ease-in-out;
        }
        .stButton > button:hover {
            background: #00f0ff33;
            box-shadow: 0 0 18px #00f0ffaa;
            color: #ffffff;
        }

        div[data-testid="stMetricValue"] {
            color: #00f0ff;
            text-shadow: 0 0 10px #00f0ff88;
        }

        .stTextInput input, .stNumberInput input, .stSelectbox div, .stTextArea textarea {
            background-color: #0d1321 !important;
            color: #e6faff !important;
            border: 1px solid #00f0ff55 !important;
        }

        .stDataFrame {
            border: 1px solid #00f0ff44;
            box-shadow: 0 0 15px #00f0ff22;
        }

        hr {
            border-color: #00f0ff33;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def tela_cadastrar():
    st.header("📝 Cadastrar Aluno")

    with st.form("form_cadastro", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("Nome Completo *")
            matricula = st.text_input("Matrícula *")
            curso = st.text_input("Curso *")
        with col2:
            email = st.text_input("E-mail *")
            nota1 = st.number_input("Nota 1", min_value=0.0, max_value=10.0, step=0.1, format="%.1f")
            nota2 = st.number_input("Nota 2", min_value=0.0, max_value=10.0, step=0.1, format="%.1f")

        enviado = st.form_submit_button("💾 Salvar Aluno")

    if enviado:
        erros = validar_dados_aluno(nome, email, matricula, curso, nota1, nota2)

        if erros:
            for erro in erros:
                st.error(erro)
            return

        media = calcular_media(nota1, nota2)
        status = calcular_status(media)

        try:
            inserir_aluno(nome.strip(), email.strip(), matricula.strip(), curso.strip(), nota1, nota2, media, status)
            st.success(f"Aluno '{nome}' cadastrado com sucesso! Média: {media} | Status: {status}")
        except sqlite3.IntegrityError:
            st.error(f"Já existe um aluno cadastrado com a matrícula '{matricula}'.")
        except Exception as e:
            st.error(f"Erro ao salvar aluno: {e}")


def tela_consultar():
    st.header("🔎 Consultar Alunos")

    df = listar_alunos()

    if df.empty:
        st.warning("Nenhum aluno cadastrado até o momento.")
        return

    busca = st.text_input("Buscar por nome ou matrícula")

    if busca:
        filtro = (
            df["nome_completo"].str.contains(busca, case=False, na=False)
            | df["matricula"].str.contains(busca, case=False, na=False)
        )
        df_filtrado = df[filtro]
    else:
        df_filtrado = df

    colunas_exibicao = {
        "nome_completo": "Nome",
        "matricula": "Matrícula",
        "curso": "Curso",
        "nota1": "Nota 1",
        "nota2": "Nota 2",
        "media": "Média",
        "status": "Status",
    }

    df_exibicao = df_filtrado[list(colunas_exibicao.keys())].rename(columns=colunas_exibicao)

    st.dataframe(df_exibicao, use_container_width=True, hide_index=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Alunos", len(df_filtrado))
    col2.metric("Aprovados", int((df_filtrado["status"] == "Aprovado").sum()))
    col3.metric("Reprovados", int((df_filtrado["status"] == "Reprovado").sum()))


def tela_editar():
    st.header("✏️ Editar Aluno")

    df = listar_alunos()

    if df.empty:
        st.warning("Nenhum aluno cadastrado para editar.")
        return

    opcoes = {f"{row['nome_completo']} — Matrícula: {row['matricula']}": row["id"] for _, row in df.iterrows()}
    selecionado = st.selectbox("Selecione o aluno", list(opcoes.keys()))
    aluno_id = opcoes[selecionado]

    aluno = buscar_aluno_por_id(aluno_id)

    if not aluno:
        st.error("Aluno não encontrado.")
        return

    with st.form("form_editar"):
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("Nome Completo *", value=aluno["nome_completo"])
            matricula = st.text_input("Matrícula *", value=aluno["matricula"])
            curso = st.text_input("Curso *", value=aluno["curso"])
        with col2:
            email = st.text_input("E-mail *", value=aluno["email"])
            nota1 = st.number_input(
                "Nota 1", min_value=0.0, max_value=10.0, step=0.1, format="%.1f", value=float(aluno["nota1"])
            )
            nota2 = st.number_input(
                "Nota 2", min_value=0.0, max_value=10.0, step=0.1, format="%.1f", value=float(aluno["nota2"])
            )

        atualizar = st.form_submit_button("🔄 Atualizar Dados")

    if atualizar:
        erros = validar_dados_aluno(nome, email, matricula, curso, nota1, nota2)

        if erros:
            for erro in erros:
                st.error(erro)
            return

        media = calcular_media(nota1, nota2)
        status = calcular_status(media)

        try:
            atualizar_aluno(
                aluno_id, nome.strip(), email.strip(), matricula.strip(), curso.strip(), nota1, nota2, media, status
            )
            st.success(f"Dados de '{nome}' atualizados com sucesso! Nova média: {media} | Status: {status}")
        except sqlite3.IntegrityError:
            st.error(f"Já existe outro aluno cadastrado com a matrícula '{matricula}'.")
        except Exception as e:
            st.error(f"Erro ao atualizar aluno: {e}")


def tela_excluir():
    st.header("🗑️ Excluir Aluno")

    df = listar_alunos()

    if df.empty:
        st.warning("Nenhum aluno cadastrado para excluir.")
        return

    opcoes = {f"{row['nome_completo']} — Matrícula: {row['matricula']}": row["id"] for _, row in df.iterrows()}
    selecionado = st.selectbox("Selecione o aluno a ser excluído", list(opcoes.keys()))
    aluno_id = opcoes[selecionado]

    aluno = buscar_aluno_por_id(aluno_id)

    if aluno:
        st.info(
            f"**Nome:** {aluno['nome_completo']}  \n"
            f"**Matrícula:** {aluno['matricula']}  \n"
            f"**Curso:** {aluno['curso']}  \n"
            f"**Média:** {aluno['media']} | **Status:** {aluno['status']}"
        )

        confirmar = st.checkbox("⚠️ Confirmo que desejo excluir este aluno permanentemente.")

        if st.button("🗑️ Excluir Definitivamente", disabled=not confirmar):
            try:
                excluir_aluno(aluno_id)
                st.success(f"Aluno '{aluno['nome_completo']}' excluído com sucesso.")
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao excluir aluno: {e}")


def main():
    aplicar_tema_dark_futurista()
    criar_tabela()

    st.sidebar.title("🎓 Sistema Escolar")
    st.sidebar.caption("Gestão de Alunos — Dark Futurista")
    st.sidebar.markdown("---")

    menu = st.sidebar.radio(
        "Navegação",
        ["Cadastrar", "Consultar", "Editar", "Excluir"],
        label_visibility="collapsed",
    )

    st.sidebar.markdown("---")
    st.sidebar.caption("Banco de dados: `escola.db` (SQLite)")

    st.title("🎓 Gestão de Alunos")
    st.markdown("---")

    if menu == "Cadastrar":
        tela_cadastrar()
    elif menu == "Consultar":
        tela_consultar()
    elif menu == "Editar":
        tela_editar()
    elif menu == "Excluir":
        tela_excluir()


if __name__ == "__main__":
    main()
