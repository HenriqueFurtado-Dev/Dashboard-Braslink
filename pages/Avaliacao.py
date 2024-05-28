import streamlit as st
from streamlit_star_rating import st_star_rating

st.title("Avaliação de Desempenho")
st.write(""" Aqui está uma avaliação geral, e um pequeno resumo do desempenho da equipe de atendimento ao longo do tempo junto com feedbacks de pontos importantes de melhoras""")

velocidade = st_star_rating("Velocidade no Atendimento", maxValue=5, defaultValue=3, key="rating_velocidade")
# st.write(velocidade)

qualidade = st_star_rating("Qualidade no Atendimento", maxValue=5, defaultValue=3, key="rating_qualidade")
# st.write(qualidade)

resolucao = st_star_rating("Resolução de Problemas", maxValue=5, defaultValue=3, key="rating_resolucao")
# st.write(resolucao)

st.title("Feedback")
st.write("""Deixe um feedback sobre o atendimento da equipe em geral levando em consideração os pontos abaixo:""")
st.write("""
- **Tempo de Atendimento:** Tempo que leva para ser atendido.
- **Qualidade do Atendimento:** Qualidade do atendimento prestado.
- **Resolução de Problemas:** Capacidade de resolver problemas.
- **Feedback:** Comentários adicionais.
         """)
feedback = st.text_area("Feedback", height=200)

submitted = st.button("Enviar Avaliação")
