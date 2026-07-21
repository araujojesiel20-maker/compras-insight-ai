import streamlit as st


def card(titulo, valor, icone, cor="#E68A13"):

    st.html(f"""
    <div style="
        background:#4A4F92;
        border-left:6px solid {cor};
        border-radius:18px;
        padding:18px;
        height:170px;
        display:flex;
        flex-direction:column;
        justify-content:space-between;
        box-shadow:0 8px 18px rgba(0,0,0,.25);
    ">

        <div style="
            font-size:34px;
        ">
            {icone}
        </div>

        <div style="
            color:white;
            font-size:16px;
            font-weight:600;
        ">
            {titulo}
        </div>

        <div style="
            color:white;
            font-size:30px;
            font-weight:700;
            line-height:1.1;
        ">
            {valor}
        </div>

    </div>
    """)