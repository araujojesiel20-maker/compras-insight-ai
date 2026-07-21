import streamlit as st

from utils import (
    formatar_numero,
    formatar_moeda
)


def mostrar_comparativo(compras, consumo, estoque):

    st.divider()
    st.header("📊 Comparativo Compras x Consumo")

    # ==================================================
    # AGRUPA COMPRAS
    # ==================================================

    compra = (
        compras.groupby("Item_Normalizado")
        .agg({
            "Item": "first",
            "Quantidade": "sum",
            "Custo total": "sum"
        })
        .reset_index()
        .rename(columns={
            "Quantidade": "Quantidade_Comprada"
        })
    )

    # ==================================================
    # AGRUPA CONSUMO
    # ==================================================

    consumo = consumo.copy()

    consumo["Item_Final"] = consumo["Item_Correspondente"].fillna(
        consumo["Item_Normalizado"]
    )

    consumo_agrupado = (
        consumo.groupby("Item_Final")
        .agg({
            "Quantidade": "sum"
        })
        .reset_index()
        .rename(columns={
            "Item_Final": "Item_Normalizado",
            "Quantidade": "Quantidade_Consumida"
        })
    )

    # ==================================================
    # AGRUPA ESTOQUE
    # ==================================================

    estoque = (
        estoque.groupby("Item_Correspondente")
        .agg({
            "Em estoque": "sum",
            "Estoque mínimo": "sum",
            "Estoque desejável": "sum",
            "Unidade": "first"
        })
        .reset_index()
        .rename(columns={
            "Item_Correspondente": "Item_Normalizado"
        })
    )

    # ==================================================
    # COMPARATIVO
    # ==================================================

    comparativo = compra.merge(
        consumo_agrupado,
        on="Item_Normalizado",
        how="outer"
    )

    comparativo = comparativo.merge(
        estoque,
        on="Item_Normalizado",
        how="left"
    )

    comparativo["Item"] = comparativo["Item"].fillna(
        comparativo["Item_Normalizado"]
    )

    colunas = [
        "Quantidade_Comprada",
        "Quantidade_Consumida",
        "Custo total",
        "Em estoque",
        "Estoque mínimo",
        "Estoque desejável"
    ]

    for coluna in colunas:
        comparativo[coluna] = comparativo[coluna].fillna(0)

    comparativo["Unidade"] = comparativo["Unidade"].fillna("")

    comparativo["Saldo"] = (
        comparativo["Quantidade_Comprada"]
        - comparativo["Quantidade_Consumida"]
    )

    # ==================================================
    # LÓGICA DE COMPRA
    # ==================================================

    comparativo["Comprar"] = (
    comparativo["Em estoque"] * 0
).astype(float)

    mascara = (
        comparativo["Em estoque"]
        <= comparativo["Estoque mínimo"]
    )

    comparativo.loc[
        mascara,
        "Comprar"
    ] = (
        comparativo["Estoque desejável"]
        - comparativo["Em estoque"]
    )

    comparativo["Comprar"] = comparativo["Comprar"].clip(lower=0)

    # ==================================================
    # MOTIVO
    # ==================================================

    comparativo["Motivo"] = "Estoque adequado"

    comparativo.loc[
        comparativo["Em estoque"] == 0,
        "Motivo"
    ] = "Estoque zerado"

    comparativo.loc[
        (
            comparativo["Em estoque"] > 0
        ) &
        (
            comparativo["Em estoque"]
            <= comparativo["Estoque mínimo"]
        ),
        "Motivo"
    ] = "Abaixo do estoque mínimo"

    comparativo = comparativo.sort_values(
        "Item"
    ).reset_index(drop=True)

    # ==================================================
    # KPIs
    # ==================================================

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "📦 Comprado",
            formatar_numero(
                comparativo["Quantidade_Comprada"].sum()
            )
        )

    with c2:
        st.metric(
            "📉 Consumido",
            formatar_numero(
                comparativo["Quantidade_Consumida"].sum()
            )
        )

    with c3:
        st.metric(
            "📦 Comprar",
            formatar_numero(
                comparativo["Comprar"].sum()
            )
        )

    with c4:
        st.metric(
            "💰 Valor Comprado",
            formatar_moeda(
                comparativo["Custo total"].sum()
            )
        )

    st.subheader("📋 Comparativo por Produto")

    tabela = comparativo.copy()

    tabela["Quantidade_Comprada"] = tabela[
        "Quantidade_Comprada"
    ].map(formatar_numero)

    tabela["Quantidade_Consumida"] = tabela[
        "Quantidade_Consumida"
    ].map(formatar_numero)

    tabela["Saldo"] = tabela[
        "Saldo"
    ].map(formatar_numero)

    tabela["Comprar"] = tabela.apply(
        lambda x: f"{formatar_numero(x['Comprar'])} {x['Unidade']}",
        axis=1
    )

    tabela["Em estoque"] = tabela.apply(
        lambda x: f"{formatar_numero(x['Em estoque'])} {x['Unidade']}",
        axis=1
    )

    tabela["Estoque mínimo"] = tabela.apply(
        lambda x: f"{formatar_numero(x['Estoque mínimo'])} {x['Unidade']}",
        axis=1
    )

    tabela["Estoque desejável"] = tabela.apply(
        lambda x: f"{formatar_numero(x['Estoque desejável'])} {x['Unidade']}",
        axis=1
    )

    tabela["Custo total"] = tabela["Custo total"].map(
        formatar_moeda
    )

    tabela = tabela[
        [
            "Item",
            "Em estoque",
            "Estoque mínimo",
            "Estoque desejável",
            "Comprar",
            "Motivo",
            "Quantidade_Comprada",
            "Quantidade_Consumida",
            "Saldo",
            "Custo total"
        ]
    ]

    st.dataframe(
        tabela,
        use_container_width=True,
        hide_index=True
    )

    return comparativo