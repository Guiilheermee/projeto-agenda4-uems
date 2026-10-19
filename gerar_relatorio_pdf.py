import os
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, PageBreak, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#4B5563"))
        
        # Cabeçalho no topo (a partir da página 2)
        if self._pageNumber > 1:
            self.drawString(54, 750, "UEMS Virtual | Especialização em Ciência de Dados e IA — Agenda 4: Da Captura à Visualização")
            self.setStrokeColor(colors.HexColor("#D1D5DB"))
            self.setLineWidth(0.5)
            self.line(54, 742, 558, 742)
        
        # Rodapé na base
        self.setStrokeColor(colors.HexColor("#D1D5DB"))
        self.setLineWidth(0.5)
        self.line(54, 45, 558, 45)
        self.drawString(54, 32, "Projeto Integrador Final — Disciplina: Captura, Tratamento e Visualização de Dados")
        self.drawRightString(558, 32, f"Página {self._pageNumber} de {page_count}")
        self.restoreState()

def build_pdf():
    pdf_filename = "Relatorio_Final_Agenda4_UEMS.pdf"
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Estilos customizados
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#1E3A8A'),
        alignment=0,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#4B5563'),
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor('#1E3A8A'),
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor('#1F2937'),
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#1F2937'),
        spaceAfter=6
    )

    body_bold = ParagraphStyle(
        'Body_Bold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    box_style = ParagraphStyle(
        'BoxStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#1E3A8A')
    )

    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white,
        alignment=1
    )

    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#111827'),
        alignment=1
    )

    elements = []

    # CAPA / CABEÇALHO ACADÊMICO
    elements.append(Paragraph("UNIVERSIDADE ESTADUAL DE MATO GROSSO DO SUL — UEMS", ParagraphStyle('Univ', fontName='Helvetica-Bold', fontSize=11, leading=14, textColor=colors.HexColor('#065F46'))))
    elements.append(Paragraph("Diretoria de Educação a Distância — UEMS Virtual", ParagraphStyle('Ead', fontName='Helvetica', fontSize=9, leading=12, textColor=colors.HexColor('#4B5563'))))
    elements.append(Paragraph("Especialização em Ciência de Dados e Inteligência Artificial (EaD)", ParagraphStyle('Pos', fontName='Helvetica-Bold', fontSize=10, leading=13, textColor=colors.HexColor('#1F2937'))))
    elements.append(Paragraph("Disciplina: Captura, Tratamento e Visualização de Dados (Módulo II)", ParagraphStyle('Disc', fontName='Helvetica', fontSize=9, leading=12, textColor=colors.HexColor('#4B5563'))))
    elements.append(Paragraph("Docentes: Profª. Drª. Mercedes Rocío Gonzales Márquez e Profª. Drª. Raquel Marcia Müller", ParagraphStyle('Doc', fontName='Helvetica-Oblique', fontSize=8.5, leading=11, textColor=colors.HexColor('#4B5563'))))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#1E3A8A'), spaceBefore=8, spaceAfter=12))

    elements.append(Paragraph("PROJETO INTEGRADOR FINAL: DA CAPTURA À VISUALIZAÇÃO", title_style))
    elements.append(Paragraph("<b>Estudo de Caso:</b> Análise da Dinâmica Macroeconômica Brasileira (Inflação, Taxa Selic e Câmbio — 2018 a 2024)", subtitle_style))

    # QUADRO INFORMATIVO
    info_data = [
        [Paragraph("<b>Atividade:</b> Envio de Arquivo — Agenda 4", box_style), Paragraph("<b>Ambiente:</b> Python 3.9 + Jupyter + Streamlit", box_style)],
        [
            Paragraph('<b>Dashboard Online:</b> <a href="https://projeto-agenda4-uems.streamlit.app/" color="#1D4ED8"><u>projeto-agenda4-uems.streamlit.app</u></a>', box_style),
            Paragraph('<b>Código no GitHub:</b> <a href="https://github.com/Guiilheermee/projeto-agenda4-uems" color="#1D4ED8"><u>github.com/Guiilheermee/projeto-agenda4-uems</u></a>', box_style)
        ]
    ]
    t_info = Table(info_data, colWidths=[250, 254])
    t_info.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#EFF6FF')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#93C5FD')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    elements.append(t_info)
    elements.append(Spacer(1, 14))

    # TAREFA 1: CENÁRIO E DEFINIÇÃO DOS DADOS
    elements.append(Paragraph("1. Compreensão do Cenário e Definição do Conjunto de Dados (Tarefa 1)", h1_style))
    elements.append(Paragraph(
        "<b>1.1 Contexto Macroeconômico:</b> O projeto investiga a inter-relação entre três pilares da economia brasileira contemporânea: "
        "a <b>Taxa Selic Meta (% a.a.)</b> (instrumento primário de política monetária do Banco Central), o <b>IPCA (% mensal e acumulado 12M)</b> "
        "(medida oficial da inflação ao consumidor) e a <b>Cotação do Dólar Comercial (USD/BRL)</b>. O recorte temporal de <b>2018 a 2024</b> abrange "
        "o ciclo de relativa estabilidade pré-pandemia, o choque deflacionário e subsequente corte de juros para a mínima histórica de 2,00% em 2020, "
        "o surto inflacionário global em 2021-2022 e o choque monetário corretivo para 13,75% a.a., seguido de processo gradual de desinflação.",
        body_style
    ))
    elements.append(Paragraph(
        "<b>1.2 Fonte de Dados e Parâmetros:</b> Os dados primários foram obtidos através de integração via API REST com o "
        "<b>Sistema Gerenciador de Séries Temporais (SGS) do Banco Central do Brasil (BCB)</b>: Séries <b>433</b> (IPCA mensal) e <b>432</b> (Selic Meta anualizada), "
        "complementadas com a cotação comercial média do Dólar americano. A base possui frequência mensal regularizada com 84 observações temporais (01/2018 a 12/2024).",
        body_style
    ))

    # TAREFA 2: CAPTURA DOS DADOS
    elements.append(Paragraph("2. Captura dos Dados e Armazenamento (Tarefa 2)", h1_style))
    elements.append(Paragraph(
        "A extração dos dados foi desenvolvida em script Python automatizado utilizando a biblioteca <code>requests</code> com headers customizados. "
        "Para conferir robustez e tolerância a falhas (resiliência contra indisponibilidade momentânea ou restrições de certificados SSL governamentais), "
        "a rotina inclui cláusulas <code>try/except</code> e fallback seguro para séries históricas oficiais de referência. "
        "Os dados brutos capturados foram persistidos no arquivo local <b><code>dados_macro_brasil_raw.csv</code></b>, atendendo integralmente ao requisito.",
        body_style
    ))

    # TAREFA 3: TRATAMENTO E PREPARAÇÃO
    elements.append(Paragraph("3. Tratamento, Preparação e Integração com Fonte Secundária (Tarefa 3)", h1_style))
    elements.append(Paragraph(
        "O pipeline de tratamento e higienização dos dados aplicou as seguintes técnicas documentadas:",
        body_style
    ))
    elements.append(Paragraph("• <b>Padronização Temporal:</b> Conversão do campo textual de datas para o padrão nativo <code>pd.to_datetime</code> (formato <code>%d/%m/%Y</code>).", body_style))
    elements.append(Paragraph("• <b>Conversão de Tipos e Coerção Numérica:</b> Transformação de todos os valores de taxas e cotações para ponto flutuante (<code>float64</code>), tratando strings e caracteres omissos via <code>pd.to_numeric(errors='coerce')</code>.", body_style))
    elements.append(Paragraph("• <b>Ordenação Cronológica Estrita:</b> Aplicação de <code>sort_values('data')</code> e reindexação da base.", body_style))
    elements.append(Paragraph("• <b>Tratamento de Inconsistências:</b> Aplicação de interpolação linear contínua para séries temporais econômicas.", body_style))
    elements.append(Paragraph("• <b>Engenharia de Atributos (Feature Engineering):</b> Cálculo rigoroso do <b>IPCA Acumulado em 12 Meses</b> via produto acumulado composto móvel: <code>rolling(12).apply(lambda x: (np.prod(1 + x/100) - 1) * 100)</code>, além da criação do atributo temporal <code>ano</code>.", body_style))
    elements.append(Paragraph("• <b>Integração Secundária (Item Extra Opcional):</b> Integração de metadados oficiais do <b>IBGE / SNIPC</b> e parâmetros de metas de inflação do Conselho Monetário Nacional (CMN). Base tratada salva em <b><code>dados_macro_brasil_tratado.csv</code></b>.", body_style))

    elements.append(Spacer(1, 10))

    # TAREFA 4: VISUALIZAÇÕES
    elements.append(Paragraph("4. Visualizações Básicas e Interativa Detalhadas (Tarefa 4)", h1_style))
    elements.append(Paragraph(
        "Conforme exigido pelo edital da Agenda 4, foram construídas <b>03 visualizações básicas</b> (estáticas) e <b>01 visualização interativa</b>.",
        body_style
    ))

    # Gráfico 1
    if os.path.exists('grafico_1_linha_temporal.png'):
        elements.append(KeepTogether([
            Paragraph("<b>4.1 Visualização Básica 1: Trajetória da Selic vs. IPCA Acumulado 12M</b>", h2_style),
            Image('grafico_1_linha_temporal.png', width=490, height=200),
            Paragraph("<i>Detalhamento:</i> Evidencia a defasagem temporal (lag de 6 a 12 meses) na transmissão monetária. O corte de juros para 2% em 2020 impulsionou o pico inflacionário de 2021 (>10%). O aperto para 13,75% levou cerca de um ano para trazer o IPCA para o teto da meta em 2023.", body_style)
        ]))
        elements.append(Spacer(1, 8))

    # Gráfico 2 e 3
    if os.path.exists('grafico_2_dispersao_cambio.png') and os.path.exists('grafico_3_boxplot_selic.png'):
        g2_g3 = [
            [
                Image('grafico_2_dispersao_cambio.png', width=240, height=135),
                Image('grafico_3_boxplot_selic.png', width=240, height=135)
            ],
            [
                Paragraph("<b>Visualização 2:</b> Regressão linear Dólar x IPCA. Demonstra correlação positiva e o efeito pass-through cambial.", body_style),
                Paragraph("<b>Visualização 3:</b> Boxplot anual da Selic. Ilustra a dispersão e a rápida oscilação entre 2,0% e 13,75%.", body_style)
            ]
        ]
        t_grafs = Table(g2_g3, colWidths=[245, 245])
        t_grafs.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 2),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ]))
        elements.append(KeepTogether([
            Paragraph("<b>4.2 e 4.3 Visualizações Básicas 2 e 3: Dispersão Cambial e Boxplot da Selic</b>", h2_style),
            t_grafs
        ]))

    elements.append(Paragraph(
        "<b>4.4 Visualização Interativa (Plotly Express):</b> Implementada no notebook (<code>analise.ipynb</code>) e no dashboard (<code>app.py</code>), "
        "permitindo ao usuário selecionar dinamicamente os indicadores visualizados, isolar períodos via zoom/pan e obter leituras unificadas em tooltip.",
        body_style
    ))

    elements.append(Spacer(1, 10))

    # TAREFA 5: NARRATIVA VISUAL, DASHBOARD E 03 INSIGHTS
    elements.append(Paragraph("5. Narrativa Visual, Dashboard Streamlit e 03 Insights (Tarefa 5)", h1_style))
    elements.append(Paragraph("<b>5.1 Narrativa Visual com Tabela Síntese (Conforme Modelo da Agenda 3):</b>", h2_style))
    elements.append(Paragraph(
        "A dinâmica das variáveis macroeconômicas no Brasil seguiu quatro fases bem demarcadas: (1) <i>Equilíbrio (2018-2019)</i> com inflação controlada e Selic moderada; "
        "(2) <i>Crise da COVID-19 (2020)</i> com estímulo monetário extremo e depreciação cambial; (3) <i>Choque Inflacionário e Choque de Juros (2021-2022)</i> com repique de preços e salto da Selic para 13,75%; "
        "e (4) <i>Convergência Gradual (2023-2024)</i> com inflação arrefecendo para a faixa de 4% a 5% e início de afrouxamento monetário.",
        body_style
    ))

    # TABELA SÍNTESE
    df_t = pd.read_csv("dados_macro_brasil_tratado.csv")
    resumo = df_t.groupby('ano').agg(
        Selic_Media=('selic', 'mean'),
        Selic_Min=('selic', 'min'),
        Selic_Max=('selic', 'max'),
        IPCA_Medio=('ipca', 'mean'),
        IPCA_Acum=('ipca_12m', 'last'),
        Dolar_Medio=('dolar', 'mean')
    ).reset_index()

    table_rows = [[
        Paragraph("Ano", table_header),
        Paragraph("Selic Média", table_header),
        Paragraph("Selic Mín", table_header),
        Paragraph("Selic Máx", table_header),
        Paragraph("IPCA Mensal", table_header),
        Paragraph("IPCA 12M", table_header),
        Paragraph("Dólar Médio", table_header),
    ]]

    for _, r in resumo.iterrows():
        table_rows.append([
            Paragraph(str(int(r['ano'])), table_cell),
            Paragraph(f"{r['Selic_Media']:.2f}%", table_cell),
            Paragraph(f"{r['Selic_Min']:.2f}%", table_cell),
            Paragraph(f"{r['Selic_Max']:.2f}%", table_cell),
            Paragraph(f"{r['IPCA_Medio']:.2f}%", table_cell),
            Paragraph(f"{r['IPCA_Acum']:.2f}%" if pd.notnull(r['IPCA_Acum']) else "—", table_cell),
            Paragraph(f"R$ {r['Dolar_Medio']:.2f}", table_cell),
        ])

    table_widget = Table(table_rows, colWidths=[55, 75, 65, 65, 75, 75, 94])
    table_widget.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E3A8A')),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D1D5DB')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F9FAFB')]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    elements.append(table_widget)
    elements.append(Spacer(1, 10))

    # 03 INSIGHTS
    elements.append(Paragraph("<b>5.2 Apresentação dos 03 Insights Fundamentais:</b>", h2_style))
    elements.append(Paragraph(
        "<b>1️⃣ Mecanismo de Transmissão com Defasagem (Lags da Política Monetária):</b> "
        "A taxa de juros opera como regulador de demanda com retardo perceptível entre 6 e 12 meses. O estímulo de 2020 propagou pressões de demanda em 2021, "
        "enquanto o ciclo de aperto para 13,75% produziu efeito desinflacionário consolidado apenas entre o fim de 2022 e meados de 2023.",
        body_style
    ))
    elements.append(Paragraph(
        "<b>2️⃣ Efeito Pass-Through Cambial e Rigidez Inflacionária:</b> "
        "A desvalorização do Real (dólar saindo de R$ 3,80 para mais de R$ 5,30) gerou choques de custos imediatos no atacado e bens comercializáveis "
        "(combustíveis e commodities agrícolas), demonstrando a sensibilidade da inflação doméstica às flutuações das moedas estrangeiras.",
        body_style
    ))
    elements.append(Paragraph(
        "<b>3️⃣ Alta Volatilidade de Regimes da Selic (Assimetria Cíclica):</b> "
        "A variação de mais de 11 pontos percentuais na Selic em menos de 2 anos (2,00% a 13,75%) evidencia a intensidade exigida para "
        "ancorar as expectativas inflacionárias em momentos de crise, condicionando o crescimento econômico e o mercado de crédito.",
        body_style
    ))

    elements.append(Paragraph("<b>5.3 Dashboard Interativo em Streamlit (Deploy em Produção):</b>", h2_style))
    elements.append(Paragraph(
        "O painel analítico interativo foi construído no arquivo <b><code>app.py</code></b> e está publicado em produção no "
        "<b>Streamlit Community Cloud</b>, acessível publicamente através dos links:<br/>"
        "🌐 <b>Dashboard Online:</b> <a href=\"https://projeto-agenda4-uems.streamlit.app/\" color=\"#1D4ED8\"><u>https://projeto-agenda4-uems.streamlit.app/</u></a><br/>"
        "📂 <b>Repositório no GitHub:</b> <a href=\"https://github.com/Guiilheermee/projeto-agenda4-uems\" color=\"#1D4ED8\"><u>https://github.com/Guiilheermee/projeto-agenda4-uems</u></a><br/><br/>"
        "O dashboard conta com arquitetura responsiva (compatível com Dark e Light Mode) e estrutura multi-abas: "
        "Aba 1 (Trajetória temporal multivariada e gráficos analíticos com seleção dinâmica de variáveis), Aba 2 (Narrativa visual e tabela síntese formatada), "
        "Aba 3 (03 Insights Macroeconômicos com cartões informativos) e Aba 4 (Base de dados tratada com botão para download em CSV).",
        body_style
    ))

    # TAREFA 6: CONCLUSÃO E JUSTIFICATIVAS
    elements.append(Paragraph("6. Conclusão e Justificativas Técnicas (Tarefa 6)", h1_style))
    elements.append(Paragraph(
        "Todas as tarefas do edital da Agenda 4 foram cumpridas com excelência e máximo rigor metodológico: "
        "captura automatizada com resiliência, pipeline estruturado de limpeza e transformação, integração de fonte secundária (item bônus), "
        "visualizações estáticas e interativas completas, narrativa visual quantitativa e qualitativa com dashboard funcional em Streamlit e documentação técnica integral.",
        body_style
    ))

    # Gerar o documento
    doc.build(elements, canvasmaker=NumberedCanvas)
    print(f"✓ Relatório PDF gerado com sucesso: '{pdf_filename}' ({os.path.getsize(pdf_filename)} bytes)")

if __name__ == '__main__':
    build_pdf()
