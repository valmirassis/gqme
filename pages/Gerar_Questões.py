from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, GoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import streamlit as st
from dotenv import load_dotenv
import os
import tempfile
import numpy as np
import time
load_dotenv()
llm = GoogleGenerativeAI(model="models/gemini-1.5-pro-latest", temperature=0.8)

embedding_model = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-exp-03-07")

st.set_page_config(page_title="Gerador de Questões Múltipla Escolha")

st.header("Gerador de Questões Múltipla Escolha", divider=True)



codigo_valido = os.getenv("CODIGO_ACESSO")
codigo = st.text_input("Informe o código de acesso", type="password")

if codigo == codigo_valido:
    st.success("Acesso autorizado ✅")
    tipo_base = st.radio("Como deseja gerar a questão?", ["Baseado em tema", "Baseado em arquivo"])
    if tipo_base == "Baseado em tema":
        # Mostra o form somente se o código for válido

        texto_base = st.text_input(label="Informe o tema da pergunta")
        opcoes = {
            "Múltipla escolha simples": "A",
            "Múltipla escolha com afirmativas": "B",
            "Múltipla escolha asserção Razão": "C"}
        rotulos = list(opcoes.keys())
        escolha = st.radio("Escolha o tipo de questao:", rotulos)
        tipo_questao = opcoes[escolha]
        qtd_questoes = st.number_input("Quantas questões deseja gerar?", min_value=1, max_value=3, value=1, step=1)
        btn = st.button(label="Gerar questão")

        if btn:
            with st.spinner("Gerando questão..."):
                if tipo_questao == "A":
                    prompt = PromptTemplate.from_template(
                        """Você é um professor de Ensino Superior e precisa elaborar {quantidade} questão(ões) 
                         de múltipla escolha
                        Com de 5 alternativas usando a estrutura
                        **Questão X**
                        Enunciado (pelo menos 40 palavras)
                        Sobre o exposto acima assinale a alternativa CORRETA:\n
                        a) [Elabore a primeira alternativa.]\n
                        b) [Elabore a segunda alternativa.]\n
                        c) [Elabore a terceira alternativa.]\n
                        d) [Elabore a quarta alternativa.]\n
                        e) [Elabore a quinta alternativa.]\n
                        Aponte qual das alternativas está correta, justificando as incorretas.
                        Verifique se a resposta da questão não se encontra no enunciado da questão.
                        O tema da questão é: {input}"""
                    )

                elif tipo_questao == "B":
                    prompt = PromptTemplate.from_template(
                        """Você é um professor de Ensino Superior e precisa elaborar {quantidade} questão(ões) 
                        Com de 5 alternativas usando a estrutura
                        **Questão X**
                        Enunciado (pelo menos 40 palavras)
                        Sobre o exposto acima análise as afirmativas a seguir: \n
                        I. [Elabore a primeira afirmativa.]\n
                        II. [Elabore a segunda afirmativa.]\n
                        III. [Elabore a terceira afirmativa.]\n
                        IV. [Elabore a quarta afirmativa.]\n

                        Assinale a alternativa que apresenta todas as afirmativas corretas. \n

                        a) [Elabore a primeira alternativa.]\n
                        b) [Elabore a segunda alternativa.]\n
                        c) [Elabore a terceira alternativa.]\n
                        d) [Elabore a quarta alternativa.]\n
                        e) [Elabore a quinta alternativa.]\n
                        Aponte qual das alternativas está correta, justificando as incorretas.
                        Verifique se a resposta da questão não se encontra no enunciado da questão.
                        O tema da questão é:  {input}"""
                    )

                elif tipo_questao == "C":
                    prompt = PromptTemplate.from_template(
                        """Você é um professor de Ensino Superior e precisa elaborar {quantidade} questão(ões) 
                        do tipo asserção razão
                        com 5 alternativas use a estrutura:
                        **Questão X**
                        Enunciado (pelo menos 40 palavras)
                        Considerando as informações acima, avalie as asserções a seguir e a relação proposta entre elas
                        I. asserção \n
                        PORQUE \n
                        II. razão \n
                        A respeito dessas asserções, assinale a opção correta. \n
                        a) As asserções I e II são proposições verdadeiras, e a II é uma justificativa correta da I.\n
                        b) As asserções I e II são proposições verdadeiras, mas a II não é uma justificativa correta da I.\n
                        c) A asserção I é uma proposição verdadeira, e a II é uma proposição falsa.\n
                        d) A asserção I é uma proposição falsa, e a II é uma proposição verdadeira.\n
                        e) As asserções I e II são proposições falsas.               
                        Aponte qual das alternativas está correta, justificando as incorretas.
                        Verifique se a resposta da questão não se encontra no enunciado da questão.
                        O tema da questão deve ser: {input}""")
                chain = LLMChain(llm=llm, prompt=prompt)
                res = chain.run(input=texto_base, quantidade=qtd_questoes)
                st.markdown(f"**Questão gerada:**\n\n{res}")

    elif tipo_base == "Baseado em arquivo":
        if "vezes_gerado" not in st.session_state:
            st.session_state["vezes_gerado"] = 0
        arquivo = st.file_uploader("Envie um arquivo em PDF", type=["pdf"])
        opcoes = {
            "Múltipla escolha simples": "A",
            "Múltipla escolha com afirmativas": "B",
            "Múltipla escolha asserção Razão": "C"}
        rotulos = list(opcoes.keys())
        escolha = st.radio("Escolha o tipo de questao:", rotulos)
        tipo_questao = opcoes[escolha]
        qtd_questoes = st.number_input("Quantas questões deseja gerar (funciona melhor com 1)?", min_value=1, max_value=3, value=1, step=1)
        consulta = st.text_input("Sobre o que a questão deve tratar? (Deixe em branco para o LLM escolher)",
                                 placeholder="Ex: Conceitos principais do texto, ou um tema dentro do arquivo "
                                 )
        btn_file = st.button("Gerar questão")
        if btn_file and arquivo:
            st.session_state["vezes_gerado"] += 1

            if st.session_state["vezes_gerado"] > 1:
                instrucao_extra = " Gere uma nova versão da questão, que seja diferente da anterior, mas baseada no mesmo conteúdo."
            else:
                instrucao_extra = ""
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

                texts = [doc.page_content for doc in chunks]

                ### Seção de debug
                # mostrar número de chunks
                # st.write(f"Total de chunks gerados: {len(chunks)}")
                # total_caracteres = sum(len(chunk.page_content) for chunk in chunks)
                # st.write(f"Total de caracteres nos chunks: {total_caracteres}")
                # for i, chunk in enumerate(chunks[:10]):
                #    st.markdown(f"**Chunk {i + 1}:**")
                #    st.text(chunk.page_content)

                # campo tema vazio
                if not consulta.strip():
                    # Define o limite máximo de chunks que será enviado
                    limite_chunks = 20

                    # Verifica se o número de chunks é menor ou igual ao limite
                    if len(chunks) <= limite_chunks:
                        chunks_selecionados = chunks
                    else:
                        chunks_selecionados = chunks[:limite_chunks]

                    # Junta os textos dos chunks selecionados
                    texto_base = "\n".join(chunk.page_content for chunk in chunks_selecionados)
                else:
                    # Embedding da consulta
                    embedding_consulta = embedding_model.embed_query(consulta)

                    # Embeddings dos chunks
                    embeddings_chunks = embedding_model.embed_documents(texts)


                    def similaridade(v1, v2):
                        return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


                    similaridades = [
                        (similaridade(embedding_consulta, emb), chunk)
                        for emb, chunk in zip(embeddings_chunks, chunks)
                    ]

                    # Seleciona os 5 chunks mais relevantes
                    chunks_relevantes = [chunk for _, chunk in
                                         sorted(similaridades, key=lambda x: x[0], reverse=True)[:5]]
                    texto_base = "\n".join(chunk.page_content for chunk in chunks_relevantes)
                # Gera embeddings dos textos (apenas conteúdo, não metadata)

                # define o prompt baseado no tipo de questão
                if tipo_questao == "A":
                    prompt = PromptTemplate.from_template(
                        """
                     Você é um professor de Ensino Superior e precisa elaborar {quantidade} questão(ões)
                      questão de múltipla escolha para avaliação.
                     
                     Siga o seguinte raciocínio passo a passo:

                     1. Analise o conteúdo fornecido abaixo e identifique os conceitos mais relevantes.
                     2. Escolha um conceito central que possa ser avaliado com uma pergunta objetiva.
                     3. Elabore um enunciado claro, contextualizado, com pelo menos 50 palavras, baseado nesse conceito.
                     4. Verifique se a **resposta correta não está explícita no enunciado**.
                     5. Crie 5 alternativas (a–e), sendo apenas uma correta.
                     6. Indique qual alternativa é a correta.
                     7. Justifique por que a alternativa correta está certa.
                     8. Justifique por que as demais alternativas estão incorretas.

                     Evite copiar diretamente o conteúdo original. Não mencione nomes de documentos ou fontes no enunciado.
                     {inst_extra}
                     Conteúdo de base:
                     {input}

                     Apresente a questão no seguinte formato (cada alternativa deve estar em uma linha separada):
                     **Questão X**
                     **Enunciado:** ...
                     \nSobre o exposto acima assinale a alternativa CORRETA: \n
                     a) [Elabore a primeira alternativa.]\n
                     b) [Elabore a segunda alternativa.]\n
                     c) [Elabore a terceira alternativa.]\n
                     d) [Elabore a quarta alternativa.]\n
                     e) [Elabore a quinta alternativa.]\n
                     **Alternativa correta:** ...
                     **Justificativa (raciocínio passo a passo):**
                     - ...
                     """
                    )

                elif tipo_questao == "B":
                    prompt = PromptTemplate.from_template(
                         """
                        Você é um professor de Ensino Superior e precisa elaborar {quantidade} questão(ões) 
                        de múltipla escolha com afirmativas.
                        
                        Siga o seguinte raciocínio passo a passo:
                        
                        1. Analise o conteúdo fornecido e identifique 4 ideias ou conceitos distintos que podem ser transformados em afirmativas.
                        2. Elabore um enunciado claro e contextualizado com pelo menos 50 palavras.
                        3. Escreva 4 afirmativas numeradas de I a IV.
                        4. Elabore 5 alternativas (a–e), com diferentes combinações de afirmativas corretas.
                        5. Verifique se **as afirmativas não indicam claramente qual alternativa é correta apenas pela redação**.
                        6. Indique qual alternativa é a correta.
                        7. Justifique por que a alternativa correta está certa.
                        8. Justifique por que as demais alternativas estão incorretas.
                        
                        Evite copiar diretamente o conteúdo original. Não mencione o nome do documento.
                        {inst_extra}
                        Conteúdo de base:
                        {input}
                        
                        Apresente a questão no seguinte formato (cada alternativa deve estar em uma linha separada):
                        **Questão X**
                        **Enunciado:** ...
                        I. ... \n
                        II. ... \n
                        III. ... \n
                        IV. ... \n
                        
                        Assinale a alternativa que apresenta todas as afirmativas corretas.\n
                        a) [Elabore a primeira alternativa.]\n
                        b) [Elabore a segunda alternativa.]\n
                        c) [Elabore a terceira alternativa.]\n
                        d) [Elabore a quarta alternativa.]\n
                        e) [Elabore a quinta alternativa.]\n
                        **Alternativa correta:** ...
                        **Justificativa (raciocínio passo a passo):**
                        - ...
                        """
                        )

                elif tipo_questao == "C":
                    prompt = PromptTemplate.from_template(
                        """
                        Você é um professor de Ensino Superior e precisa elaborar {quantidade} questão(ões) 
                        do tipo múltipla escolha com estrutura de asserção e razão.
                        
                        Siga o seguinte raciocínio passo a passo:
                        
                        1. Analise o conteúdo fornecido e selecione um conceito principal.
                        2. Elabore um enunciado introdutório (contexto) com pelo menos 50 palavras.
                        3. Crie uma **asserção (I)** e uma **razão (II)** relacionadas ao conceito.
                        4. Elabore 5 alternativas (a–e) sobre a veracidade das asserções e se a razão justifica a asserção.
                        5. Verifique se **o enunciado não antecipa a resposta correta nem contém pistas óbvias**.
                        6. Indique qual alternativa é a correta.
                        7. Justifique por que a alternativa correta está certa.
                        8. Justifique por que as demais alternativas estão incorretas.
                        
                        Evite copiar diretamente o conteúdo original. Não mencione o nome do documento.
                        
                        {inst_extra}
                        Conteúdo de base:
                        {input}
                        
                        Apresente a questão no seguinte formato (cada alternativa deve estar em uma linha separada):
                        **Questão X**
                        **Enunciado:** ...
                        Considerando as informações, avalie as asserções a seguir e a relação proposta entre elas.
                        I. ... \n
                        PORQUE  \n
                        II. ... \n
                        A respeito dessas asserções, assinale a opção CORRETA. \n
                        a) As asserções I e II são proposições verdadeiras, e a II é uma justificativa correta da I.\n
                        b) As asserções I e II são proposições verdadeiras, mas a II não é uma justificativa correta da I.\n
                        c) A asserção I é uma proposição verdadeira, e a II é uma proposição falsa.\n
                        d) A asserção I é uma proposição falsa, e a II é uma proposição verdadeira.\n
                        e) As asserções I e II são proposições falsas.
                        **Alternativa correta:** ...
                        **Justificativa (raciocínio passo a passo):**
                        - ...
                        """)
                chain = LLMChain(llm=llm, prompt=prompt)
                res = chain.run(input=texto_base,  quantidade=qtd_questoes, inst_extra=instrucao_extra)
                st.markdown(f"**Questão gerada:**\n\n{res}")
        elif btn_file and not arquivo:
            st.warning("Você precisa enviar um arquivo antes de gerar a questão.")

else:
    if codigo != "":
        st.error("Código inválido ❌")
