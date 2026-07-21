import sqlite3
import os


def conectar():

    os.makedirs("dados", exist_ok=True)

    return sqlite3.connect("dados/compras.db")


def criar_banco():

    conn = conectar()

    cursor = conn.cursor()

    # ============================
    # COMPRAS
    # ============================

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS compras(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        codigo TEXT,

        item TEXT,

        fornecedor TEXT,

        data DATE,

        quantidade REAL,

        custo_unitario REAL,

        custo_total REAL,

        id_importacao INTEGER,

        data_importacao TEXT,

        arquivo_origem TEXT

    )

    """)

    # ============================
    # IMPORTAÇÕES
    # ============================

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS importacoes(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        arquivo TEXT,

        data_importacao TEXT,

        registros INTEGER

    )

    """)

    conn.commit()

    conn.close()

    print("Banco criado com sucesso!")


if __name__ == "__main__":

    criar_banco()