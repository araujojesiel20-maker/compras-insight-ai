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
from pedido_compra import mostrar_pedido_compra


# ======================================================
# CONFIGURAÇÃO DA PÁGINA
# ======================================================

st.set_page_config(
    page_title=TITULO,
    page_icon=ICONE,
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================================================
# CSS
# ======================================================

css_path = Path("styles.css")

if css_path.exists():

    st.markdown(
        f"<style>{css_path.read_text(encoding='utf-8')}</style>",
        unsafe_allow_html=True
    )

# ======================================================
# CABEÇALHO
# ======================================================

mostrar_cabecalho()

st.divider()

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

if arquivo_base is None:

    st.markdown(
        """
<div style="
background:#34377A;
padding:30px;
border-radius:18px;
border-left:8px solid #E68A13;
box-shadow:0 8px 18px rgba(0,0,0,.25);
margin-top:20px;
">

<h2 style="
color:white;
margin-top:0;
margin-bottom:20px;
font-size:30px;
font-weight:700;
">

📂 Bem-vindo ao Compras Insight AI

</h2>

<p style="
color:#F5F5F5;
font-size:18px;
line-height:1.8;
">

Carregue a planilha principal para iniciar a análise inteligente de compras.

O arquivo deve conter as seguintes abas:

</p>

<div style="
background:rgba(255,255,255,.08);
padding:20px;
border-radius:12px;
margin-top:15px;
">

<ul style="
color:white;
font-size:18px;
line-height:2;
margin-left:20px;
">

<li>📦 Compras</li>

<li>📉 Consumo</li>

<li>🏬 Estoque</li>

</ul>

</div>

</div>
        """,
        unsafe_allow_html=True
    )

    st.stop()

# ======================================================
# PROCESSAMENTO
# ======================================================

with st.spinner("Processando a base de dados..."):

    base = carregar_base(arquivo_base)

    compras = base["compras"]
    consumo = base["consumo"]
    estoque = base["estoque"]

    compras, consumo, estoque = preparar_dados(
        compras,
        consumo,
        estoque
    )

# ======================================================
# FILTROS
# ======================================================

st.divider()

compras_filtradas = aplicar_filtros(compras)

# ======================================================
# CONSUMO FILTRADO
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

st.divider()

container_dashboard = st.container()

with container_dashboard:

    mostrar_dashboard(
        compras_filtradas,
        consumo_filtrado,
        comparativo
    )

# ======================================================
# CURVA ABC
# ======================================================

st.divider()

container_abc = st.container()

with container_abc:

    mostrar_curva_abc(
        compras_filtradas
    )

# ======================================================
# PRIORIDADES
# ======================================================

st.divider()

container_prioridades = st.container()

with container_prioridades:

    mostrar_prioridades(
        comparativo,
        compras_filtradas
    )

# ======================================================
# SUGESTÃO DE COMPRA
# ======================================================

st.divider()

container_sugestao = st.container()

with container_sugestao:

    mostrar_sugestao_compra(
        comparativo,
        compras_filtradas
    )

# ======================================================
# PEDIDO DE COMPRA
# ======================================================

st.divider()

container_pedido = st.container()

with container_pedido:

    mostrar_pedido_compra(
        compras_filtradas
    )

# ======================================================
# GRÁFICOS
# ======================================================

st.divider()

container_graficos = st.container()

with container_graficos:

    mostrar_graficos(
        compras_filtradas
    )

# ======================================================
# IA
# ======================================================

st.divider()

container_ia = st.container()

with container_ia:

    perguntar_ia(
        compras_filtradas
    )

# ======================================================
# RODAPÉ
# ======================================================

st.markdown(
    """
<br><br>

<div style="text-align:center;color:#BFC6E0;font-size:14px;">

Compras Insight AI • Desenvolvido para otimizar decisões de compras e estoque.

</div>
""",
    unsafe_allow_html=True
)