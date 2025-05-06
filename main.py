from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, GoogleGenerativeAI
from langchain.prompts import PromptTemplate
import streamlit as st
from dotenv import load_dotenv
import os
import tempfile

load_dotenv()
llm = GoogleGenerativeAI(model="models/gemini-1.5-pro-latest")

embedding_model = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-exp-03-07")

st.set_page_config(page_title="Gerador de Questões")
st.header("Gerador de questões")

codigo_valido = os.getenv("CODIGO_ACESSO")
codigo = st.text_input("Informe o código de acesso", type="password")

if codigo == codigo_valido:
    st.success("Acesso autorizado ✅")
    tipo_base = st.radio("Como deseja gerar a questão?", ["Baseado em tema", "Baseado em arquivo"])
    if tipo_base == "Baseado em tema":
        # Mostra o form somente se o código for válido

        assunto = st.text_input(label="Informe o tema da pergunta")
        opcoes = {
            "Múltipla escolha simples": "A",
            "Múltipla escolha com afirmativas": "B",
            "Múltipla escolha asserção Razão": "C"}
        rotulos = list(opcoes.keys())
        escolha = st.radio("Escolha o tipo de questao:", rotulos)
        tipo_questao = opcoes[escolha]

        btn = st.button(label="Gerar questão")

        if btn:
            with st.spinner("Gerando questão..."):
                if tipo_questao == "A":
                    prompt = PromptTemplate.from_template(
                        """Atue como um professor de Ensino Superior e crie uma pergunta de múltipla escolha
                        Com de 5 alternativas usando a estrutura
                        Enunciado (pelo menos 50 palavras)
                        Sobre o exposto acima assinale a alternativa CORRETA:
                        a) [Elabore a primeira alternativa.]
                        b) [Elabore a segunda alternativa.]
                        c) [Elabore a terceira alternativa.]
                        d) [Elabore a quarta alternativa.]
                        e) [Elabore a quinta alternativa.]
                        aponte qual das alternativas está correta, justificando as incorretas
                        O tema da questão é: {input}"""
                       )

                elif tipo_questao == "B":
                    prompt = PromptTemplate.from_template(
                        """Atue como um professor de Ensino Superior e crie uma pergunta de múltipla escolha"
                        Com de 5 alternativas usando a estrutura
                        Enunciado (pelo menos 50 palavras)
                        Sobre o exposto acima análise as afirmativas a seguir:
                        I. [Elabore a primeira afirmativa.]\n
                        II. [Elabore a segunda afirmativa.]\n
                        III. [Elabore a terceira afirmativa.]\n
                        IV. [Elabore a quarta afirmativa.]\n
                        
                        Assinale a alternativa que apresenta todas as afirmativas corretas.
                        
                        a) [Elabore a primeira alternativa.]\n
                        b) [Elabore a segunda alternativa.]\n
                        c) [Elabore a terceira alternativa.]\n
                        d) [Elabore a quarta alternativa.]\n
                        e) [Elabore a quinta alternativa.]\n
                        
                        Aponte qual das alternativas está correta, justificando as incorretas
                        O tema da questão é:  {input}"""
                    )

                elif tipo_questao == "C":
                    prompt = PromptTemplate.from_template(
                        """Atue como um professor de Ensino Superior e crie uma pergunta de múltipla escolha to tipo asserção razão
                        com 5 alternativas use a estrutura:
                        Contexto (pelo menos 50 palavras)
                        Considerando as informações acima, avalie as asserções a seguir e a relação proposta entre elas"
                        I. asserção
                        PORQUE
                        II. razão
                        A respeito dessas asserções, assinale a opção correta.
                        a) As asserções I e II são proposições verdadeiras, e a II é uma justificativa correta da I.\n
                        b) As asserções I e II são proposições verdadeiras, mas a II não é uma justificativa correta da I.\n
                        c) A asserção I é uma proposição verdadeira, e a II é uma proposição falsa.\n
                        d) A asserção I é uma proposição falsa, e a II é uma proposição verdadeira.\n
                        e) As asserções I e II são proposições falsas.               
                        Aponte qual das alternativas está correta, justificando as incorretas
                        O tema da questão deve ser: {input}""")

                model = prompt | llm

                res = model.invoke({'input': assunto})
                st.markdown(f"**Questão gerada:**\n\n{res}")
    elif tipo_base == "Baseado em arquivo":
        arquivo = st.file_uploader("Envie um arquivo de texto ou PDF", type=["pdf"])
        opcoes = {
            "Múltipla escolha simples": "A",
            "Múltipla escolha com afirmativas": "B",
            "Múltipla escolha asserção Razão": "C"}
        rotulos = list(opcoes.keys())
        escolha = st.radio("Escolha o tipo de questao:", rotulos)
        tipo_questao = opcoes[escolha]

        btn_file = st.button("Gerar questão")
        if btn_file and arquivo:
            with st.spinner("Lendo e processando o arquivo..."):
                # Salva o arquivo temporariamente
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(arquivo.read())
                    caminho_temporario = tmp_file.name

                # Usa o loader da LangChain
                loader = PyPDFLoader(caminho_temporario)
                documentos = loader.load()

                # Chunk de 1000 caracteres mantendo 100 caracteres entre cada chunk para não perder contexot
                splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=100)
                # divide o documento conforme o chunck
                chunks = splitter.split_documents(documentos)
                chunks = [chunk for chunk in chunks if len(chunk.page_content) > 300]


                ### Seção de debug
                # mostrar número de chunks
                # st.write(f"Total de chunks gerados: {len(chunks)}")
                # total_caracteres = sum(len(chunk.page_content) for chunk in chunks)
                # st.write(f"Total de caracteres nos chunks: {total_caracteres}")
                # for i, chunk in enumerate(chunks[:10]):
                #    st.markdown(f"**Chunk {i + 1}:**")
                #    st.text(chunk.page_content)




                # Gera embeddings dos textos (apenas conteúdo, não metadata)
                texts = [doc.page_content for doc in chunks]
                _ = embedding_model.embed_documents(texts)  # Só para demonstrar que funciona
                # define o prompt baseado no tipo de questão
                if tipo_questao == "A":
                    prompt = PromptTemplate.from_template(
                        """Atue como um professor de Ensino Superior e crie uma pergunta de múltipla escolha
                        Com de 5 alternativas usando a estrutura
                        Enunciado (pelo menos 50 palavras)
                        Sobre o exposto acima assinale a alternativa CORRETA:
                        a) [Elabore a primeira alternativa.]\n
                        b) [Elabore a segunda alternativa.]\n
                        c) [Elabore a terceira alternativa.]\n
                        d) [Elabore a quarta alternativa.]\n
                        e) [Elabore a quinta alternativa.]\n
                        aponte qual das alternativas está correta, justificando as incorretas
                        Não referencie ou mencione o nome do documento no enunciado.
                        Gere uma questão com base neste conteúdo: {input}"""
                    )

                elif tipo_questao == "B":
                    prompt = PromptTemplate.from_template(
                        """Atue como um professor de Ensino Superior e crie uma pergunta de múltipla escolha"
                        Com de 5 alternativas usando a estrutura
                        Enunciado (pelo menos 50 palavras)
                        Sobre o exposto acima análise as afirmativas a seguir:
                        I. [Elabore a primeira afirmativa.]\n
                        II. [Elabore a segunda afirmativa.]\n
                        III. [Elabore a terceira afirmativa.]\n
                        IV. [Elabore a quarta afirmativa.]\n

                        Assinale a alternativa que apresenta todas as afirmativas corretas.

                        a) [Elabore a primeira alternativa.]\n
                        b) [Elabore a segunda alternativa.]\n
                        c) [Elabore a terceira alternativa.]\n
                        d) [Elabore a quarta alternativa.]\n
                        e) [Elabore a quinta alternativa.]\n

                        Aponte qual das alternativas está correta, justificando as incorretas
                        Não referencie ou mencione o nome do documento no enunciado.
                        Gere uma questão com base neste conteúdo:  {input}"""
                    )

                elif tipo_questao == "C":
                    prompt = PromptTemplate.from_template(
                        """Atue como um professor de Ensino Superior e crie uma pergunta de múltipla escolha to tipo asserção razão
                        com 5 alternativas use a estrutura:
                        Enunciado (pelo menos 50 palavras)
                        Considerando as informações acima, avalie as asserções a seguir e a relação proposta entre elas"
                        I. asserção
                        PORQUE
                        II. razão
                        A respeito dessas asserções, assinale a opção correta.
                        a) As asserções I e II são proposições verdadeiras, e a II é uma justificativa correta da I.\n
                        b) As asserções I e II são proposições verdadeiras, mas a II não é uma justificativa correta da I.\n
                        c) A asserção I é uma proposição verdadeira, e a II é uma proposição falsa.\n
                        d) A asserção I é uma proposição falsa, e a II é uma proposição verdadeira.\n
                        e) As asserções I e II são proposições falsas.               
                        Aponte qual das alternativas está correta, justificando as incorretas
                        Não referencie ou mencione o nome do documento no enunciado. 
                        Gere uma questão com base neste conteúdo: {input}""")
                model = prompt | llm
                texto_base = "\n".join(chunk.page_content for chunk in chunks[:10])

                res = model.invoke({'input': texto_base})
                st.markdown(f"**Questão gerada:**\n\n{res}")
        elif btn_file and not arquivo:
            st.warning("Você precisa enviar um arquivo antes de gerar a questão.")
else:
    if codigo != "":
        st.error("Código inválido ❌")
