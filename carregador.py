import pandas as pd
from pathlib import Path
from config import (
    USAR_BASE_COMPARTILHADA,
    CAMINHO_PLANILHA
)


def _limpar_dataframe(df):
    """
    Limpa e padroniza um DataFrame.
    """

    # Remove colunas totalmente vazias
    df = df.dropna(axis=1, how="all")

    # Remove colunas 'Unnamed'
    df = df.loc[:, ~df.columns.astype(str).str.contains("^Unnamed")]

    # Remove espaços dos nomes das colunas
    df.columns = df.columns.astype(str).str.strip()

    # Remove espaços das células de texto
    for coluna in df.select_dtypes(include="object").columns:
        df[coluna] = df[coluna].astype(str).str.strip()

    return df


def carregar_base(upload=None):
    """
    Carrega a planilha principal do Compras Insight AI.

    Retorna:
        {
            "compras": DataFrame,
            "consumo": DataFrame,
            "estoque": DataFrame
        }
    """

    # =====================================
    # Origem da base
    # =====================================

    if USAR_BASE_COMPARTILHADA:

        if not CAMINHO_PLANILHA.exists():

            raise FileNotFoundError(
                f"Não foi possível localizar a base:\n{CAMINHO_PLANILHA}"
            )

        origem = CAMINHO_PLANILHA

    else:

        if upload is None:
            return None

        origem = upload

    try:

        arquivo = pd.ExcelFile(origem)

        abas = arquivo.sheet_names

        obrigatorias = ["Compras", "Consumo", "Estoque"]

        faltando = [aba for aba in obrigatorias if aba not in abas]

        if faltando:
            raise ValueError(
                f"As seguintes abas não foram encontradas: {', '.join(faltando)}"
            )

        compras = pd.read_excel(
            arquivo,
            sheet_name="Compras"
        )

        consumo = pd.read_excel(
            arquivo,
            sheet_name="Consumo"
        )

        estoque = pd.read_excel(
            arquivo,
            sheet_name="Estoque"
        )

        compras = _limpar_dataframe(compras)
        consumo = _limpar_dataframe(consumo)
        estoque = _limpar_dataframe(estoque)

        # =====================================
        # Converte datas
        # =====================================

        if "Data" in compras.columns:
            compras["Data"] = pd.to_datetime(
                compras["Data"],
                errors="coerce"
            )

        if "Data de Consumo" in consumo.columns:
            consumo["Data de Consumo"] = pd.to_datetime(
                consumo["Data de Consumo"],
                errors="coerce"
            )

        # =====================================
        # Converte colunas numéricas
        # =====================================

        numericas_compras = [
            "Quantidade",
            "Custo Unitário",
            "Custo total"
        ]

        for coluna in numericas_compras:
            if coluna in compras.columns:
                compras[coluna] = pd.to_numeric(
                    compras[coluna],
                    errors="coerce"
                ).fillna(0)

        numericas_consumo = [
            "Quantidade",
            "Custo Unitário",
            "Custo total"
]

        for coluna in numericas_consumo:
            if coluna in consumo.columns:
                consumo[coluna] = pd.to_numeric(
                    consumo[coluna],
                    errors="coerce"
                ).fillna(0)

        numericas_estoque = [
            "Em estoque",
            "Estoque mínimo",
            "Estoque desejável"
        ]

        for coluna in numericas_estoque:
            if coluna in estoque.columns:
                estoque[coluna] = pd.to_numeric(
                    estoque[coluna],
                    errors="coerce"
                ).fillna(0)

        return {
            "compras": compras,
            "consumo": consumo,
            "estoque": estoque
        }

    except Exception as e:
        raise Exception(f"Erro ao carregar a base: {e}")