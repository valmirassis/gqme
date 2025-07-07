import streamlit as st
st.set_page_config(page_title="Gerador de Questões Múltipla Escolha", layout="wide")

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
st.markdown("## 🎯 Diferencial da ferramente em relação ao uso direto em um LLM")

st.markdown("""Este sistema foi desenvolvido para transformar um modelo de linguagem (LLM) genérico em uma 
ferramenta educacional específica e acessível para professores. """)

with st.expander(" 📚 Vantagens ", expanded=True):
    st.markdown("""
    - Interface simples e orientada para professores. 
    - Não é necessário ter conhecimento técnico de **engenharia de prompt**.
    - Campos guiados (tema, quantidade, tipo de questão) tornam o uso mais rápido.
    - Reduz a curva de aprendizado e o risco de comandos mal interpretados.
    - Garante consistência  na apresentação e estrutura das questões.
    - Permite gerar questões com base em **conteúdos reais** (apostilas, artigos, capítulos).
    - Utiliza embeddings e recuperação semântica para focar nos trechos mais relevantes.
    - Aplicação de níveis com base na Taxonomia de Bloom*.
    
    """)
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
st.markdown("## 📚 Histórico das questões geradas")
st.markdown("""
- As questões geradas não ficam salvas no sistema.
- A página histórico armazena as questões geradas pelo usuário durante a sessão.
- Caso feche o navegador ou abra o sistema em um nova de aba o histórico será reiniciado.

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

### ✅ Múltipla Escolha Asserção-Razão
- Enunciado com **pelo menos 40 palavras**.
- 1 **asserção** e 1 **razão**.
- 5 alternativas (**a–e**) sobre a relação entre as proposições.
- O sistema indicará a alternativa correta e justificará as incorretas.

### ✅ Número de questões
- É possível gerar 1, 2 ou 3 questões por solicitação, porém, na geração por arquivos recomenda-se a geração de apenas 1 questão.


### ✅ Nível de dificuldade
- Caso a opção **'Gerar questão com versões em nível de dificuldade fácil e difícil?'** seja marcada, 
será gerado duas versões para cada questão uma de nível fácil e outra de nível difícil.
- Os níveis e dificuldades são definidos a partir da **Taxonomia de Bloom**. 
- **Fácil** - níveis 1 (lembrança) ou 2 (compreensão).
- **Difícil** - níveis 3 (aplicação), 4 (análise) ou 5 (avaliação).
""")

st.divider()
st.markdown("""
A Taxonomia de Bloom, conforme discutida por Faraon, Granlund e Rönkkö (2023), é uma estrutura hierárquica que organiza
 os objetivos educacionais em diferentes níveis de complexidade cognitiva, sendo amplamente utilizada no planejamento 
 e avaliação da aprendizagem no ensino superior. Originalmente composta por categorias como conhecimento, compreensão 
 e aplicação, a taxonomia foi posteriormente revisada, substituindo os substantivos por verbos de ação e incorporando 
 a metacognição como elemento essencial para o desenvolvimento de habilidades cognitivas. Com a crescente presença da 
 tecnologia na educação, surgiu a taxonomia digital de Bloom, que mantém os mesmos seis níveis – lembrar, compreender, 
 aplicar, analisar, avaliar e criar – mas os adapta ao uso de ferramentas tecnológicas para promover o aprendizado. 
 Essa versão digital oferece orientações práticas para integrar recursos digitais ao ensino, ajudando educadores a 
 planejar atividades que estimulem tanto habilidades de ordem inferior quanto de ordem superior, com base no uso 
 crítico e criativo da tecnologia.\n
FARAON, M.; GRANLUD, V.; ROKKO, K. (2023) Artificial Intelligence Practices in Higher Education Using Bloom’s Digital 
Taxonomy. 2023 5th International Workshop on Artificial Intelligence and Education (WAIE). 
DOI: https://doi.org/10.1109/WAIE60568.2023.00017
"""

)