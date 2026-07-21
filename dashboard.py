import streamlit as st

from cards import card
from utils import (
    formatar_moeda,
    formatar_numero
)


def mostrar_dashboard(compras, consumo, comparativo):

    # =====================================================
    # VALIDAÇÃO
    # =====================================================

    if compras.empty:

        st.warning("Nenhum dado de compras encontrado.")
        return

    # =====================================================
    # FINANCEIRO
    # =====================================================

    total_comprado = compras["Custo total"].sum()

    if consumo.empty:

        total_consumido = 0

    else:

        total_consumido = consumo["Custo total"].sum()

    saldo = total_comprado - total_consumido

    economia = saldo * 0.05 if saldo > 0 else 0

    # =====================================================
    # ESTOQUE
    # =====================================================

    abaixo_minimo = 0

    if (
        comparativo is not None
        and not comparativo.empty
        and "Em estoque" in comparativo.columns
        and "Estoque mínimo" in comparativo.columns
    ):

        abaixo_minimo = (
            comparativo["Em estoque"]
            <= comparativo["Estoque mínimo"]
        ).sum()

    # =====================================================
    # CARDS
    # =====================================================

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:

        card(
            "Total Comprado",
            formatar_moeda(total_comprado),
            "💰",
            "#F39C12"
        )

    with c2:

        card(
            "Total Consumido",
            formatar_moeda(total_consumido),
            "📉",
            "#27AE60"
        )

    with c3:

        card(
            "Saldo Financeiro",
            formatar_moeda(saldo),
            "📦",
            "#3498DB"
        )

    with c4:

        card(
            "Economia Potencial",
            formatar_moeda(economia),
            "💵",
            "#E74C3C"
        )

    with c5:

        card(
            "Abaixo do Estoque Mínimo",
            formatar_numero(abaixo_minimo),
            "⚠️",
            "#7D3C98"
        )

    st.markdown("<br>", unsafe_allow_html=True)