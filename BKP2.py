import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns  # Incluindo seaborn para gráficos
import hmac
import math

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
</style>
"""

def check_password():
    def login_form():
        with st.form("Credentials"):
            st.image('logo-braslink.png', width=200)
            st.title("Login - Painel Global")
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")
            st.form_submit_button("Log in", on_click=password_entered)
            st.text("Feito por Henrique Furtado 💜")

    def password_entered():
        if st.session_state["username"] in st.secrets[
            "passwords"
        ] and hmac.compare_digest(
            st.session_state["password"],
            st.secrets.passwords[st.session_state["username"]],
        ):
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

def generate_first_chart(atendidas, nao_atendidas):
    sizes = [atendidas, nao_atendidas]
    labels = [f'Atendidas\n{atendidas}', f'Não Atendidas\n{nao_atendidas}']
    colors = ['green', 'red']
    explode = [0.1, 0]
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.pie(sizes, labels=labels, autopct='%.1f%%', explode=explode, startangle=90, colors=colors)
    ax.set_title('(SLA) Produzido')
    ax.legend(loc="upper right", labels=labels)
    return fig

def generate_second_chart(objetivo_atendimento, sla_minimo):
    sizes = [objetivo_atendimento, sla_minimo]
    labels = [f'Atendimentos Totais \n{objetivo_atendimento}', f'Não Atendidas(SLA) \n{sla_minimo}']
    cores = ['cyan', 'yellow']
    explode = [0.1, 0]
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.pie(sizes, labels=labels, autopct='%.1f%%', explode=explode, startangle=90, colors=cores)
    ax.set_title('(SLA) Objetivo')
    ax.legend(loc="upper right", labels=labels)
    return fig

def generate_bar_chart(df):
    plt.figure(figsize=(10, 6))
    sns.barplot(x='PERÍODO', y='ATENDIDAS', data=df)
    plt.xlabel('Período')
    plt.ylabel('Média de Atendidas')
    plt.title('Comparação de Médias de Atendidas por Período')
    plt.xticks(rotation=45)
    plt.gca().set_xticklabels(df['PERÍODO'][::-1])
    st.pyplot(plt)

def generate_line_chart(df):
    plt.figure(figsize=(10, 6))
    plt.plot(df['PERÍODO'], df['ATENDIDAS'], marker='o', color='b')
    plt.xlabel('Período')
    plt.ylabel('Média de Atendidas')
    plt.title('Média de Atendidas por Período')
    plt.xticks(rotation=45)
    plt.grid(True)
    st.pyplot(plt)

def main():
    st.title(f"🛠️ Seja bem vindo {st.session_state.get('user', '').capitalize()}")

    st.write("""
        Este script realiza várias tarefas para analisar e visualizar dados de atendimento. Abaixo estão as funcionalidades detalhadas:

        ### 💾 Upload e Leitura de Arquivo
        """)

    uploaded_file = st.file_uploader("Selecione um arquivo CSV no padrão export da Global, Esperamos que você aproveite a aplicação e obtenha insights valiosos dos seus dados! 😊")

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file, sep=';', encoding='latin1')
            df.columns = df.columns.str.strip()
            first_analyse(df)
        except Exception as e:
            st.error(f"Erro ao ler o arquivo: {e}")

def first_analyse(df):
    st.write(df.head())

    atendidas = df['ATENDIDAS'].sum()
    nao_atendidas = df['NÃO ATENDIDAS'].sum()
    atendimento_total = atendidas + nao_atendidas

    st.markdown(style, unsafe_allow_html=True)

    st.title('Informações Totais')
    st.write("""
        ### 📊 Análise de Dados
        - **Função `first_analyse(df)`:
        - ** Realiza a primeira análise dos dados importados do CSV, mostrando as primeiras linhas e calculando estatísticas importantes.
             """)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f'<div class="square"><span class="titulo">Total:</span>{atendimento_total}</div>', unsafe_allow_html=True)

    with col2:
        st.markdown(f'<div class="square"><span class="titulo-atendidas">Atendidas:</span>{atendidas}</div>', unsafe_allow_html=True)

    with col3:
        st.markdown(f'<div class="square"><span class="titulo-nao-atendidas">Não Atendidas:</span>{nao_atendidas}</div>', unsafe_allow_html=True)

    fig1 = generate_first_chart(atendidas, nao_atendidas)
    fig2 = generate_second_chart(atendimento_total - math.trunc((atendimento_total / 100) * 15), math.trunc((atendimento_total / 100) * 15))

    col1, col2 = st.columns(2)
    with col1:
        st.pyplot(fig1)

    with col2:
        st.pyplot(fig2)

    st.title('Tempo médio')
    st.write("""
        ### 🕒 Cálculo de Tempos Médios
        - **Função `first_analyse(df)`:
        - ** Realiza a primeira análise dos dados importados do CSV, mostrando as primeiras linhas e calculando estatísticas importantes.
             """)

    df.rename(columns={'T.M. ATEND.': 'tempo_medio_atend', 'T.M. ABAND.': 'tempo_medio_abandono', 'T.M. ESPERA': 'tempo_medio_espera'}, inplace=True)

    def format_mean_time(column):
        mean_timedelta = pd.to_timedelta(column).mean()
        minutes = (mean_timedelta.seconds % 3600) // 60
        seconds = mean_timedelta.seconds % 60
        return f"{minutes:02d}:{seconds:02d}"

    atendimento = format_mean_time(df['tempo_medio_atend'])
    espera = format_mean_time(df['tempo_medio_espera'])
    abandono = format_mean_time(df['tempo_medio_abandono'])

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f'<div class="square"><span class="titulo">ATENDIMENTO:</span>{atendimento}</div>', unsafe_allow_html=True)

    with col2:
        st.markdown(f'<div class="square"><span class="titulo-atendidas">ESPERA:</span>{espera}</div>', unsafe_allow_html=True)

    with col3:
        st.markdown(f'<div class="square"><span class="titulo-nao-atendidas">ABANDONO:</span>{abandono}</div>', unsafe_allow_html=True)

    st.title("Comparação de atendimentos")
    st.write("""
        ### 📈 Geração de Gráficos
        - **Função `generate_first_chart(atendidas, nao_atendidas)`:** Gera um gráfico de pizza mostrando a proporção de atendimentos realizados e não realizados.
        - **Função `generate_second_chart(objetivo_atendimento, sla_minimo)`:** Cria outro gráfico de pizza para comparar os atendimentos totais com os não atendidos dentro do SLA desejado.
        - **Função `generate_period_chart(PERÍODO, ATENDIDAS)`:** Cria um gráfico de barras para comparar a quantidade de atendimentos por período.
        """)
    generate_bar_chart(df)
    generate_line_chart(df)

if __name__ == '__main__':
    main()
