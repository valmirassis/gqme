from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import streamlit as st

load_dotenv()
llm = GoogleGenerativeAI(model="models/gemini-1.5-pro-latest")
prompt = PromptTemplate.from_template("Atue como um professor de Ensino Superior e crie uma pergunta de múltipla escolha de 5 alternativas com a estrutura "
                                      "analise as afirmativas abaixo coloque 4 afirmativas com números romanos (não é necessário expressar isso no enunciado) "
                                      "e depois assinale quais estão corretas  sobre o tema {input}, o enunciado deve ter pelo menos 100 palavras, aponte "
                                      "qual das alternativas está correta, justificando as incorretas?")
model = prompt | llm

st.set_page_config(page_title="Gerador de Questões")
st.header("Gerador de questões")

entrada=st.text_input(label="Informe o assunto")
btn = st.button(label="Enviar")
if (btn):
    res = model.invoke({'input': entrada})
    st.write(res)
