import pandas as pd


def carregar_saida(arquivo):

    df = pd.read_excel(
        arquivo,
        header=0
    )

    # Remove primeira coluna vazia
    if df.columns[0] != "Codigo ":
        df = df.iloc[:, 1:]

    # Remove espaços dos nomes das colunas
    df.columns = df.columns.str.strip()

    # Converte data
    df["Data de Consumo"] = pd.to_datetime(df["Data de Consumo"])

    # Renomeia para manter o padrão do sistema
    df.rename(
        columns={
            "Data de Consumo": "Data",
            "Custo Unitário": "Custo Unitario"
        },
        inplace=True
    )

    # Calcula o valor consumido
    df["Valor Consumido"] = (
        df["Quantidade"] *
        df["Custo Unitario"]
    )

    return df