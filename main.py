from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import streamlit as st
import os

load_dotenv()
llm = GoogleGenerativeAI(model="models/gemini-1.5-pro-latest")
prompt = PromptTemplate.from_template("Atue como um professor de Ensino Superior e crie uma pergunta de múltipla escolha de 5 alternativas com a estrutura "
                                      "analise as afirmativas abaixo coloque 4 afirmativas com números romanos (não é necessário expressar isso no enunciado) "
                                      "e depois assinale quais estão corretas  sobre o tema {input}, o enunciado deve ter pelo menos 100 palavras, aponte "
                                      "qual das alternativas está correta, justificando as incorretas? Mostre uma alternativa por linha")
model = prompt | llm

st.set_page_config(page_title="Gerador de Questões")
st.header("Gerador de questões")

codigo_valido = os.getenv("CODIGO_ACESSO")
codigo = st.text_input("Informe o código de acesso", type="password")

if codigo == codigo_valido:
    st.success("Acesso autorizado ✅")

    # Mostra o campo de assunto e o botão somente se o código for válido
    entrada = st.text_input(label="Informe o assunto")
    btn = st.button(label="Enviar")

    if btn:
        with st.spinner("Gerando questão..."):
            res = model.invoke({'input': entrada})
            st.markdown(f"**Questão gerada:**\n\n{res}")
else:
    if codigo != "":
        st.error("Código inválido ❌")
