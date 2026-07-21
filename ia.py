import streamlit as st
import ollama

from prompts import PROMPT_SISTEMA


def montar_contexto(df):

    total = df["Custo total"].sum()

    media = df["Custo total"].mean()

    fornecedores = df["Fornecedor"].nunique()

    compras = len(df)

    top_fornecedores = (
        df.groupby("Fornecedor")["Custo total"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    top_produtos = (
        df.groupby("Item")["Custo total"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    contexto = f"""
RESUMO DAS COMPRAS

Valor Total:
R$ {total:,.2f}

Quantidade de Compras:
{compras}

Quantidade de Fornecedores:
{fornecedores}

Valor Médio:
R$ {media:,.2f}

TOP 10 FORNECEDORES

{top_fornecedores.to_string()}

TOP 10 PRODUTOS

{top_produtos.to_string()}
"""

    return contexto


def consultar_ollama(contexto, pergunta):

    resposta = ollama.chat(

        model="llama3.2:3b",

        messages=[

            {
                "role": "system",
                "content": PROMPT_SISTEMA
            },

            {
                "role": "user",
                "content": contexto + "\n\nPergunta:\n" + pergunta
            }

        ]

    )

    return resposta["message"]["content"]

def perguntar_ia(df):

    st.divider()

    st.header("🤖 Analista Inteligente de Compras")

    st.write(
        "Utilize os botões abaixo ou faça uma pergunta personalizada."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        resumo = st.button("📄 Resumo Executivo")

    with col2:
        economia = st.button("💰 Economia")

    with col3:
        fornecedores = st.button("🏭 Fornecedores")

    col4, col5 = st.columns(2)

    with col4:
        produtos = st.button("📦 Produtos")

    with col5:
        tendencias = st.button("📈 Tendências")

    st.divider()

    pergunta = st.text_area(
        "💬 Faça uma pergunta sobre as compras",
        placeholder="Ex.: Qual fornecedor teve maior gasto?"
    )

    prompt = None

    if resumo:
        prompt = """
Faça um resumo executivo das compras.

Utilize linguagem profissional.

Mostre:

- Valor total
- Número de fornecedores
- Número de compras
- Principais fornecedores
- Principais produtos
- Conclusão
"""

    elif economia:
        prompt = """
Analise os dados procurando oportunidades de economia.

Verifique:

- concentração de fornecedores
- produtos caros
- oportunidades de negociação
- recomendações
"""

    elif fornecedores:
        prompt = """
Faça uma análise dos fornecedores.

Quem são os maiores?

Quem merece atenção?

Existe concentração de compras?
"""

    elif produtos:
        prompt = """
Analise os produtos.

Quais possuem maior impacto financeiro?

Quais deveriam ser renegociados?
"""

    elif tendencias:
        prompt = """
Analise tendências dos dados.

Existe algum comportamento interessante?

Existe algum alerta?
"""

    elif pergunta.strip():

        prompt = pergunta

    if prompt:

        contexto = montar_contexto(df)

        with st.spinner("🧠 IA analisando..."):

            try:

                resposta = consultar_ollama(
                    contexto,
                    prompt
                )

                st.success("✅ Análise concluída")

                st.markdown(resposta)

            except Exception as erro:

                st.error(f"Erro ao consultar a IA: {erro}")