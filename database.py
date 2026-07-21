import sqlite3
from pathlib import Path


# Pasta onde está este arquivo
BASE_DIR = Path(__file__).resolve().parent

# Pasta do banco
DADOS_DIR = BASE_DIR / "dados"
DADOS_DIR.mkdir(exist_ok=True)

# Caminho completo do banco
BANCO = DADOS_DIR / "compras.db"


def conectar():

    return sqlite3.connect(BANCO)


def criar_banco():

    conn = conectar()

    cursor = conn.cursor()

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


if __name__ == "__main__":
    criar_banco()