import streamlit as st
import pandas as pd


def aplicar_filtros(df):

    filtro = df.copy()

    st.sidebar.header("🔎 Filtros")

    # =====================================================
    # GARANTE TIPOS
    # =====================================================

    filtro["Fornecedor"] = filtro["Fornecedor"].fillna(
        "Fornecedor não informado"
    ).astype(str)

    filtro["Item"] = filtro["Item"].fillna("").astype(str)

    filtro["Data"] = pd.to_datetime(
        filtro["Data"],
        errors="coerce"
    )

    # =====================================================
    # FORNECEDOR
    # =====================================================

    fornecedores = sorted(
        filtro["Fornecedor"].unique().tolist()
    )

    fornecedor = st.sidebar.selectbox(
        "🏭 Fornecedor",
        ["Todos"] + fornecedores
    )

    # =====================================================
    # ITEM
    # =====================================================

    item = st.sidebar.text_input(
        "📦 Pesquisar Item"
    )

    # =====================================================
    # DATAS
    # =====================================================

    data_min = filtro["Data"].min()
    data_max = filtro["Data"].max()

    if pd.isna(data_min) or pd.isna(data_max):

        data_inicio = None
        data_fim = None

    else:

        data_inicio = st.sidebar.date_input(
            "📅 Data Inicial",
            value=data_min.date(),
            format="DD/MM/YYYY"
        )

        data_fim = st.sidebar.date_input(
            "📅 Data Final",
            value=data_max.date(),
            format="DD/MM/YYYY"
        )

    # =====================================================
    # APLICA FILTROS
    # =====================================================

    if fornecedor != "Todos":

        filtro = filtro[
            filtro["Fornecedor"] == fornecedor
        ]

    if item:

        filtro = filtro[
            filtro["Item"].str.contains(
                item,
                case=False,
                na=False
            )
        ]

    if data_inicio and data_fim:

        inicio = pd.to_datetime(data_inicio)

        fim = (
            pd.to_datetime(data_fim)
            + pd.Timedelta(days=1)
            - pd.Timedelta(seconds=1)
        )

        filtro = filtro[
            (filtro["Data"] >= inicio)
            &
            (filtro["Data"] <= fim)
        ]

    filtro = filtro.reset_index(drop=True)

    return filtro