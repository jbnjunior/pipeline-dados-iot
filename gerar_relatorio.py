from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether
)

BASE = Path(__file__).resolve().parent
DOCS = BASE / "docs"
DOCS.mkdir(exist_ok=True)
OUTPUT = DOCS / "relatorio_final.pdf"

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name="CapaTitulo", parent=styles["Title"],
    fontName="Helvetica-Bold", fontSize=23, leading=29,
    alignment=TA_CENTER, textColor=colors.HexColor("#17365D"),
    spaceAfter=18
))
styles.add(ParagraphStyle(
    name="Subtitulo", parent=styles["Normal"],
    fontSize=12, leading=18, alignment=TA_CENTER,
    textColor=colors.HexColor("#526579")
))
styles.add(ParagraphStyle(
    name="Secao", parent=styles["Heading1"],
    fontSize=16, leading=20, textColor=colors.HexColor("#17365D"),
    spaceBefore=12, spaceAfter=8
))
styles.add(ParagraphStyle(
    name="Subsecao", parent=styles["Heading2"],
    fontSize=12, leading=15, textColor=colors.HexColor("#24527A"),
    spaceBefore=8, spaceAfter=5
))
styles.add(ParagraphStyle(
    name="TextoRelatorio", parent=styles["BodyText"],
    fontSize=9.5, leading=14, spaceAfter=7
))
styles.add(ParagraphStyle(
    name="Legenda", parent=styles["BodyText"],
    fontSize=8, leading=11, textColor=colors.HexColor("#526579")
))

def P(text, style="TextoRelatorio"):
    return Paragraph(text, styles[style])

def rodape(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#D7E0EA"))
    canvas.line(2*cm, 1.55*cm, A4[0]-2*cm, 1.55*cm)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#526579"))
    canvas.drawString(2*cm, 1.1*cm, "Pipeline de Dados com IoT e Docker")
    canvas.drawRightString(A4[0]-2*cm, 1.1*cm, f"Página {doc.page}")
    canvas.restoreState()

doc = SimpleDocTemplate(
    str(OUTPUT), pagesize=A4,
    rightMargin=2*cm, leftMargin=2*cm,
    topMargin=2*cm, bottomMargin=2*cm,
    title="Pipeline de Dados com IoT e Docker",
    author="Projeto acadêmico"
)

story = []

# Capa
story += [
    Spacer(1, 3.2*cm),
    P("RELATÓRIO TÉCNICO", "Subtitulo"),
    Spacer(1, 0.5*cm),
    P("Pipeline de Dados<br/>com IoT e Docker", "CapaTitulo"),
    Spacer(1, 0.4*cm),
    P("Ingestão, armazenamento, consultas SQL e visualização de dados de temperatura",
      "Subtitulo"),
    Spacer(1, 2.0*cm),
    P("<b>Tecnologias:</b> Python, PostgreSQL, Docker, SQL e Streamlit",
      "Subtitulo"),
    Spacer(1, 0.5*cm),
    P("Dataset: Temperature Readings of IoT Devices", "Subtitulo"),
    Spacer(1, 4.5*cm),
    P("Relatório elaborado a partir dos testes executados no projeto.",
      "Legenda"),
    PageBreak()
]

story += [
    P("1. Introdução", "Secao"),
    P(
        "Este projeto implementa um pipeline de dados para processar leituras de "
        "temperatura disponibilizadas em arquivo CSV, armazená-las em um banco "
        "PostgreSQL executado em contêiner Docker e disponibilizar consultas "
        "analíticas por meio de views SQL. Um dashboard desenvolvido com Streamlit "
        "permite explorar visualmente os dados."
    ),
    P("2. Objetivos", "Secao"),
    P(
        "O objetivo é demonstrar uma sequência integrada de ingestão, persistência, "
        "transformação e visualização de dados. A solução utiliza ferramentas "
        "reproduzíveis em ambiente local e separa o código de ingestão, as consultas "
        "SQL e a camada de apresentação."
    ),
    P("3. Tecnologias utilizadas", "Secao")
]

tech = [
    ["Tecnologia", "Função no projeto"],
    ["Python", "Implementação do processo de ingestão e integração com o banco."],
    ["Docker Compose", "Inicialização e gerenciamento do contêiner do PostgreSQL."],
    ["PostgreSQL 16", "Armazenamento relacional das leituras de temperatura."],
    ["SQL", "Criação de views para sumarização e análise dos dados."],
    ["Streamlit", "Aplicação web para apresentação dos indicadores e gráficos."],
    ["Plotly", "Visualizações interativas no dashboard."]
]
t = Table(tech, colWidths=[4.0*cm, 11.0*cm], repeatRows=1)
t.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#17365D")),
    ("TEXTCOLOR", (0,0), (-1,0), colors.white),
    ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTNAME", (0,1), (-1,-1), "Helvetica"),
    ("FONTSIZE", (0,0), (-1,-1), 8.5),
    ("LEADING", (0,0), (-1,-1), 12),
    ("GRID", (0,0), (-1,-1), 0.4, colors.HexColor("#D7E0EA")),
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("ROWBACKGROUNDS", (0,1), (-1,-1),
     [colors.white, colors.HexColor("#F3F6FA")]),
    ("LEFTPADDING", (0,0), (-1,-1), 7),
    ("RIGHTPADDING", (0,0), (-1,-1), 7),
    ("TOPPADDING", (0,0), (-1,-1), 6),
    ("BOTTOMPADDING", (0,0), (-1,-1), 6),
]))
story += [t, Spacer(1, 10), P("4. Dataset e processamento", "Secao")]

