import streamlit as st
import plotly.express as px
import pandas as pd

# ==========================================
# PALETA DE CORES
# ==========================================

AZUL = "#34377A"
LARANJA = "#E68A13"
FUNDO = "#FFFFFF"
GRADE = "#E8E8E8"
TEXTO = "#2C2C2C"


# ==========================================
# LAYOUT PADRÃO
# ==========================================

def aplicar_layout(fig):

    fig.update_layout(

        template="plotly_white",

        paper_bgcolor=FUNDO,

        plot_bgcolor=FUNDO,

        font=dict(
            family="Segoe UI",
            size=13,
            color=TEXTO
        ),

        title=dict(
            x=0.02,
            font=dict(
                size=21,
                color=AZUL
            )
        ),

        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),

        margin=dict(
            l=20,
            r=20,
            t=70,
            b=20
        ),

        height=470

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


# ==========================================
# DASHBOARD GRÁFICO
# ==========================================

def mostrar_graficos(df):

    st.markdown("## 📊 Indicadores Gráficos")

    if df.empty:

        st.warning("Nenhum dado encontrado para os filtros selecionados.")

        return

    df = df.copy()

    df["Data"] = pd.to_datetime(df["Data"], errors="coerce")

    df = df.dropna(subset=["Data"])

    # =====================================================
    # PRIMEIRA LINHA
    # =====================================================

    col1, col2 = st.columns(2)

    with col1:

        mensal = (
            df.groupby(
                df["Data"].dt.to_period("M")
            )["Custo total"]
            .sum()
            .reset_index()
        )

        mensal["Data"] = mensal["Data"].astype(str)

        fig = px.line(
            mensal,
            x="Data",
            y="Custo total",
            markers=True,
            title="📈 Evolução das Compras"
        )

        fig.update_traces(
            line=dict(
                color=LARANJA,
                width=4
            ),
            marker=dict(
                size=8
            ),
            fill="tozeroy",
            fillcolor="rgba(230,138,19,.18)"
        )

        aplicar_layout(fig)

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False}
        )

    with col2:

        fornecedores = (
            df.groupby("Fornecedor")["Custo total"]
            .sum()
            .sort_values(ascending=False)
            .head(8)
            .reset_index()
        )

        fig = px.pie(
            fornecedores,
            names="Fornecedor",
            values="Custo total",
            hole=0.68,
            title="🍩 Participação dos Fornecedores"
        )

        aplicar_layout(fig)

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False}
        )

    # =====================================================
    # SEGUNDA LINHA
    # =====================================================

    col3, col4 = st.columns(2)

    with col3:

        produtos = (
            df.groupby("Item")["Custo total"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .sort_values()
            .reset_index()
        )

        fig = px.bar(
            produtos,
            x="Custo total",
            y="Item",
            orientation="h",
            title="📦 Top 10 Produtos",
            color="Custo total",
            color_continuous_scale="YlOrBr",
            text_auto=".2s"
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
            df.groupby("Fornecedor")["Custo total"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .sort_values()
            .reset_index()
        )

        fig = px.bar(
            fornecedores,
            x="Custo total",
            y="Fornecedor",
            orientation="h",
            title="🏭 Top 10 Fornecedores",
            color="Custo total",
            color_continuous_scale="Blues",
            text_auto=".2s"
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