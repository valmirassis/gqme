import streamlit as st
st.set_page_config(page_title="Gerador de Questões Múltipla Escolha")

st.markdown("## 📌 Informações importantes")
st.warning(
    "**Professor**, ao usar este sistema, é essencial revisar cuidadosamente cada questão gerada, analisando o contexto "
    "e as informações apresentadas. A **IA Generativa é uma ferramenta auxiliar**,"
    " mas o conteúdo final é sua responsabilidade. Sempre supervisione o que será apresentado aos alunos."
)

st.divider()

st.markdown("## 💡 Sobre o sistema")
st.markdown("""
Este sistema utiliza o modelo de linguagem **Gemini** integrado via **LangChain**, com **Streamlit** para a interface 
e **Python** como linguagem de desenvolvimento.

O objetivo é auxiliar professores na **geração de questões de múltipla escolha** com diferentes estruturas,
 usando temas ou arquivos como base.
""")

st.divider()

st.markdown("## ⚙️ Como utilizar o gerador")

with st.expander("📂 Modo: Baseado em Tema", expanded=True):
    st.markdown("""
    - O modelo usará seu **conhecimento prévio** (base de dados de treinamento) para gerar a questão.
    - Informe um **tema objetivo**, como:
        - `"Sustentabilidade"`
        - `"Reforma tributária"`
        - `"Programação orientada a objetos"`
    - Clique em **Gerar questão** para obter o resultado.
    """)

with st.expander("📄 Modo: Baseado em Arquivo PDF", expanded=True):
    st.markdown("""
    - O modelo utilizará o conteúdo **presente no arquivo** para gerar a questão.
    -  Nesta opção ainda é possível informar um assunto presente no arquivo para que a questão seja gerada com base
         naquele assunto, por exemplo, um artigo sobre fundamentos dos sistemas de informação, e no artigo há um
         subtópico sobre a evolução dos sistemas de informações, assim, caso queira uma questão especificamente sobre
         esse tópico você deve informar isso no campo **'Sobre o que a questão deve tratar?'**
         

    :blue-background[**Importante:** O modelo pode gerar conteúdo irrelevante (alucinação) se o texto não fornecer base suficiente.]

    🔹 **Recomendação:** use arquivos entre **2 e 20 páginas**.  \n
    🔹 **Observação:** páginas com menos de **300 caracteres** são **descartadas pelo sistema**. \n
    🔹 O sistema lê apenas os textos presentes no arquivo, sem considerar o conteúdo gráfico.\n
    """)

st.divider()

st.markdown("## 🧠 Estruturas de questões suportadas")

st.markdown("""
### ✅ Múltipla Escolha Simples
- Enunciado com **pelo menos 40 palavras**.
- 5 alternativas (**a–e**) — apenas 1 correta.
- O sistema indicará a alternativa correta e justificará as incorretas.

### ✅ Múltipla Escolha com Afirmativas
- Enunciado com **pelo menos 40 palavras**.
- 4 afirmativas sobre o tema (I a IV).
- 5 alternativas de combinação (**a–e**) — apenas 1 correta.
- O sistema indicará a alternativa correta e justificará as incorretas.

### ✅ Múltipla Escolha Assserção-Razão
- Enunciado com **pelo menos 40 palavras**.
- 1 **asserção** e 1 **razão**.
- 5 alternativas (**a–e**) sobre a relação entre as proposições.
- O sistema indicará a alternativa correta e justificará as incorretas.

### ✅ Número de questões
- É possível gerar 1, 2 ou 3 questões por solicitação, porém, na geração por arquivos recomenda-se a geração de apenas 1 questão.
""")