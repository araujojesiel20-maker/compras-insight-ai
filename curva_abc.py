import streamlit as st
import plotly.express as px

from utils import (
    formatar_moeda,
    formatar_numero,
    formatar_percentual
)


def mostrar_curva_abc(df):

    st.divider()

    st.header("📊 Curva ABC")

    if df.empty:

        st.warning("Nenhum dado encontrado para os filtros selecionados.")

        return

    # =====================================================
    # AGRUPAMENTO
    # =====================================================

    chave = (
        "Item_Normalizado"
        if "Item_Normalizado" in df.columns
        else "Item"
    )

    abc = (

        df.groupby(chave)

        .agg({

            "Item": "first",

            "Custo total": "sum"

        })

        .reset_index()

        .sort_values(

            "Custo total",

            ascending=False

        )

    )

    # =====================================================
    # CURVA ABC
    # =====================================================

    total = abc["Custo total"].sum()

    abc["Percentual"] = (

        abc["Custo total"]

        /

        total

    ) * 100

    abc["Acumulado"] = abc["Percentual"].cumsum()

    def classe(valor):

        if valor <= 80:
            return "A"

        elif valor <= 95:
            return "B"

        return "C"

    abc["Classe"] = abc["Acumulado"].apply(classe)

    # =====================================================
    # CARDS
    # =====================================================

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(

            "🔴 Classe A",

            formatar_numero(

                (abc["Classe"] == "A").sum()

            )

        )

    with c2:

        st.metric(

            "🟠 Classe B",

            formatar_numero(

                (abc["Classe"] == "B").sum()

            )

        )

    with c3:

        st.metric(

            "🟢 Classe C",

            formatar_numero(

                (abc["Classe"] == "C").sum()

            )

        )

    # =====================================================
    # GRÁFICO
    # =====================================================

    grafico = (

        abc.head(20)

        .sort_values("Custo total")

    )

    fig = px.bar(

        grafico,

        x="Custo total",

        y="Item",

        orientation="h",

        color="Classe",

        text="Custo total",

        title="Produtos de Maior Impacto Financeiro",

        color_discrete_map={

            "A": "#D62828",

            "B": "#F4A261",

            "C": "#2A9D8F"

        }

    )

    fig.update_traces(

        texttemplate="R$ %{x:,.0f}",

        textposition="outside"

    )

    fig.update_layout(

        template="plotly_white",

        paper_bgcolor="white",

        plot_bgcolor="white",

        height=550,

        coloraxis_showscale=False,

        yaxis=dict(

            categoryorder="total ascending"

        )

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    # =====================================================
    # RESUMO
    # =====================================================

    resumo = (

        abc.groupby("Classe")

        .agg(

            Produtos=("Item", "count"),

            Valor=("Custo total", "sum"),

            Percentual=("Percentual", "sum")

        )

        .reset_index()

    )

    resumo["Valor"] = resumo["Valor"].apply(

        formatar_moeda

    )

    resumo["Percentual"] = resumo["Percentual"].apply(

        formatar_percentual

    )

    st.subheader("📋 Resumo da Curva ABC")

    st.dataframe(

        resumo,

        use_container_width=True,

        hide_index=True

    )

    # =====================================================
    # TABELA
    # =====================================================

    tabela = abc.copy()

    tabela["Custo total"] = tabela["Custo total"].apply(

        formatar_moeda

    )

    tabela["Percentual"] = tabela["Percentual"].apply(

        formatar_percentual

    )

    tabela["Acumulado"] = tabela["Acumulado"].apply(

        formatar_percentual

    )

    tabela = tabela[

        [

            "Item",

            "Classe",

            "Custo total",

            "Percentual",

            "Acumulado"

        ]

    ]

    st.subheader("📑 Produtos Classificados")

    st.dataframe(

        tabela,

        use_container_width=True,

        hide_index=True

    )