import pandas as pd
from rapidfuzz import process

from mapeamento import buscar
from normalizacao import normalizar_nome


# =====================================================
# LOCALIZA O ITEM
# =====================================================

def localizar_item(item, lista):

    # Verifica se existe um mapeamento manual
    conhecido = buscar(item)

    if conhecido:
        return conhecido

    # Correspondência exata
    if item in lista:
        return item

    # Correspondência aproximada
    resultado = process.extractOne(
        item,
        lista,
        score_cutoff=85
    )

    if resultado:
        return resultado[0]

    return None


# =====================================================
# PREPARA DADOS
# =====================================================

def preparar_dados(compras, consumo, estoque):

    compras = compras.copy()
    consumo = consumo.copy()
    estoque = estoque.copy()

    # -----------------------------------------
    # Normalização
    # -----------------------------------------

    compras["Item_Normalizado"] = compras["Item"].apply(
        normalizar_nome
    )

    consumo["Item_Normalizado"] = consumo["Item"].apply(
        normalizar_nome
    )

    estoque["Item_Normalizado"] = estoque["Item"].apply(
        normalizar_nome
    )

    # -----------------------------------------
    # Localiza correspondências
    # -----------------------------------------

    itens_compra = compras["Item_Normalizado"].unique()

    consumo["Item_Correspondente"] = consumo[
        "Item_Normalizado"
    ].apply(
        lambda x: localizar_item(
            x,
            itens_compra
        )
    )

    estoque["Item_Correspondente"] = estoque[
        "Item_Normalizado"
    ].apply(
        lambda x: localizar_item(
            x,
            itens_compra
        )
    )

    # -----------------------------------------
    # Preço médio
    # -----------------------------------------

    compras["Preço Médio"] = (
        compras["Custo total"] /
        compras["Quantidade"].replace(0, pd.NA)
    )

    compras["Preço Médio"] = compras["Preço Médio"].fillna(0)

    preco = (

        compras.groupby("Item_Normalizado")["Preço Médio"]

        .mean()

    )

    # -----------------------------------------
    # Fornecedor principal
    # -----------------------------------------

    fornecedor = (

        compras.groupby("Item_Normalizado")["Fornecedor"]

        .agg(

            lambda x:

            x.mode().iloc[0]

            if not x.mode().empty

            else "Fornecedor não localizado"

        )

    )

    # -----------------------------------------
    # Preenche informações no consumo
    # -----------------------------------------

    consumo["Fornecedor"] = consumo[
        "Item_Correspondente"
    ].map(fornecedor)

    consumo["Preço Médio"] = consumo[
        "Item_Correspondente"
    ].map(preco)

    consumo["Fornecedor"] = consumo[
        "Fornecedor"
    ].fillna("Fornecedor não localizado")

    consumo["Preço Médio"] = consumo[
        "Preço Médio"
    ].fillna(0)

    # -----------------------------------------
    # Preenche informações no estoque
    # -----------------------------------------

    estoque["Fornecedor"] = estoque[
        "Item_Correspondente"
    ].map(fornecedor)

    estoque["Preço Médio"] = estoque[
        "Item_Correspondente"
    ].map(preco)

    estoque["Fornecedor"] = estoque[
        "Fornecedor"
    ].fillna("Fornecedor não localizado")

    estoque["Preço Médio"] = estoque[
        "Preço Médio"
    ].fillna(0)

    return compras, consumo, estoque