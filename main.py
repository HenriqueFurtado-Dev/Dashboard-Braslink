import hmac
import streamlit as st
import pandas as pd
import streamlit as st

# Define o estilo CSS inline
style = """
<style>
.square {
    width: 220px;
    border-radius: 10px;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    text-align: center;
    padding: 20px;
    font-size: 62px;
    border: 2px solid #000000;
}
.square .titulo {
    font-size: 22px;
}
</style>
"""

def check_password():
    def login_form():
        # Creating a form to take user input
        with st.form("Credentials"):
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")
            st.form_submit_button("Log in", on_click=password_entered)

    def password_entered():
        # Verify username and password
        if st.session_state["username"] in st.secrets[
            "passwords"
        ] and hmac.compare_digest(
            st.session_state["password"],
            st.secrets.passwords[st.session_state["username"]],
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the username or password.
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    # Return True if the username + password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show inputs for username + password.
    login_form()
    if "password_correct" in st.session_state:
        st.error("😕 Usuário não encontrado ou senha incorreta")
    return False


if not check_password():
    st.stop()



# Main Streamlit app starts here
def main():
    st.title("Braslink - Análises e Relatórios")
    uploaded_file = st.file_uploader("Selecione um arquivo CSV no padrão export da Global")
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file, sep=';', encoding='latin1')
            first_analyse(df)
        except Exception as e:
            st.error(f"Erro ao ler o arquivo: {e}")

def first_analyse(df):
    st.write(df.head())
    
    atendidas = df['ATENDIDAS'].sum() + df['NÃO ATENDIDAS'].sum()
    nao_atendidas = df['NÃO ATENDIDAS'].sum()  

    atendimento_total = atendidas + nao_atendidas
    

    # Adiciona o estilo CSS à página
    st.markdown(style, unsafe_allow_html=True)

    # Define o conteúdo das três colunas
    col1, col2, col3 = st.columns(3)

    # Adiciona os campos quadrados às colunas
    with col1:
        st.markdown(f'<div class="square"><span class="titulo">Total:</span>{atendimento_total}</div>', unsafe_allow_html=True)

    with col2:
        st.markdown(f'<div class="square"><span class="titulo">Atendidas:</span>{atendidas}</div>', unsafe_allow_html=True)

    with col3:
        st.markdown(f'<div class="square"><span class="titulo">Não Atendidas:</span>{nao_atendidas}</div>', unsafe_allow_html=True)


if __name__ == '__main__':
    main()