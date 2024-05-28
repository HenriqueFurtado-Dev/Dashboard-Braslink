import streamlit as st
import json
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

# Carregar dados existentes
data = load_data()

st.title("Registro de Ocorrências")

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

# Exibir dados já cadastrados
st.subheader("Ocorrências Cadastradas")
if data:
    for entry in data:
        st.write(f"**Nome:** {entry['nome']}")
        st.write(f"**Assuntos:** {', '.join(entry['assuntos'])}")
        st.write(f"**Protocolo:** {entry['protocolo']}")
        st.write(f"**Data do Ocorrido:** {entry['data_ocorrencia']}")
        st.write(f"**Comentário:** {entry['comentario']}")
        st.markdown("---")
else:
    st.write("Nenhuma ocorrência cadastrada.")
