import streamlit as st
import pandas as pd


def mostrar_pedido_compra(compras):

    st.subheader("🛒 Pedido de Compra")

    if compras.empty:
        st.warning("Nenhum item encontrado.")
        return

    # ==========================================
    # IDENTIFICAÇÃO DAS COLUNAS
    # ==========================================

    col_codigo = next(
        (c for c in compras.columns if "codigo" in c.lower() or "código" in c.lower()),
        None
    )

    col_item = next(
        (c for c in compras.columns if "item" in c.lower()),
        None
    )

    col_fornecedor = next(
        (c for c in compras.columns if "fornecedor" in c.lower()),
        None
    )

    col_qtd = next(
        (
            c for c in compras.columns
            if "quantidade" in c.lower()
            or "qtd" in c.lower()
        ),
        None
    )

    col_unidade = next(
        (
            c for c in compras.columns
            if "unidade" in c.lower()
            or "medida" in c.lower()
            or "un" == c.lower()
        ),
        None
    )

    col_valor = next(
        (
            c for c in compras.columns
            if "valor unit" in c.lower()
            or "preço unit" in c.lower()
            or "valor_unitario" in c.lower()
        ),
        None
    )

    # ==========================================
    # CRIA TABELA
    # ==========================================

    pedido = pd.DataFrame()

    pedido["Selecionar"] = False

    pedido["Código"] = (
        compras[col_codigo]
        if col_codigo
        else ""
    )

    pedido["Item"] = (
        compras[col_item]
        if col_item
        else ""
    )

    pedido["Fornecedor"] = (
        compras[col_fornecedor]
        if col_fornecedor
        else ""
    )

    pedido["Quantidade"] = (
        compras[col_qtd]
        if col_qtd
        else 0
    )

    pedido["Unidade"] = (
        compras[col_unidade]
        if col_unidade
        else ""
    )

    pedido["Valor Unitário"] = (
        compras[col_valor]
        if col_valor
        else 0.0
    )

    pedido["Valor Total"] = (
        pedido["Quantidade"]
        * pedido["Valor Unitário"]
    )

    # ==========================================
    # FILTROS
    # ==========================================

    st.markdown("### 🔎 Filtros")

    f1, f2, f3 = st.columns(3)

    with f1:

        fornecedor = st.selectbox(
            "Fornecedor",
            ["Todos"] + sorted(
                pedido["Fornecedor"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )
        )

    with f2:

        codigo = st.text_input("Código")

    with f3:

        item = st.text_input("Item")

    filtro = pedido.copy()

    if fornecedor != "Todos":

        filtro = filtro[
            filtro["Fornecedor"] == fornecedor
        ]

    if codigo:

        filtro = filtro[
            filtro["Código"]
            .astype(str)
            .str.contains(codigo, case=False)
        ]

    if item:

        filtro = filtro[
            filtro["Item"]
            .astype(str)
            .str.contains(item, case=False)
        ]

    # ==========================================
    # DATA EDITOR
    # ==========================================

    st.markdown("### 📋 Itens do Pedido")

    tabela = st.data_editor(

        filtro,

        use_container_width=True,

        hide_index=True,

        num_rows="fixed",

        column_config={

            "Selecionar": st.column_config.CheckboxColumn(),

            "Quantidade": st.column_config.NumberColumn(
                step=1
            ),

            "Valor Unitário": st.column_config.NumberColumn(
                format="R$ %.2f"
            ),

            "Valor Total": st.column_config.NumberColumn(
                format="R$ %.2f",
                disabled=True
            )

        }

    )

    # ==========================================
    # RECALCULAR
    # ==========================================

    tabela["Valor Total"] = (
        tabela["Quantidade"]
        * tabela["Valor Unitário"]
    )

    selecionados = tabela[
        tabela["Selecionar"]
    ]

    total = selecionados["Valor Total"].sum()

    quantidade = selecionados["Quantidade"].sum()

    itens = len(selecionados)

    # ==========================================
    # RESUMO
    # ==========================================

    st.markdown("### 📊 Resumo")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Itens Selecionados",
        itens
    )

    c2.metric(
        "Quantidade Total",
        int(quantidade)
    )

    c3.metric(
        "Valor Total",
        f"R$ {total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    )

    # ==========================================
    # OBSERVAÇÕES
    # ==========================================

    observacoes = st.text_area(

        "Observações",

        height=120,

        placeholder="Digite aqui observações para o fornecedor..."

    )

    # ==========================================
    # BOTÃO
    # ==========================================

    st.button(
        "📄 Emitir Pedido",
        type="primary"
    )