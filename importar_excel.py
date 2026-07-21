import sqlite3
import pandas as pd


def importar_planilha(arquivo):

    df = pd.read_excel(
        arquivo,
        header=1
    )

    # Remove colunas sem nome
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

    # Padroniza nomes
    df.columns = [

        "Codigo",

        "Item",

        "Fornecedor",

        "Data",

        "Quantidade",

        "Custo_Unitario",

        "Custo_Total"

    ]

    df["Data"] = pd.to_datetime(df["Data"])

    conn = sqlite3.connect("dados/compras.db")

    df.to_sql(

        "compras",

        conn,

        if_exists="append",

        index=False

    )

    conn.close()

    return len(df)