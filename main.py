import hmac
import math
from ssl import cert_time_to_seconds
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


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
.espaco {
    width: 60px;
    background-color: red;
}
.titulo-atendidas {
    color: green;
    font-size: 22px;
}
.titulo-nao-atendidas {
    color: red;
    font-size: 22px;
}

"""

def check_password():
    def login_form():
        # Creating a form to take user input
        with st.form("Credentials"):
            st.image('logo-braslink.png', width=200)
            st.title("Login - Painel Global")
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")
            st.form_submit_button("Log in", on_click=password_entered)
            st.text("Feito por Henrique Furtado 💜")

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

# Função para gerar o primeiro gráfico
def generate_first_chart(atendidas, nao_atendidas):
    # Configurando os dados do gráfico
    sizes = [atendidas, nao_atendidas]
    labels = [f'Atendidas\n{atendidas}', f'Não Atendidas\n{nao_atendidas}']
    colors = ['green', 'red']
    explode = [0.1, 0]

    # Criando o gráfico de pizza
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.pie(sizes, labels=labels, autopct='%.1f%%', explode=explode, startangle=90, colors=colors)

    # Adicionando título
    ax.set_title('(SLA) Produzido')

    # Adicionando legenda
    ax.legend(loc="upper right", labels=labels)

    return fig

# Função para gerar o segundo gráfico
def generate_second_chart(objetivo_atendimento, sla_minimo):
    # Configurando o gráfico
    sizes = [objetivo_atendimento, sla_minimo]
    labels = [f'Atendimentos Totais \n{objetivo_atendimento}', f'Não Atendidas(SLA) \n{sla_minimo}']
    cores = ['cyan', 'yellow']
    explode = [0.1, 0]

    # Criando o gráfico de pizza
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.pie(sizes, labels=labels, autopct='%.1f%%', explode=explode, startangle=90, colors=cores)

    # Adicionando título
    ax.set_title('(SLA) Objetivo')

    # Adicionando legenda
    ax.legend(loc="upper right", labels=labels)

    return fig

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

    st.title('Informações sobre atendimentos')

    # Define o conteúdo das três colunas
    col1, col2, col3 = st.columns(3)


    # Adiciona os campos quadrados às colunas
    with col1:
        st.markdown(f'<div class="square"><span class="titulo">Total:</span>{atendimento_total}</div>', unsafe_allow_html=True)

    with col2:
        st.markdown(f'<div class="square"><span class="titulo-atendidas">Atendidas:</span>{atendidas}</div>', unsafe_allow_html=True)

    with col3:
        st.markdown(f'<div class="square"><span class="titulo-nao-atendidas">Não Atendidas:</span>{nao_atendidas}</div>', unsafe_allow_html=True)
    
    # Gerando os gráficos
    fig1 = generate_first_chart(atendidas, nao_atendidas)
    fig2 = generate_second_chart(atendimento_total - math.trunc((atendimento_total / 100) * 15), math.trunc((atendimento_total / 100) * 15))

    # Exibindo os gráficos lado a lado com padding superior e inferior
    col1, col2 = st.columns(2)
    with col1:
        st.pyplot(fig1, clear_figure=True, use_container_width=True, padding_top=120, padding_bottom=120)

    with col2:
        st.pyplot(fig2, clear_figure=True, use_container_width=True, padding_top=120, padding_bottom=120)
    
    st.title('Tempo médio')

    df.rename(columns={'  T.M. ATEND.': 'tempo_medio_atend'}, inplace=True)
    df.rename(columns={'T.M. ABAND.': 'tempo_medio_abandono'}, inplace=True)
    df.rename(columns={'T.M. ESPERA': 'tempo_medio_espera'}, inplace=True)

    
    # Defina a função de tempo médio para calcular a média de tempo e converter para string formatada
    def format_mean_time(column):
        mean_timedelta = pd.to_timedelta(column).mean()  # Calcula o tempo médio
        minutes = (mean_timedelta.seconds % 3600) // 60  # Calcula os minutos
        seconds = mean_timedelta.seconds % 60  # Calcula os segundos
        return f"{minutes:02d}:{seconds:02d}"  # Formata a string para exibir

    # No main():
    # Calcula os tempos médios e formata para exibição
    atendimento = format_mean_time(df['tempo_medio_atend'])
    espera = format_mean_time(df['tempo_medio_espera'])
    abandono = format_mean_time(df['tempo_medio_abandono'])


    # Define o conteúdo das três colunas
    col1, col2, col3 = st.columns(3)

    # Adiciona os campos quadrados às colunas
    with col1:
        st.markdown(f'<div class="square"><span class="titulo">ATENDIMENTO:</span>{atendimento}</div>', unsafe_allow_html=True)

    with col2:
        st.markdown(f'<div class="square"><span class="titulo-atendidas">ESPERA:</span>{espera}</div>', unsafe_allow_html=True)

    with col3:
        st.markdown(f'<div class="square"><span class="titulo-nao-atendidas">ABANDONO:</span>{abandono}</div>', unsafe_allow_html=True)




if __name__ == '__main__':
    main()
