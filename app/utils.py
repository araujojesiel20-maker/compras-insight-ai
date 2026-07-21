import pandas as pd
import math
from rapidfuzz import process

# =====================================================
# CARREGAR PLANILHA DE COMPRAS
# =====================================================

def carregar_planilha(arquivo):

    df = pd.read_excel(
        arquivo,
        header=1
    )

    # Remove colunas "Unnamed"
    df = df.loc[:, ~df.columns.astype(str).str.contains("^Unnamed")]

    # Converte datas
    df["Data"] = pd.to_datetime(df["Data"])

    return df


# =====================================================
# FORMATAÇÃO DE MOEDA
# =====================================================

def formatar_moeda(valor):

    if valor is None or pd.isna(valor):
        return "R$ 0,00"

    valor = float(valor)

    return (
        f"R$ {valor:,.2f}"
        .replace(",", "§")
        .replace(".", ",")
        .replace("§", ".")
    )


# =====================================================
# FORMATAÇÃO DE NÚMEROS
# =====================================================

def formatar_numero(valor):

    if valor is None or pd.isna(valor):
        return "0"

    valor = int(round(float(valor)))

    return (
        f"{valor:,}"
        .replace(",", ".")
    )


# =====================================================
# FORMATAÇÃO DE PERCENTUAL
# =====================================================

def formatar_percentual(valor):

    if valor is None or pd.isna(valor):
        return "0,0%"

    return (
        f"{float(valor):.1f}%"
        .replace(".", ",")
    )


# =====================================================
# FORMATAÇÃO DE DATA
# =====================================================

def formatar_data(data):

    if pd.isna(data):
        return ""

    return pd.to_datetime(data).strftime("%d/%m/%Y")

import re


# ===============================================
# NORMALIZA O NOME DOS PRODUTOS
# ===============================================

def normalizar_item(texto):

    if texto is None:
        return ""

    texto = str(texto).upper()

    texto = texto.strip()

    # Remove espaços duplicados
    texto = re.sub(r"\s+", " ", texto)

    # Remove espaço antes/depois dos parênteses
    texto = texto.replace("( ", "(")
    texto = texto.replace(" )", ")")

    # Padroniza unidades
    texto = texto.replace(" KG", "KG")
    texto = texto.replace(" G", "G")
    texto = texto.replace(" ML", "ML")
    texto = texto.replace(" L", "L")

    # Remove espaços antes e depois das vírgulas
    texto = texto.replace(" ,", ",")
    texto = texto.replace(", ", ",")

    return texto
def localizar_item(nome, lista):

    resultado = process.extractOne(
        normalizar_item(nome),
        lista,
        score_cutoff=85
    )

    if resultado:

        return resultado[0]

    return None