import streamlit as st

from mapeamento import salvar


def confirmar_mapeamentos(pendentes, lista_produtos):

    st.divider()

    st.header("🧠 Aprendizado da IA")

    st.info(
        "Confirme os produtos abaixo. "
        "Após a confirmação a IA nunca mais perguntará."
    )

    for i, item in enumerate(pendentes):

        with st.container(border=True):

            st.write(
                f"### Produto do Consumo\n"
                f"**{item['consumo']}**"
            )

            st.write(
                f"Similaridade encontrada: "
                f"**{item['similaridade']:.1f}%**"
            )

            opcao = st.selectbox(

                "Produto correspondente",

                lista_produtos,

                index=lista_produtos.index(
                    item["sugestao"]
                ),

                key=f"produto_{i}"

            )

            if st.button(

                "✅ Confirmar",

                key=f"btn_{i}"

            ):

                salvar(

                    item["consumo"],

                    opcao

                )

                st.success("Aprendido!")

                st.rerun()