story += [
    P(
        "Foi utilizado o arquivo <b>IOT-temp.csv</b>, obtido do conjunto de dados "
        "Temperature Readings of IoT Devices. O arquivo contém campos relacionados "
        "ao identificador da leitura, ambiente, data/hora, temperatura e indicação "
        "de entrada/saída. O script de ingestão valida e processa os registros antes "
        "de gravá-los no banco."
    ),
    P(
        "Durante a execução registrada, o processo informou <b>35.537 linhas válidas</b> "
        "processadas e armazenadas no PostgreSQL. Esse número representa os registros "
        "aceitos pelo pipeline, não necessariamente todas as linhas do CSV original."
    ),
    P("5. Arquitetura e fluxo de execução", "Secao"),
    P(
        "<b>CSV → script Python de ingestão → PostgreSQL em Docker → views SQL → "
        "dashboard Streamlit/Plotly.</b> O Docker Compose descreve o serviço do banco "
        "e facilita iniciar o ambiente local. O módulo de ingestão realiza a leitura "
        "e a preparação dos dados; as views disponibilizam agregações para consulta."
    ),
    P("6. Banco de dados e resultados", "Secao")
]

results = [
    ["Indicador verificado", "Resultado observado"],
    ["Tabela de leituras", "temperature_readings"],
    ["Registros no PostgreSQL", "35.537"],
    ["Views SQL criadas", "4"],
    ["Primeira leitura registrada", "28/07/2018 07:06"],
    ["Última leitura registrada", "08/12/2018 09:30"],
    ["Ambiente identificado", "Room Admin"],
    ["Temperatura média observada", "36,62"],
    ["Temperatura mínima observada", "21,00"],
    ["Temperatura máxima observada", "51,00"],
]
t2 = Table(results, colWidths=[7.0*cm, 8.0*cm], repeatRows=1)
t2.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#17365D")),
    ("TEXTCOLOR", (0,0), (-1,0), colors.white),
    ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE", (0,0), (-1,-1), 8.5),
    ("GRID", (0,0), (-1,-1), 0.4, colors.HexColor("#D7E0EA")),
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("ROWBACKGROUNDS", (0,1), (-1,-1),
     [colors.white, colors.HexColor("#F3F6FA")]),
    ("LEFTPADDING", (0,0), (-1,-1), 7),
    ("TOPPADDING", (0,0), (-1,-1), 6),
    ("BOTTOMPADDING", (0,0), (-1,-1), 6),
]))
story += [
    t2,
    Spacer(1, 8),
    P(
        "Observação: o campo utilizado como ambiente apresenta o valor “Room Admin” "
        "nos dados processados. Portanto, este relatório não interpreta esse campo "
        "como evidência de múltiplos dispositivos físicos."
    ),
    P("7. Views SQL", "Secao"),
    P("<b>avg_temp_por_dispositivo:</b> resume a temperatura média, mínima e máxima "
      "e a quantidade de leituras por valor identificado no campo de agrupamento."),
    P("<b>leituras_por_hora:</b> organiza as leituras por hora para permitir análise "
      "da distribuição temporal."),
    P("<b>temp_max_min_por_dia:</b> apresenta temperaturas máxima e mínima por dia."),
    P("<b>resumo_dataset:</b> apresenta indicadores gerais, incluindo total de leituras "
      "e intervalo temporal disponível."),
    P("8. Dashboard", "Secao"),
    P(
        "A aplicação Streamlit apresenta gráficos para facilitar a exploração dos dados "
        "e oferece uma camada visual sobre as informações consultadas no PostgreSQL. "
        "As capturas de tela do ambiente de execução devem ser mantidas na pasta "
        "<b>screenshots/</b> do projeto como evidências complementares."
    ),
    P("9. Limitações", "Secao"),
    P(
        "Os resultados refletem o subconjunto de registros aceitos pelo processo de "
        "ingestão. A identificação de ambiente disponível no conjunto processado não "
        "permite concluir que existam vários sensores ou dispositivos independentes. "
        "Além disso, os dados analisados são históricos e não representam, por si só, "
        "uma transmissão IoT em tempo real."
    ),
    P("10. Conclusão", "Secao"),
    P(
        "O projeto demonstra um fluxo funcional de dados desde um arquivo CSV até o "
        "armazenamento relacional e a visualização analítica. A execução validou a "
        "inserção de 35.537 registros e a criação de quatro views SQL. A integração "
        "entre Python, PostgreSQL, Docker e Streamlit constitui uma base para ampliar "
        "o pipeline com validações adicionais, novos indicadores e fontes de dados "
        "contínuas."
    ),
    P("11. Estrutura do projeto", "Secao"),
    P(
        "<b>src/</b>: módulos Python de banco de dados e ingestão.<br/>"
        "<b>sql/views.sql</b>: definições das views analíticas.<br/>"
        "<b>dashboard.py</b>: aplicação Streamlit.<br/>"
        "<b>docker-compose.yml</b>: configuração do serviço PostgreSQL.<br/>"
        "<b>data/</b>: diretório local do dataset, excluído do versionamento.<br/>"
        "<b>screenshots/</b>: evidências visuais da execução.<br/>"
        "<b>docs/</b>: documentação e relatório final."
    ),
        Spacer(1, 10),
    P("Identificação acadêmica", "Subsecao"),
    P("<b>Aluno:</b> Juarez Barra Nova Junior", "Legenda"),
    P("<b>Curso:</b> Análise e Desenvolvimento de Sistemas", "Legenda"),
    P("<b>Disciplina:</b> Disruptive Architectures: IoT, Big Data e IA", "Legenda"),
]

doc.build(story, onFirstPage=rodape, onLaterPages=rodape)
print(f"Relatório criado: {OUTPUT}")
print(f"Tamanho: {OUTPUT.stat().st_size:,} bytes")
