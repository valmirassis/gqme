import streamlit as st
import streamlit.components.v1 as components
st.set_page_config(page_title="Gerador de Questões Múltipla Escolha", layout="wide")

st.markdown("## 📌 Questionário")
st.write("Responda o questionário incorporado abaixo ou clique no link para abrir no Google Forms.")


st.link_button("🌎 Abrir formulário no Forms", "https://forms.gle/pferQfzHJjwYN7Nf9")
components.iframe(
    src="https://docs.google.com/forms/d/e/1FAIpQLScXu83b0Xw9b8bSqb8oKHjZByzHai9Sedm3R2Mk14OBv8gZ0A/viewform?embedded=true",
    width=700,
    height=5000
)