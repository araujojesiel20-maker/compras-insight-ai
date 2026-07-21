import streamlit as st
from datetime import datetime


def mostrar_cabecalho():

    hoje = datetime.now().strftime("%d/%m/%Y")

    st.markdown(
        """
        <style>

        .header-box{

            background:linear-gradient(135deg,#34377A,#2B2F66);

            border-radius:18px;

            padding:20px 28px;

            border-left:6px solid #E68A13;

            box-shadow:0 8px 20px rgba(0,0,0,.20);

            margin-bottom:20px;

        }

        .titulo{

            color:white;

            font-size:34px;

            font-weight:700;

            margin:0;

            line-height:1.1;

        }

        .subtitulo{

            color:#E68A13;

            font-size:18px;

            margin-top:4px;

            font-weight:600;

        }

        .descricao{

            color:#D7DCF8;

            font-size:14px;

            margin-top:8px;

        }

        .status{

            text-align:right;

            color:white;

            font-size:15px;

            line-height:1.8;

        }

        .online{

            color:#4CD964;

            font-weight:bold;

        }

        </style>
        """,
        unsafe_allow_html=True
    )

    with st.container():

        st.markdown("<div class='header-box'>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1.2, 5, 2])

        with col1:

            st.image(
                "imagens/logo.png",
                width=125
            )

        with col2:

            st.markdown(
                """
                <div class="titulo">
                    Compras Insight AI
                </div>

                <div class="subtitulo">
                    Laticínios Stefanello
                </div>

                <div class="descricao">
                    Plataforma inteligente para análise de compras, consumo,
                    estoque, indicadores financeiros e apoio à decisão.
                </div>
                """,
                unsafe_allow_html=True
            )

        with col3:

            st.markdown(
                f"""
                <div class="status">

                📅 <strong>{hoje}</strong>

                <br>

                <span class="online">🟢 Sistema Online</span>

                <br>

                Versão 1.0

                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("</div>", unsafe_allow_html=True)