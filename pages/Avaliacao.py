import streamlit as st
from streamlit_star_rating import st_star_rating
from datetime import datetime, timedelta
import json
import pandas as pd
import io
import os
import hmac

def check_password():
    def login_form():
        with st.form("Credentials"):
            st.image('logo-braslink.png', width=200)
            st.title("Login - Painel de Avaliações")
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")
            st.form_submit_button("Log in", on_click=password_entered)
            st.text("Feito por Henrique Furtado 💜")

    def password_entered():
        if st.session_state["username"] in st.secrets["passwords"] and hmac.compare_digest(
                st.session_state["password"],
                st.secrets.passwords[st.session_state["username"]]):
            st.session_state["password_correct"] = True
            st.session_state["user"] = st.session_state["username"]  # Armazena o nome do usuário na sessão
            del st.session_state["password"]
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if st.session_state.get("password_correct", False):
        return True

    login_form()
    if "password_correct" in st.session_state:
        st.error("😕 Usuário não encontrado ou senha incorreta")
    return False


if not check_password():
    st.stop()

st.title("🏆 Avaliação de Desempenho")
st.write("""Aqui está uma avaliação geral, e um pequeno resumo do desempenho da equipe de atendimento ao longo do tempo junto com feedbacks de pontos importantes de melhoras""")

# Seleção de período
periodo = st.selectbox(
    "Selecione o período de avaliação",
    ["Última semana", "Últimos 15 dias", "Últimos 30 dias", "Últimos 90 dias"]
)

# Obter data atual
data_atual = datetime.now()

# Calcular data inicial com base no período selecionado
if periodo == "Última semana":
    data_inicial = data_atual - timedelta(days=7)
elif periodo == "Últimos 15 dias":
    data_inicial = data_atual - timedelta(days=15)
elif periodo == "Últimos 30 dias":
    data_inicial = data_atual - timedelta(days=30)
else:  # "Últimos 90 dias"
    data_inicial = data_atual - timedelta(days=90)

st.write(f"Data atual: {data_atual.strftime('%d/%m/%Y')}")
st.write(f"Data de início do período selecionado: {data_inicial.strftime('%d/%m/%Y')}")

# Avaliação
velocidade = st_star_rating("Velocidade no Atendimento", maxValue=5, defaultValue=3, key="rating_velocidade")
qualidade = st_star_rating("Qualidade no Atendimento", maxValue=5, defaultValue=3, key="rating_qualidade")
resolucao = st_star_rating("Resolução de Problemas", maxValue=5, defaultValue=3, key="rating_resolucao")
consistencia = st_star_rating("Consistência entre os atendimentos", maxValue=5, defaultValue=3, key="rating_consistencia")
conhecimento = st_star_rating("Conhecimento técnico dos atendentes", maxValue=5, defaultValue=3, key="rating_conhecimento")

st.title("Feedback")
st.write("""Deixe um feedback sobre o atendimento da equipe em geral levando em consideração os pontos abaixo:""")
st.write("""
- **Tempo de Atendimento:** Tempo que leva para ser atendido.
- **Qualidade do Atendimento:** Qualidade do atendimento prestado.
- **Resolução de Problemas:** Capacidade de resolver problemas.
- **Feedback:** Comentários adicionais.
""")
feedback = st.text_area("Feedback", height=200)

st.title("Resumo")
st.write(f"Período de avaliação: {periodo}")
st.write(f"Data de início avaliada: {data_inicial.strftime('%d/%m/%Y')}")
st.write(f"Data final avaliada: {data_atual.strftime('%d/%m/%Y')}")
st.write(f"Nota dada para velocidade de atendimento: {velocidade}")
st.write(f"Nota dada para qualidade de atendimento: {qualidade}")
st.write(f"Nota dada para resolução de atendimento: {resolucao}")
st.write(f"Nota dada para consistência de atendimento: {consistencia}")
st.write(f"Nota dada para conhecimento técnico dos atendentes: {conhecimento}")
st.write(f"Feedback: {feedback}")

submitted = st.button("Enviar Avaliação")

if submitted:
    # Carregar avaliações existentes
    json_file = 'avaliacoes.json'
    if os.path.exists(json_file):
        with open(json_file, 'r', encoding='utf-8') as f:
            avaliacoes = json.load(f)
    else:
        avaliacoes = []

    # Adicionar nova avaliação ao final da lista
    nova_avaliacao = {
        "Periodo de avaliacao": periodo,
        "Data de inicio avaliada": data_inicial.strftime('%d/%m/%Y'),
        "Data final avaliada": data_atual.strftime('%d/%m/%Y'),
        "Velocidade no Atendimento": velocidade,
        "Qualidade no Atendimento": qualidade,
        "Resolução de Problemas": resolucao,
        "Consistência entre os atendimentos": consistencia,
        "Conhecimento técnico dos atendentes": conhecimento,
        "Feedback": feedback
    }
    avaliacoes.append(nova_avaliacao)

    # Salvar todas as avaliações no arquivo JSON
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(avaliacoes, f, ensure_ascii=False, indent=4)

    st.write("Avaliação enviada com sucesso!")

    # Disponibilizar JSON para download
    json_data = json.dumps(avaliacoes, ensure_ascii=False, indent=4)
    st.download_button(
        label="Baixar JSON",
        data=json_data,
        file_name=json_file,
        mime="application/json"
    )

    # Converter lista de avaliações para DataFrame e depois para CSV
    df = pd.DataFrame(avaliacoes)
    csv_data = df.to_csv(index=False, encoding='utf-8')
    csv_file = 'avaliacoes.csv'

    # Disponibilizar CSV para download
    st.download_button(
        label="Baixar CSV",
        data=csv_data,
        file_name=csv_file,
        mime="text/csv"
    )
