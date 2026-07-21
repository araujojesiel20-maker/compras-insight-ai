import streamlit as st
from datetime import datetime


def mostrar_cabecalho():

    hoje = datetime.now().strftime("%d/%m/%Y")

    col1, col2, col3 = st.columns([1.2, 5, 1.5])

    with col1:

        st.image(
            "imagens/logo.png",
            width=170
        )

    with col2:

        st.markdown(
            """
            <h1 style='margin-bottom:0;color:white;'>
            Compras Insight AI
            </h1>

            <h4 style='margin-top:0;color:#E68A13;'>
            Laticínios Stefanello
            </h4>
            """,
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            f"""
            <div style="
                text-align:right;
                color:white;
                margin-top:15px;
            ">

            📅 {hoje}

            <br><br>

            🟢 Sistema Online

            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<hr>", unsafe_allow_html=True)