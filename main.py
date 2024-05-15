import pandas as pd
import streamlit as st

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


if __name__ == '__main__':
    main()