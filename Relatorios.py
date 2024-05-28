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
            st.title("Login - Relatórios")
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

def generate_sla_pie_chart(df):
    sla_padrao = df['SLA PADRÃO (%)'].mean()
    sla_desejado = df['SLA DESEJADO (%)'].mean()
    labels = ['SLA Padrão', 'SLA Desejado']
    sizes = [sla_padrao, sla_desejado]
    colors = ['blue', 'orange']
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.pie(sizes, labels=labels, autopct='%.1f%%', startangle=90, colors=colors)
    ax.set_title('Média de SLA Padrão vs Desejado')
    return fig



def main():
    
    st.title(f"🛠️ Seja bem vindo {st.session_state.get('user', '').capitalize()}")

    st.write("""
    Este painel permite analisar e visualizar dados de atendimento ao cliente. Carregue um arquivo CSV para ver as estatísticas e gráficos gerados a partir dos dados.
    
    ### Funcionalidades:
    - 💾 **Upload e Leitura de Arquivo:** Carregue um arquivo CSV contendo os dados de atendimento.
    - 📊 **Análise de Dados:** Veja uma análise inicial dos dados.
    - 📈 **Geração de Gráficos:** Visualize diferentes gráficos baseados nos dados carregados.
    """)

    uploaded_file = st.file_uploader("Selecione um arquivo CSV no padrão export da Global")
    
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
    ### Informações Gerais dos Atendimentos
    - **Total de Atendimentos:** Soma de todas as chamadas atendidas e não atendidas.
    - **Atendidas:** Número total de chamadas atendidas.
    - **Não Atendidas:** Número total de chamadas não atendidas.
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

    st.title('Tempo Médio de Atendimentos')
    st.write("""
    ### Tempos Médios
    - **Tempo Médio de Atendimento:** Tempo médio que leva para atender uma chamada.
    - **Tempo Médio de Espera:** Tempo médio que uma chamada espera antes de ser atendida.
    - **Tempo Médio de Abandono:** Tempo médio até que uma chamada é abandonada (desistida pelo cliente).
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

    st.title("Comparação de Atendimentos")
    st.write("""
    ### Comparação de Desempenho ao Longo do Tempo
    - **Gráfico de Barras:** Mostra a média de chamadas atendidas por período.
    - **Gráfico de Linhas:** Exibe a tendência de atendimento ao longo do tempo.
    """)
    generate_bar_chart(df)
    generate_line_chart(df)

    st.title("🖨️ Imprima o relatório")
    st.image('./ctrlp.png', caption='basta pressionar CTRL + P para abrir a janela de impressão do navegador', use_column_width=True)

if __name__ == '__main__':
    main()
