import streamlit as st
import pandas as pd
from utils import formatar_moeda

def mostrar_resumo(df):

    st.divider()

    st.header("📑 Resumo Executivo")

    total = df["Custo total"].sum()

    quantidade = len(df)

    fornecedores = df["Fornecedor"].nunique()

    produtos = df["Item"].nunique()

    maior_fornecedor = (
        df.groupby("Fornecedor")["Custo total"]
        .sum()
        .sort_values(ascending=False)
    )

    nome_fornecedor = maior_fornecedor.index[0]
    valor_fornecedor = maior_fornecedor.iloc[0]

    maior_produto = (
        df.groupby("Item")["Custo total"]
        .sum()
        .sort_values(ascending=False)
    )

    nome_produto = maior_produto.index[0]
    valor_produto = maior_produto.iloc[0]

    participacao = valor_fornecedor / total * 100

    economia = valor_fornecedor * 0.05

    st.success(f"""

### 🤖 Análise Inteligente

Durante o período analisado foram realizadas **{quantidade} compras**.

Foram adquiridos **{produtos} produtos diferentes** junto a **{fornecedores} fornecedores**.

O valor total comprado foi de

# 💰 {formatar_moeda(total)}

O fornecedor com maior participação foi **{nome_fornecedor}**, representando **{participacao:.1f}%** do valor comprado.

O produto de maior impacto financeiro foi **{nome_produto}**.

Caso seja possível negociar apenas **5%** com o principal fornecedor, a economia estimada será de

# 💵 {formatar_moeda(economia)}

""")

    st.info("""

### 📌 Recomendações da IA

✅ Revisar os produtos Classe A da Curva ABC.

✅ Negociar os três maiores fornecedores.

✅ Avaliar itens com maior impacto financeiro.

✅ Comparar os custos com períodos anteriores.

✅ Monitorar tendências de consumo.

""")