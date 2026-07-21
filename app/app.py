import streamlit as st
from pathlib import Path

from cabecalho import mostrar_cabecalho
from config import TITULO, ICONE
from dashboard import mostrar_dashboard
from filtros import aplicar_filtros
from graficos import mostrar_graficos
from ia import perguntar_ia
from curva_abc import mostrar_curva_abc
from sugestao_compra import mostrar_sugestao_compra
from prioridades import mostrar_prioridades
from comparativo import mostrar_comparativo
from matcher import preparar_dados
from carregador import carregar_base


# ======================================================
# CONFIGURAÇÃO DA PÁGINA
# ======================================================

st.set_page_config(
    page_title=TITULO,
    page_icon=ICONE,
    layout="wide"
)

# ======================================================
# CSS
# ======================================================

css = Path("app/styles.css").read_text(encoding="utf-8")

st.markdown(
    f"<style>{css}</style>",
    unsafe_allow_html=True
)

# ======================================================
# CABEÇALHO
# ======================================================

mostrar_cabecalho()

# ======================================================
# UPLOAD
# ======================================================

arquivo_base = st.file_uploader(
    "📂 Base de Dados Compras Insight AI",
    type=["xlsx"],
    help="Arquivo contendo as abas Compras, Consumo e Estoque."
)
# ======================================================
# AGUARDA UPLOAD
# ======================================================

# ======================================================
# AGUARDA UPLOAD
# ======================================================

if arquivo_base is None:

    st.markdown(
        """
<div style="
background:#34377A;
padding:30px;
border-radius:14px;
border-left:8px solid #E68A13;
box-shadow:0 4px 12px rgba(0,0,0,.25);
margin-top:10px;
">

<h2 style="
color:white;
margin-top:0;
margin-bottom:20px;
font-size:34px;
font-weight:700;
">

📂 Para iniciar a análise

</h2>

<p style="
color:#F5F5F5;
font-size:18px;
margin-bottom:20px;
">

Carregue a planilha principal contendo as seguintes abas:

</p>

<div style="
background:rgba(255,255,255,.08);
padding:18px;
border-radius:10px;
">

<ul style="
color:#FFFFFF;
font-size:18px;
line-height:2.1;
margin-left:20px;
">

<li>📦 <strong>Compras</strong></li>

<li>📉 <strong>Consumo</strong></li>

<li>🏬 <strong>Estoque</strong></li>

</ul>

</div>

</div>
""",
        unsafe_allow_html=True
    )

    st.stop()

else:

    # ======================================================
    # CARREGA PLANILHAS
    # ======================================================

    base = carregar_base(arquivo_base)

    compras = base["compras"]
    consumo = base["consumo"]
    estoque = base["estoque"]

    # ======================================================
    # RELACIONA PRODUTOS
    # ======================================================

    compras, consumo, estoque = preparar_dados(
        compras,
        consumo,
        estoque
)


    # ======================================================
    # FILTROS
    # ======================================================

    compras_filtradas = aplicar_filtros(compras)

    # ======================================================
    # FILTRA O CONSUMO PELOS MESMOS PRODUTOS
    # ======================================================

    itens = compras_filtradas["Item_Normalizado"].unique()

    consumo_filtrado = consumo[
        consumo["Item_Correspondente"].isin(itens)
    ].copy()

# ======================================================
# COMPARATIVO
# ======================================================

    comparativo = mostrar_comparativo(
        compras_filtradas,
        consumo_filtrado,
        estoque
)

# ======================================================
# DASHBOARD
# ======================================================

    mostrar_dashboard(
        compras_filtradas,
        consumo_filtrado,
        comparativo
)

    # ======================================================
    # CURVA ABC
    # ======================================================

    mostrar_curva_abc(
    compras_filtradas
)


    # ======================================================
    # PRIORIDADES
    # ======================================================

    mostrar_prioridades(
            comparativo,
            compras_filtradas
    )

    # ======================================================
    # SUGESTÃO DE COMPRA
    # ======================================================

    mostrar_sugestao_compra(
            comparativo,
            compras_filtradas
    )

    # ======================================================
    # GRÁFICOS
    # ======================================================

    mostrar_graficos(
            compras_filtradas
    )

    # ======================================================
    # IA
    # ======================================================

    perguntar_ia(
            compras_filtradas
        )