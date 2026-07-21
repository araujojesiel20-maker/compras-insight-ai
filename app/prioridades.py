import streamlit as st

from utils import (
    formatar_numero,
    formatar_moeda
)


def mostrar_prioridades(comparativo, compras):

    st.divider()

    st.header("🧠 IA - Prioridades de Compra")

    if comparativo.empty:

        st.warning("Nenhum dado disponível para calcular prioridades.")

        return

    dados = comparativo.copy()

    # =====================================================
    # PREÇO MÉDIO
    # =====================================================

    chave = (
        "Item_Normalizado"
        if "Item_Normalizado" in compras.columns
        else "Item"
    )

    compras = compras.copy()

    compras["Preço Médio"] = (
        compras["Custo total"] /
        compras["Quantidade"].replace(0, 1)
    )

    preco = (
        compras.groupby(chave)["Preço Médio"]
        .mean()
    )

    if chave in dados.columns:

        dados["Preço Médio"] = dados[chave].map(preco)

    else:

        dados["Preço Médio"] = dados["Item"].map(preco)

    dados["Preço Médio"] = dados["Preço Médio"].fillna(0)

    # =====================================================
    # QUANTIDADE RECOMENDADA
    # =====================================================

    dados["Quantidade Recomendada"] = dados["Comprar"]

    dados["Valor Estimado"] = (

        dados["Quantidade Recomendada"]

        *

        dados["Preço Médio"]

    )

    # =====================================================
    # PRIORIDADE
    # =====================================================

    def prioridade(linha):

        if linha["Em estoque"] == 0:

            return "🔴 Alta"

        elif linha["Em estoque"] <= linha["Estoque mínimo"]:

            return "🟡 Média"

        return "🟢 Baixa"

    dados["Prioridade"] = dados.apply(
        prioridade,
        axis=1
    )

    ordem = {

        "🔴 Alta": 1,
        "🟡 Média": 2,
        "🟢 Baixa": 3

    }

    dados["Ordem"] = dados["Prioridade"].map(ordem)

    dados = dados.sort_values(

        ["Ordem", "Valor Estimado"],

        ascending=[True, False]

    )

    alta = dados[
        dados["Prioridade"] == "🔴 Alta"
    ]

    media = dados[
        dados["Prioridade"] == "🟡 Média"
    ]

    baixa = dados[
        dados["Prioridade"] == "🟢 Baixa"
    ]

    # =====================================================
    # CARDS
    # =====================================================

    c1, c2, c3 = st.columns(3)

    with c1:

        st.error(f"""

# 🔴 Alta

Produtos

**{len(alta)}**

""")

    with c2:

        st.warning(f"""

# 🟡 Média

Produtos

**{len(media)}**

""")

    with c3:

        st.success(f"""

# 🟢 Baixa

Produtos

**{len(baixa)}**

""")

    # =====================================================
    # TABELA
    # =====================================================

    st.subheader("📋 Produtos Priorizados")

    tabela = dados[
        [
            "Prioridade",
            "Item",
            "Em estoque",
            "Estoque mínimo",
            "Quantidade Recomendada",
            "Preço Médio",
            "Valor Estimado"
        ]
    ].copy()

    tabela["Em estoque"] = tabela[
        "Em estoque"
    ].apply(formatar_numero)

    tabela["Estoque mínimo"] = tabela[
        "Estoque mínimo"
    ].apply(formatar_numero)

    tabela["Quantidade Recomendada"] = tabela[
        "Quantidade Recomendada"
    ].apply(formatar_numero)

    tabela["Preço Médio"] = tabela[
        "Preço Médio"
    ].apply(formatar_moeda)

    tabela["Valor Estimado"] = tabela[
        "Valor Estimado"
    ].apply(formatar_moeda)

    st.dataframe(

        tabela,

        hide_index=True,

        use_container_width=True

    )

    # =====================================================
    # RESUMO
    # =====================================================

    urgentes = dados[
        dados["Prioridade"] != "🟢 Baixa"
    ]

    total = urgentes["Valor Estimado"].sum()

    quantidade = urgentes["Quantidade Recomendada"].sum()

    st.success(

        f"""

### 💰 Resumo das Compras Prioritárias

**Produtos prioritários:** {len(urgentes)}

**Quantidade recomendada:** {formatar_numero(quantidade)}

## Valor estimado: {formatar_moeda(total)}

"""

    )