import streamlit as st
from textwrap import dedent


def card(titulo, valor, icone, cor="#E68A13"):

    html = dedent(f"""
    <div style="
        background:rgba(255,255,255,.08);
        border-left:6px solid {cor};
        border-radius:18px;
        padding:18px;
        height:170px;
        box-shadow:0 6px 16px rgba(0,0,0,.25);
    ">

        <div style="
            font-size:34px;
            margin-bottom:10px;
        ">
            {icone}
        </div>

        <div style="
            color:#FFFFFF;
            font-size:17px;
            font-weight:600;
            line-height:1.3;
            min-height:42px;
        ">
            {titulo}
        </div>

        <div style="
            color:white;
            font-size:34px;
            font-weight:700;
            margin-top:10px;
            line-height:1.1;
            word-break:break-word;
        ">
            {valor}
        </div>

    </div>
    """)

    st.markdown(html, unsafe_allow_html=True)