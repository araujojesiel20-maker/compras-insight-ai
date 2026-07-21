import streamlit as st

st.write("CARDS.PY CARREGADO")

def card(titulo, valor, icone, cor="#E68A13"):

    st.markdown(
        f"""
### {icone}

**{titulo}**

# {valor}
"""
    )