import pandas as pd
import re
import unicodedata


# ==========================================================
# REMOVE ACENTOS
# ==========================================================

def remover_acentos(texto):

    if pd.isna(texto):
        return ""

    texto = str(texto)

    return "".join(
        c for c in unicodedata.normalize("NFKD", texto)
        if not unicodedata.combining(c)
    )


# ==========================================================
# NORMALIZA NOME DO PRODUTO
# ==========================================================

def normalizar_nome(nome):

    if pd.isna(nome):
        return ""

    nome = str(nome).upper()

    nome = remover_acentos(nome)

    # Padronizações comuns
    substituicoes = {

        " LTS ": " L ",
        " LT ": " L ",
        " LITRO ": " L ",
        " LITROS ": " L ",

        " KG ": " KG ",
        " KGS ": " KG ",
        " QUILO ": " KG ",
        " QUILOS ": " KG ",

        " GR ": " G ",
        " GRS ": " G ",
        " GRAMA ": " G ",
        " GRAMAS ": " G ",

        " ML ": " ML ",

        " UND ": "",
        " UN ": "",
        " UNID ": "",
        " UNIDADE ": "",

        " CX ": "",
        " CAIXA ": "",

        " PCT ": "",
        " PACOTE ": ""
    }

    nome = f" {nome} "

    for antigo, novo in substituicoes.items():
        nome = nome.replace(antigo, novo)

    # Remove caracteres especiais
    nome = re.sub(r"[^A-Z0-9 ]", " ", nome)

    # Remove espaços repetidos
    nome = re.sub(r"\s+", " ", nome)

    return nome.strip()


# ==========================================================
# NORMALIZA UMA COLUNA
# ==========================================================

def normalizar_dataframe(df, coluna="Item"):

    df = df.copy()

    df["Item_Normalizado"] = df[coluna].apply(
        normalizar_nome
    )

    return df