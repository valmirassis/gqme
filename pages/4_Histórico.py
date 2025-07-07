import streamlit as st

st.set_page_config(page_title="Gerador de Questões Múltipla Escolha", layout="wide")

st.markdown("## 📚 Questões geradas nesta sessão")
st.warning("As questões desta página ficam disponíveis somente durante a sessão de navegação, ao fechar o navegador ou "
         "abrir a página em nova aba as questões são apagadas.")

if "questoes_geradas" not in st.session_state:
    st.write("Sem questões geradas nesta sessão")
    st.session_state["questoes_geradas"] = []
for i, q in enumerate(st.session_state["questoes_geradas"], start=1):
    st.info(f"Questão(ões) geradas na solicitação {i}")
    st.markdown(f"\n\n{q}")
    st.divider()