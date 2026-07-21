import math
import re

import pandas as pd
from rapidfuzz import process


# =====================================================
# CARREGAR PLANILHA
# =====================================================

def carregar_planilha(arquivo):

    df = pd.read_excel(
        arquivo,
        header=1
    )

    df = df.loc[
        :,
        ~df.columns.astype(str).str.contains("^Unnamed")
    ]

    df["Data"] = pd.to_datetime(df["Data"])

    return df


# =====================================================
# MOEDA (INTELIGENTE)
# =====================================================

def formatar_moeda(valor):

    if valor is None or pd.isna(valor):
        return "R$ 0,00"

    valor = float(valor)

    if abs(valor) >= 1_000_000_000:

        return (
            f"R$ {valor/1_000_000_000:.2f} Bi"
            .replace(".", ",")
        )

    if abs(valor) >= 1_000_000:

        return (
            f"R$ {valor/1_000_000:.2f} Mi"
            .replace(".", ",")
        )

    if abs(valor) >= 1_000:

        return (
            f"R$ {valor/1_000:.1f} mil"
            .replace(".", ",")
        )

    return (
        f"R$ {valor:,.2f}"
        .replace(",", "§")
        .replace(".", ",")
        .replace("§", ".")
    )


# =====================================================
# NÚMEROS
# =====================================================

def formatar_numero(valor):

    if valor is None or pd.isna(valor):
        return "0"

    valor = int(round(float(valor)))

    if abs(valor) >= 1_000_000:

        return (
            f"{valor/1_000_000:.1f} Mi"
            .replace(".", ",")
        )

    if abs(valor) >= 1000:

        return (
            f"{valor/1000:.1f} mil"
            .replace(".", ",")
        )

    return f"{valor}"


# =====================================================
# PERCENTUAL
# =====================================================

def formatar_percentual(valor):

    if valor is None or pd.isna(valor):
        return "0,0%"

    return (
        f"{float(valor):.1f}%"
        .replace(".", ",")
    )


# =====================================================
# DATA
# =====================================================

def formatar_data(data):

    if pd.isna(data):
        return ""

    return pd.to_datetime(
        data
    ).strftime("%d/%m/%Y")


# =====================================================
# NORMALIZAÇÃO
# =====================================================

def normalizar_item(texto):

    if texto is None:
        return ""

    texto = str(texto).upper()

    texto = texto.strip()

    texto = re.sub(r"\s+", " ", texto)

    texto = texto.replace("( ", "(")
    texto = texto.replace(" )", ")")

    texto = texto.replace(" KG", "KG")
    texto = texto.replace(" G", "G")
    texto = texto.replace(" ML", "ML")
    texto = texto.replace(" L", "L")

    texto = texto.replace(" ,", ",")
    texto = texto.replace(", ", ",")

    return texto


# =====================================================
# MATCH
# =====================================================

def localizar_item(nome, lista):

    resultado = process.extractOne(
        normalizar_item(nome),
        lista,
        score_cutoff=85
    )

    if resultado:

        return resultado[0]

    return None