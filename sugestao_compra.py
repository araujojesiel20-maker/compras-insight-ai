import streamlit as st

from pdf_compras import gerar_pdf

from utils import (
    formatar_numero,
    formatar_moeda
)


def mostrar_sugestao_compra(comparativo, compras):

    st.divider()

    st.header("🛒 Sugestão Inteligente de Compras")

    if comparativo.empty:

        st.warning("Nenhum dado disponível.")

        return

    sugestao = comparativo.copy()

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

    if "Preço Médio" not in sugestao.columns:

        if chave in sugestao.columns:

            sugestao["Preço Médio"] = sugestao[
                chave
            ].map(preco)

        else:

            sugestao["Preço Médio"] = sugestao[
                "Item"
            ].map(preco)

    sugestao["Preço Médio"] = sugestao[
        "Preço Médio"
    ].fillna(0)

    # =====================================================
    # UTILIZA A NOVA LÓGICA
    # =====================================================

    if "Comprar" not in sugestao.columns:

        st.error(
            "A coluna 'Comprar' não foi encontrada no comparativo."
        )

        return

    sugestao["Quantidade Recomendada"] = sugestao["Comprar"]

    sugestao = sugestao[
        sugestao["Quantidade Recomendada"] > 0
    ].copy()

    if sugestao.empty:

        st.success("✅ Todos os estoques estão acima do mínimo.")

        return

    # =====================================================
    # VALOR ESTIMADO
    # =====================================================

    sugestao["Valor Estimado"] = (

        sugestao["Quantidade Recomendada"]

        *

        sugestao["Preço Médio"]

    )

    sugestao = sugestao.sort_values(

        "Valor Estimado",

        ascending=False

    )

    # =====================================================
    # KPIs
    # =====================================================

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(

            "Produtos",

            formatar_numero(

                len(sugestao)

            )

        )

    with c2:

        st.metric(

            "Quantidade",

            formatar_numero(

                sugestao["Quantidade Recomendada"].sum()

            )

        )

    with c3:

        st.metric(

            "Valor Estimado",

            formatar_moeda(

                sugestao["Valor Estimado"].sum()

            )

        )

    # =====================================================
    # TABELA
    # =====================================================

    tabela = sugestao[
        [
            "Item",
            "Em estoque",
            "Estoque mínimo",
            "Estoque desejável",
            "Quantidade Recomendada",
            "Unidade",
            "Preço Médio",
            "Valor Estimado",
            "Motivo"
        ]
    ].copy()

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

    tabela["Quantidade Recomendada"] = tabela.apply(
        lambda x: f"{formatar_numero(x['Quantidade Recomendada'])} {x['Unidade']}",
        axis=1
    )

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
    # TOTAL
    # =====================================================

    total = sugestao["Valor Estimado"].sum()

    st.success(

        f"""

### 💰 Valor estimado da próxima compra

# {formatar_moeda(total)}

"""

    )

    st.divider()

    # =====================================================
    # PDF
    # =====================================================

    col1, col2 = st.columns(2)

    with col1:

        if st.button(

            "📄 Gerar Relatório PDF",

            use_container_width=True

        ):

            caminho_pdf = gerar_pdf(

                comparativo,

                compras

            )

            st.session_state["pdf_gerado"] = caminho_pdf

            st.success(

                "✅ Relatório gerado com sucesso!"

            )

    with col2:

        if "pdf_gerado" in st.session_state:

            with open(

                st.session_state["pdf_gerado"],

                "rb"

            ) as arquivo:

                st.download_button(

                    "⬇️ Baixar Relatório PDF",

                    data=arquivo,

                    file_name="Sugestao_Compras.pdf",

                    mime="application/pdf",

                    use_container_width=True

                )