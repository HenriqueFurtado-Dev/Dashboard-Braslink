import streamlit as st
import json
import pandas as pd
from datetime import datetime
import hmac

def check_password():
    def login_form():
        with st.form("Credentials"):
            st.image('logo-braslink.png', width=200)
            st.title("Login - Painel de Anotações")
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


# Função para carregar os dados do arquivo JSON
def load_data():
    try:
        with open('data.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Função para salvar os dados no arquivo JSON
def save_data(data):
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4)

# Função para converter os dados para CSV
def convert_to_csv(data):
    df = pd.DataFrame(data)
    return df.to_csv(index=False)

# Carregar dados existentes
data = load_data()

st.title("🚨 Registro de Ocorrências")
st.write("Use o formulário abaixo para registrar uma nova ocorrência e posteriormente baixar os dados em formato JSON ou CSV.")

# Formulário de entrada de dados
with st.form("entry_form"):
    nome = st.selectbox("Nome do Funcionário", ["Gustavo P.", "Mariana Silva", "José Almeoida", "Ana Rodrigues"], index=0, help="Selecione o nome do funcionário")  # Nomes dos funcionários
    assuntos = st.multiselect("Assuntos", ["Problema Técnico", "Dúvida", "Sugestão", "Ótimo atendimento", "Outro"])  # Assuntos via checkboxes
    protocolo = st.text_input("Protocolo")  # Campo de texto
    data_ocorrencia = st.date_input("Data do Ocorrido", datetime.today())  # Seleção da data
    comentario = st.text_area("Comentário")  # Campo de comentário
    
    submitted = st.form_submit_button("Salvar registro")

    if submitted:
        if nome and assuntos and protocolo and comentario:
            new_entry = {
                "nome": nome,
                "assuntos": assuntos,
                "protocolo": protocolo,
                "data_ocorrencia": data_ocorrencia.strftime('%Y-%m-%d'),
                "comentario": comentario
            }
            data.append(new_entry)
            save_data(data)
            st.success("Ocorrência salva com sucesso!")
        else:
            st.error("Por favor, preencha todos os campos.")

# Adicionar botões para download
st.subheader("Baixar Dados")
json_data = json.dumps(data, indent=4)
st.download_button(label="Baixar JSON", data=json_data, file_name="data.json", mime="application/json")

csv_data = convert_to_csv(data)
st.download_button(label="Baixar CSV", data=csv_data, file_name="data.csv", mime="text/csv")


# Exibir dados já cadastrados
st.subheader("Ocorrências Cadastradas")
if data:
    for entry in data:
        st.write(f"**Nome:** {entry.get('nome', 'N/A')}")
        st.write(f"**Assuntos:** {', '.join(entry.get('assuntos', []))}")
        st.write(f"**Protocolo:** {entry.get('protocolo', 'N/A')}")
        st.write(f"**Data do Ocorrido:** {entry.get('data_ocorrencia', 'N/A')}")
        st.write(f"**Comentário:** {entry.get('comentario', 'N/A')}")
        st.markdown("---")
else:
    st.write("Nenhuma ocorrência cadastrada.")

