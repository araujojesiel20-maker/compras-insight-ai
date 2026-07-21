import streamlit as st
import plotly.express as px
import pandas as pd

AZUL = "#34377A"
LARANJA = "#E68A13"
FUNDO = "#FFFFFF"
GRADE = "#ECECEC"
TEXTO = "#303030"


# =====================================================
# REDUZ NOMES MUITO GRANDES
# =====================================================

def reduzir(texto, tamanho=30):

    texto = str(texto)

    if len(texto) <= tamanho:
        return texto

    return texto[:tamanho] + "..."


# =====================================================
# LAYOUT
# =====================================================

def aplicar_layout(fig):

    fig.update_layout(

        template="plotly_white",

        paper_bgcolor=FUNDO,
        plot_bgcolor=FUNDO,

        font=dict(
            family="Segoe UI",
            size=11,
            color=TEXTO
        ),

        title=dict(
            x=0.02,
            font=dict(
                size=18,
                color=AZUL
            )
        ),

        legend=dict(
            orientation="h",
            y=-0.25,
            x=0.5,
            xanchor="center",
            font=dict(size=10)
        ),

        margin=dict(
            l=60,
            r=30,
            t=60,
            b=70
        ),

        height=560

    )

    fig.update_xaxes(
        showgrid=False,
        zeroline=False
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor=GRADE,
        zeroline=False
    )

    return fig


# =====================================================
# DASHBOARD
# =====================================================

def mostrar_graficos(df):

    st.markdown("## 📊 Indicadores Gráficos")

    if df.empty:

        st.warning("Nenhum dado encontrado.")

        return

    df = df.copy()

    df["Data"] = pd.to_datetime(df["Data"])

    # --------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        mensal = (
            df.groupby(df["Data"].dt.to_period("M"))
            ["Custo total"]
            .sum()
            .reset_index()
        )

        mensal["Data"] = mensal["Data"].astype(str)

        fig = px.line(
            mensal,
            x="Data",
            y="Custo total",
            title="📈 Evolução das Compras",
            markers=True
        )

        fig.update_traces(
            line=dict(
                color=LARANJA,
                width=3
            ),

            marker=dict(
                size=6
            )
        )

        aplicar_layout(fig)

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False}
        )

    with col2:

        fornecedores = (
            df.groupby("Fornecedor")
            ["Custo total"]
            .sum()
            .sort_values(ascending=False)
            .head(8)
            .reset_index()
        )

        fornecedores["Fornecedor"] = fornecedores["Fornecedor"].apply(reduzir)

        fig = px.pie(
            fornecedores,
            names="Fornecedor",
            values="Custo total",
            hole=.70,
            title="🍩 Participação dos Fornecedores"
        )

        fig.update_traces(
            textfont_size=11
        )

        aplicar_layout(fig)

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False}
        )

    # --------------------------------------------------

    col3, col4 = st.columns(2)

    with col3:

        produtos = (
            df.groupby("Item")
            ["Custo total"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .sort_values()
            .reset_index()
        )

        produtos["Item"] = produtos["Item"].apply(reduzir)

        fig = px.bar(
            produtos,
            x="Custo total",
            y="Item",
            orientation="h",
            color="Custo total",
            title="📦 Top Produtos",
            color_continuous_scale="YlOrBr"
        )

        fig.update_layout(
            coloraxis_showscale=False
        )

        aplicar_layout(fig)

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False}
        )

    with col4:

        fornecedores = (
            df.groupby("Fornecedor")
            ["Custo total"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .sort_values()
            .reset_index()
        )

        fornecedores["Fornecedor"] = fornecedores["Fornecedor"].apply(reduzir)

        fig = px.bar(
            fornecedores,
            x="Custo total",
            y="Fornecedor",
            orientation="h",
            color="Custo total",
            title="🏭 Top Fornecedores",
            color_continuous_scale="Blues"
        )

        fig.update_layout(
            coloraxis_showscale=False
        )

        aplicar_layout(fig)

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False}
        )

    st.markdown("<br>", unsafe_allow_html=True)