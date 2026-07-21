from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    Image
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import cm

from datetime import datetime
import os

from utils import (
    formatar_moeda,
    formatar_numero
)

# ===========================================================
# CORES
# ===========================================================

AZUL = colors.HexColor("#34377A")
LARANJA = colors.HexColor("#E68A13")
VERMELHO = colors.HexColor("#D62828")
VERDE = colors.HexColor("#2A9D8F")
CINZA = colors.HexColor("#F4F4F4")


# ===========================================================
# PDF
# ===========================================================

def gerar_pdf(comparativo, compras):

    pasta = "relatorios"
    os.makedirs(pasta, exist_ok=True)

    agora = datetime.now()

    numero_relatorio = agora.strftime("%Y%m%d%H%M%S")

    nome_pdf = os.path.join(
        pasta,
        f"Relatorio_Sugestao_Compras_{numero_relatorio}.pdf"
    )

    doc = SimpleDocTemplate(
        nome_pdf,
        rightMargin=1.5 * cm,
        leftMargin=1.5 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm
    )

    estilos = getSampleStyleSheet()

    titulo = estilos["Title"]
    titulo.alignment = TA_CENTER

    subtitulo = estilos["Heading2"]
    subtitulo.alignment = TA_CENTER

    normal = estilos["BodyText"]

    elementos = []

    # =======================================================
    # LOGO
    # =======================================================

    logo = "app/imagens/logo.png"

    if os.path.exists(logo):

        img = Image(
            logo,
            width=5 * cm,
            height=2.2 * cm
        )

        img.hAlign = "CENTER"

        elementos.append(img)

    elementos.append(
        Spacer(1, 0.4 * cm)
    )

    # =======================================================
    # CABEÇALHO
    # =======================================================

    elementos.append(
        Paragraph(
            "Laticínios Stefanello",
            titulo
        )
    )

    elementos.append(
        Paragraph(
            "Compras Insight AI",
            subtitulo
        )
    )

    elementos.append(
        Paragraph(
            "<b>RELATÓRIO DE SUGESTÃO INTELIGENTE DE COMPRAS</b>",
            titulo
        )
    )

    elementos.append(
        Spacer(1, 0.5 * cm)
    )

    elementos.append(
        Paragraph(
            f"<b>Data:</b> {agora.strftime('%d/%m/%Y')}",
            normal
        )
    )

    elementos.append(
        Paragraph(
            f"<b>Hora:</b> {agora.strftime('%H:%M:%S')}",
            normal
        )
    )

    elementos.append(
        Paragraph(
            f"<b>Relatório Nº:</b> {numero_relatorio}",
            normal
        )
    )

    if "Data" in compras.columns:

        inicio = compras["Data"].min()
        fim = compras["Data"].max()

        elementos.append(
            Paragraph(
                f"<b>Período analisado:</b> "
                f"{inicio.strftime('%d/%m/%Y')} até "
                f"{fim.strftime('%d/%m/%Y')}",
                normal
            )
        )

    elementos.append(
        Spacer(1, 0.6 * cm)
    )

    # =======================================================
    # PREPARAÇÃO DOS DADOS
    # =======================================================

    dados = comparativo.copy()

    chave = (
        "Item_Normalizado"
        if "Item_Normalizado" in compras.columns
        else "Item"
    )

    compras = compras.copy()

    compras["Preço Médio"] = (
        compras["Custo total"] /
        compras["Quantidade"].replace(0, 1)
    )

    preco = (
        compras.groupby(chave)["Preço Médio"]
        .mean()
    )

    fornecedor = (
        compras.groupby(chave)["Fornecedor"]
        .agg(
            lambda x:
            x.mode().iloc[0]
            if not x.mode().empty
            else "Fornecedor não localizado"
        )
    )

    if "Preço Médio" not in dados.columns:

        if chave in dados.columns:

            dados["Preço Médio"] = dados[
                chave
            ].map(preco)

        else:

            dados["Preço Médio"] = dados[
                "Item"
            ].map(preco)

    if "Fornecedor" not in dados.columns:

        if chave in dados.columns:

            dados["Fornecedor"] = dados[
                chave
            ].map(fornecedor)

        else:

            dados["Fornecedor"] = dados[
                "Item"
            ].map(fornecedor)

    dados["Fornecedor"] = dados[
        "Fornecedor"
    ].fillna("Fornecedor não localizado")

    dados["Preço Médio"] = dados[
        "Preço Médio"
    ].fillna(0)

    # =======================================================
    # UTILIZA A NOVA LÓGICA
    # =======================================================

    dados["Quantidade Recomendada"] = dados["Comprar"]

    dados["Valor Estimado"] = (

        dados["Quantidade Recomendada"]

        *

        dados["Preço Médio"]

    )

    # =======================================================
    # PRIORIDADES
    # =======================================================

    alta = dados[
        dados["Em estoque"] == 0
    ].copy()

    media = dados[
        (
            dados["Em estoque"] > 0
        )
        &
        (
            dados["Em estoque"]
            <=
            dados["Estoque mínimo"]
        )
    ].copy()

    baixa = dados[
        dados["Comprar"] > 0
    ].copy()

    # =======================================================
    # FUNÇÕES AUXILIARES
    # =======================================================

    def moeda(valor):
        return formatar_moeda(valor)

    def numero(valor):
        return formatar_numero(valor)
    
        # =======================================================
    # GERA TABELAS
    # =======================================================

    def adicionar_prioridade(
        titulo_secao,
        cor,
        tabela
    ):

        tabela = tabela[
            tabela["Quantidade Recomendada"] > 0
        ].copy()

        if tabela.empty:
            return

        elementos.append(
            Paragraph(
                f"<font color='{cor.hexval()}'><b>{titulo_secao}</b></font>",
                estilos["Heading2"]
            )
        )

        dados_tabela = [[
            "Produto",
            "Estoque",
            "Mín.",
            "Desej.",
            "Comprar",
            "Un.",
            "Fornecedor",
            "Valor Est."
        ]]

        tabela = tabela.sort_values(
            "Valor Estimado",
            ascending=False
        )

        for _, linha in tabela.iterrows():

            dados_tabela.append([

                Paragraph(
                    str(linha["Item"]),
                    normal
                ),

                numero(
                    linha["Em estoque"]
                ),

                numero(
                    linha["Estoque mínimo"]
                ),

                numero(
                    linha["Estoque desejável"]
                ),

                numero(
                    linha["Quantidade Recomendada"]
                ),

                str(
                    linha["Unidade"]
                ),

                Paragraph(
                    str(linha["Fornecedor"]),
                    normal
                ),

                moeda(
                    linha["Valor Estimado"]
                )

            ])

        larguras = [

            5.6 * cm,
            1.8 * cm,
            1.8 * cm,
            2.0 * cm,
            2.0 * cm,
            1.2 * cm,
            4.0 * cm,
            2.8 * cm

        ]

        relatorio = Table(
            dados_tabela,
            colWidths=larguras,
            repeatRows=1
        )

        relatorio.setStyle(

            TableStyle([

                ("BACKGROUND", (0, 0), (-1, 0), cor),

                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

                ("FONTSIZE", (0, 0), (-1, 0), 9),

                ("BOTTOMPADDING", (0, 0), (-1, 0), 8),

                ("TOPPADDING", (0, 0), (-1, 0), 8),

                ("GRID", (0, 0), (-1, -1), 0.35, colors.grey),

                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [colors.white, CINZA]
                ),

                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

                ("ALIGN", (1, 1), (-1, -1), "CENTER"),

                ("BOTTOMPADDING", (0, 1), (-1, -1), 6),

                ("TOPPADDING", (0, 1), (-1, -1), 6)

            ])

        )

        elementos.append(relatorio)

        elementos.append(
            Spacer(1, 0.5 * cm)
        )

    # =======================================================
    # SEÇÕES DO RELATÓRIO
    # =======================================================

    adicionar_prioridade(
        "🔴 ESTOQUE ZERADO",
        VERMELHO,
        alta
    )

    adicionar_prioridade(
        "🟠 ABAIXO DO ESTOQUE MÍNIMO",
        LARANJA,
        media
    )

    adicionar_prioridade(
        "🟢 REPOSIÇÃO PROGRAMADA",
        VERDE,
        baixa
    )
        # =======================================================
    # RESUMO EXECUTIVO
    # =======================================================

    total_produtos = len(
        dados[dados["Quantidade Recomendada"] > 0]
    )

    total_quantidade = dados[
        "Quantidade Recomendada"
    ].sum()

    total_estimado = dados[
        "Valor Estimado"
    ].sum()

    estoque_zerado = (
        dados["Em estoque"] == 0
    ).sum()

    abaixo_minimo = (
        (
            dados["Em estoque"] > 0
        )
        &
        (
            dados["Em estoque"]
            <=
            dados["Estoque mínimo"]
        )
    ).sum()

    estoque_ok = (
        dados["Em estoque"]
        >
        dados["Estoque mínimo"]
    ).sum()

    elementos.append(
        Spacer(1, 0.5 * cm)
    )

    elementos.append(
        Paragraph(
            "<b>Resumo Executivo</b>",
            estilos["Heading2"]
        )
    )

    resumo = [

        ["Indicador", "Valor"],

        [
            "Produtos para compra",
            str(total_produtos)
        ],

        [
            "Quantidade total sugerida",
            formatar_numero(total_quantidade)
        ],

        [
            "Valor estimado",
            formatar_moeda(total_estimado)
        ],

        [
            "Produtos com estoque zerado",
            str(estoque_zerado)
        ],

        [
            "Produtos abaixo do mínimo",
            str(abaixo_minimo)
        ],

        [
            "Produtos com estoque adequado",
            str(estoque_ok)
        ]

    ]

    tabela_resumo = Table(
        resumo,
        colWidths=[9 * cm, 6 * cm]
    )

    tabela_resumo.setStyle(

        TableStyle([

            ("BACKGROUND", (0, 0), (-1, 0), AZUL),

            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

            ("GRID", (0, 0), (-1, -1), 0.35, colors.grey),

            ("BACKGROUND", (0, 1), (-1, -1), CINZA),

            ("ALIGN", (1, 1), (1, -1), "CENTER"),

            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),

            ("TOPPADDING", (0, 0), (-1, -1), 8)

        ])

    )

    elementos.append(tabela_resumo)

    elementos.append(
        Spacer(1, 0.8 * cm)
    )

    elementos.append(

        Paragraph(

            """
<b>Observações</b><br/><br/>

• Produtos classificados como <b>Estoque Zerado</b> possuem prioridade máxima de compra.<br/><br/>

• Produtos <b>Abaixo do Estoque Mínimo</b> necessitam reposição para evitar ruptura.<br/><br/>

• A quantidade sugerida busca recompor o estoque até o nível desejável cadastrado.<br/><br/>

• Este relatório foi gerado automaticamente pelo <b>Compras Insight AI</b>.
""",

            normal

        )

    )

    # =======================================================
    # RODAPÉ
    # =======================================================

    elementos.append(
        Spacer(1, 1 * cm)
    )

    elementos.append(

        Paragraph(

            f"""
<font color="#777777">
Relatório gerado em {agora.strftime("%d/%m/%Y às %H:%M:%S")}<br/>
Compras Insight AI • Laticínios Stefanello
</font>
""",

            estilos["BodyText"]

        )

    )

    # =======================================================
    # FINALIZA PDF
    # =======================================================

    doc.build(elementos)

    return nome_pdf