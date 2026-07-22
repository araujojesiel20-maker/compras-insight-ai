# config.py

TITULO = "📊 Compras Insight AI"

SUBTITULO = "Assistente Inteligente para o Setor de Compras"

ICONE = "📊"

# config.py

from pathlib import Path

# ==================================================
# INTERFACE
# ==================================================

TITULO = "📊 Compras Insight AI"

SUBTITULO = "Assistente Inteligente para o Setor de Compras"

ICONE = "📊"

# ==================================================
# EMPRESA
# ==================================================

EMPRESA = "Laticínio Stefanello"

VERSAO = "1.0"

# ==================================================
# BASE DE DADOS
# ==================================================

# Exemplo (vamos alterar depois para o caminho real da rede)
CAMINHO_PLANILHA_COMPRAS = r"C:\Compras\Base_Compras.xlsx"

AUTO_ATUALIZAR = True

# ==================================================
# PASTAS
# ==================================================

PASTA_PEDIDOS = Path("pedidos")
PASTA_HISTORICO = Path("historico")
PASTA_BACKUP = Path("backup")

# Cria as pastas automaticamente
for pasta in [PASTA_PEDIDOS, PASTA_HISTORICO, PASTA_BACKUP]:
    pasta.mkdir(exist_ok=True)

    from pathlib import Path

# ==================================================
# BASE DE DADOS
# ==================================================

# False = utiliza upload
# True = utiliza pasta compartilhada
USAR_BASE_COMPARTILHADA = True

# Caminho da planilha oficial da empresa
CAMINHO_PLANILHA = Path(
    r"C:\Compras\Base_Compras.xlsx"
)