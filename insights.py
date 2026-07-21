import streamlit as st

from utils import (
    formatar_moeda,
    formatar_percentual
)


def mostrar_insights(df):

    st.divider()

    st.header("🤖 Inteligência Artificial")

    total = df["Custo total"].sum()

    quantidade_compras = len(df)

    produtos = df["Item"].nunique()

    fornecedores = df["Fornecedor"].nunique()

    fornecedor = (
        df.groupby("Fornecedor")["Custo total"]
        .sum()
        .sort_values(ascending=False)
    )

    produto = (
        df.groupby("Item")["Custo total"]
        .sum()
        .sort_values(ascending=False)
    )

    top_fornecedor = fornecedor.index[0]
    valor_top = fornecedor.iloc[0]

    top_produto = produto.index[0]
    valor_produto = produto.iloc[0]

    participacao = (valor_top / total) * 100

    economia = valor_top * 0.05

    st.success(f"""
## 📊 Resumo Geral

💰 **Valor comprado**

**{formatar_moeda(total)}**

📦 **Compras realizadas**

**{quantidade_compras}**

🏭 **Fornecedores**

**{fornecedores}**

📋 **Produtos**

**{produtos}**
""")

    col1, col2 = st.columns(2)

    with col1:

        st.info(f"""
### 🏭 Principal fornecedor

**{top_fornecedor}**

Valor comprado

**{formatar_moeda(valor_top)}**

Participação

**{formatar_percentual(participacao)}**
""")

        st.info(f"""
### 📦 Produto de maior investimento

**{top_produto}**

Valor

**{formatar_moeda(valor_produto)}**
""")

    with col2:

        st.warning(f"""
### 💵 Economia Potencial

Negociando apenas **5%**

com o principal fornecedor

economia estimada

# {formatar_moeda(economia)}
""")

        if participacao >= 40:

            st.error(f"""
### ⚠️ Alerta

O fornecedor **{top_fornecedor}**

representa

**{formatar_percentual(participacao)}**

das compras.

Considere buscar novos fornecedores.
""")

        else:

            st.success("""
### ✅ Situação

Não foi encontrada concentração elevada de compras.
""")

    st.divider()

    st.subheader("🎯 Recomendações da IA")

    st.markdown(f"""
- Negociar preços com **{top_fornecedor}**.

- Revisar o consumo de **{top_produto}**.

- Priorizar análise dos produtos da Curva ABC.

- Comparar compras e consumo mensalmente.

- Monitorar fornecedores com maior participação.

- A economia potencial estimada é de **{formatar_moeda(economia)}**.
""")