import sqlite3
from pathlib import Path

# Pasta onde está este arquivo
BASE_DIR = Path(__file__).resolve().parent

# Banco de dados
BANCO = BASE_DIR / "aprendizado.db"


def conectar():

    conn = sqlite3.connect(BANCO)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS mapeamentos(

        item_consumo TEXT PRIMARY KEY,

        item_compra TEXT

    )
    """)

    conn.commit()

    return conn


def buscar(item):

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT item_compra
        FROM mapeamentos
        WHERE item_consumo = ?
        """,
        (item,)
    )

    resultado = cursor.fetchone()

    conn.close()

    if resultado:
        return resultado[0]

    return None


def salvar(item_consumo, item_compra):

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT OR REPLACE INTO mapeamentos
        VALUES(?,?)
        """,
        (
            item_consumo,
            item_compra
        )
    )

    conn.commit()
    conn.close()