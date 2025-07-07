import streamlit as st
st.set_page_config(page_title="Gerador de Questões Múltipla Escolha")

st.header("Gerador de Questões Múltipla Escolha", divider=True)
st.write(""" O Gerador de Questões Múltiplas faz parte da pesquisa de mestrado de Valmir Ribeiro de Assis, 
         no Programa de Pós-graduação em Computação Aplicada, da Universidade do Estado de Santa Catarina, 
         intitulado "AiForTeachers: Plataforma para criação de Recursos Educacionais abertos (REA) baseados em 
         Inteligência Artificial Generativa para Professores do Ensino Superior", vinculado ao projeto de pesquisa 
         "Metodologias ativas e aprendizagem colaborativa na educação formal e informal com suporte das tecnologias
         de informação e comunicação" sob orientação da Professora Avanilde Kemczinski, Dra. e com parecer
         consubstanciado do Comitê de Ética em Pesquisas Envolvendo Seres Humanos CAAE: 66987023.5.0000.0118.
         Esta pesquisa tem como objetivo analisar as percepções dos professores do Ensino Superior sobre a utilização 
         da ferramenta para geração de questões múltipla escolha com o uso GenIA.""")
st.write(""" A ferramenta foi desenvolvida durante a disciplina de Sistemas Inteligentes (2025/1) ministrada pelo Professor
         Rafael Stubs Parpinelli.
         """)

st.write("")
st.write()
st.warning(" 🚨 **Antes de gerar as questões, leia as informações no menu lateral.**")

st.success(" ✅ **Após gerar as questões, não esqueça de responder o formulário na página Avaliar.**")
st.divider()
