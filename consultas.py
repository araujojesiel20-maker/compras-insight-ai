import sqlite3
import pandas as pd


def carregar_compras():

    conn = sqlite3.connect("dados/compras.db")

    df = pd.read_sql(

        "SELECT * FROM compras",

        conn

    )

    conn.close()

    df["Data"] = pd.to_datetime(df["Data"])

    return df