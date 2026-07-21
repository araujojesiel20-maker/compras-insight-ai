import streamlit as st

from mapeamento import salvar


def confirmar(item_consumo, item_compra, similaridade):

    st.warning("⚠ Produto sem correspondência cadastrada")

    st.write(f"**Produto:** {item_consumo}")

    st.write(f"**Encontrado:** {item_compra}")

    st.write(f"**Similaridade:** {similaridade:.1f}%")

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            f"✅ Confirmar {item_consumo}"
        ):

            salvar(
                item_consumo,
                item_compra
            )

            st.success("Correspondência salva!")

            st.rerun()

    with col2:

        st.button(
            "✏ Escolher outro"
        )