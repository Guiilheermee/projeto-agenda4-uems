import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Configuração da Página
st.set_page_config(
    page_title="Dashboard Macro Brasil - UEMS",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título e Subtítulo Responsivos ao Tema (Dark / Light)
st.title("📊 Painel Macroeconômico: Inflação, Juros e Câmbio")
st.caption("Projeto Integrador: Da Captura à Visualização (Agenda 4) | Pós-Graduação: Especialização em Ciência de Dados e IA — UEMS Virtual")

@st.cache_data
def load_data():
    df = pd.read_csv("dados_macro_brasil_tratado.csv")
    df['data'] = pd.to_datetime(df['data'])
    return df

df = load_data()

# Barra Lateral (Sidebar) com Informações e Filtros
st.sidebar.markdown("### 🎓 UEMS Virtual")
st.sidebar.markdown("**Especialização em Ciência de Dados e IA**")
st.sidebar.markdown("---")
st.sidebar.subheader("Configurações & Filtros")

anos_disponiveis = sorted(df['ano'].unique())
anos_selecionados = st.sidebar.multiselect(
    "📅 Selecione os Anos:",
    options=anos_disponiveis,
    default=anos_disponiveis
)

if not anos_selecionados:
    st.warning("⚠️ Por favor, selecione ao menos um ano no menu lateral para visualizar as informações.")
    st.stop()

# Filtragem dos dados
df_view = df[df['ano'].isin(anos_selecionados)].sort_values('data').copy()

st.sidebar.markdown("---")
st.sidebar.markdown("**Fontes de Dados:**")
st.sidebar.markdown("• [BCB SGS API](https://dadosabertos.bcb.gov.br/) (Séries 432 e 433)")
st.sidebar.markdown("• [IBGE / SNIPC](https://sidra.ibge.gov.br/) (Metadados Secundários)")
st.sidebar.markdown("• Período Histórico: 2018 - 2024")

# Cartões de Métricas (KPIs)
st.subheader("📌 Indicadores Econômicos no Período Selecionado")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

ult_selic = df_view['selic'].iloc[-1]
ult_dolar = df_view['dolar'].iloc[-1]
ult_ipca = df_view['ipca'].iloc[-1]
ult_ipca_12m = df_view['ipca_12m'].dropna().iloc[-1] if not df_view['ipca_12m'].dropna().empty else 0.0

with kpi1:
    st.metric("Taxa Selic Recente", f"{ult_selic:.2f}% a.a.")
with kpi2:
    st.metric("Câmbio Dólar (USD)", f"R$ {ult_dolar:.2f}")
with kpi3:
    st.metric("Último IPCA Mensal", f"{ult_ipca:.2f}%")
with kpi4:
    st.metric("IPCA Acum. 12 Meses", f"{ult_ipca_12m:.2f}%")

st.markdown("---")

# Abas Principais
tab_graficos, tab_narrativa, tab_insights, tab_dados = st.tabs([
    "📈 Visualizações Interativas", 
    "📖 Narrativa Visual (Agenda 3)", 
    "💡 03 Insights Macroeconômicos", 
    "📋 Base de Dados Tratada"
])

# ----------------- ABA 1: VISUALIZAÇÕES INTERATIVAS -----------------
with tab_graficos:
    st.subheader("1. Trajetória Temporal Comparativa dos Indicadores")
    indicadores_plot = st.multiselect(
        "Selecione as variáveis para o gráfico interativo:",
        options=['selic', 'ipca_12m', 'dolar', 'ipca'],
        default=['selic', 'ipca_12m', 'dolar'],
        format_func=lambda x: {
            'selic': 'Taxa Selic Meta (% a.a.)',
            'ipca_12m': 'IPCA Acumulado 12M (%)',
            'dolar': 'Taxa de Câmbio USD (R$)',
            'ipca': 'IPCA Mensal (%)'
        }[x]
    )

    if indicadores_plot:
        fig_interativa = px.line(
            df_view,
            x='data',
            y=indicadores_plot,
            markers=True,
            title="Evolução Temporal dos Indicadores Macroeconômicos (Brasil: 2018 - 2024)",
            labels={'value': 'Taxa (%) / Cotação (R$)', 'data': 'Data', 'variable': 'Indicador'},
            color_discrete_map={
                'selic': '#1F77B4',
                'ipca_12m': '#DC2626',
                'dolar': '#16A34A',
                'ipca': '#F59E0B'
            }
        )
        fig_interativa.update_layout(
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_interativa, use_container_width=True)
    else:
        st.info("Selecione ao menos um indicador acima para exibir o gráfico.")

    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.subheader("2. Relação Câmbio vs. IPCA Mensal")
        try:
            fig_scatter = px.scatter(
                df_view,
                x='dolar',
                y='ipca',
                trendline='ols',
                color=df_view['ano'].astype(str),
                labels={'dolar': 'Dólar Comercial (R$)', 'ipca': 'IPCA Mensal (%)', 'color': 'Ano'},
                title="Dispersão: Cotação do Dólar x Inflação Mensal"
            )
        except Exception:
            fig_scatter = px.scatter(
                df_view,
                x='dolar',
                y='ipca',
                color=df_view['ano'].astype(str),
                labels={'dolar': 'Dólar Comercial (R$)', 'ipca': 'IPCA Mensal (%)', 'color': 'Ano'},
                title="Dispersão: Cotação do Dólar x Inflação Mensal"
            )
        st.plotly_chart(fig_scatter, use_container_width=True)

    with col_g2:
        st.subheader("3. Dispersão da Selic por Ano")
        fig_box = px.box(
            df_view,
            x='ano',
            y='selic',
            color=df_view['ano'].astype(str),
            labels={'ano': 'Ano', 'selic': 'Taxa Selic (% a.a.)', 'color': 'Ano'},
            title="Distribuição da Taxa Selic por Ano (Boxplot)"
        )
        st.plotly_chart(fig_box, use_container_width=True)

# ----------------- ABA 2: NARRATIVA VISUAL -----------------
with tab_narrativa:
    st.subheader("📖 Narrativa Visual (Texto + Tabela Integrada)")
    st.markdown("""
    A dinâmica macroeconômica brasileira entre **2018 e 2024** foi marcada por ciclos extremos e contrapostos de política monetária e choques externos:
    
    1. **2018 - 2019 (Estabilidade Inicial):** Período de inflação ancorada em torno de 3,7% a 4,3% e taxa Selic em patamar moderado (6,5% a 5,0%), com câmbio em patamar acessível (R$ 3,60 a R$ 3,90).
    2. **2020 (Choque Pandêmico e Selic Mínima Histórica):** Diante da crise da COVID-19, o COPOM/BCB promoveu um corte histórico de juros, levando a Selic ao piso de **2,0% a.a.**, simultaneamente à forte desvalorização do Real (dólar superando R$ 5,00).
    3. **2021 - 2022 (Choque Inflacionário e Choque de Juros):** O descompasso nas cadeias de suprimentos globais e o câmbio depreciado geraram um surto inflacionário (IPCA acumulado superou 10% a 12%). Em resposta, o Banco Central implementou um dos apertos monetários mais agressivos do mundo, elevando a Selic de 2,0% para **13,75% a.a.**
    4. **2023 - 2024 (Desinflação e Afrouxamento Gradual):** Com a transmissão dos juros altos à economia real, a inflação refluiu para a faixa de 4,0% a 4,8%, permitindo o início do ciclo de corte da Selic até a faixa de 10,5% - 11,25%.
    """)

    st.markdown("#### 📊 Tabela Síntese: Métricas Médias Anuais")
    
    df_resumo = df_view.groupby('ano').agg(
        Selic_Media=('selic', 'mean'),
        Selic_Min=('selic', 'min'),
        Selic_Max=('selic', 'max'),
        IPCA_Mensal_Medio=('ipca', 'mean'),
        IPCA_Acum_Ano=('ipca_12m', 'last'),
        Dolar_Medio=('dolar', 'mean')
    ).reset_index()

    st.dataframe(
        df_resumo.style.format({
            'Selic_Media': '{:.2f}%',
            'Selic_Min': '{:.2f}%',
            'Selic_Max': '{:.2f}%',
            'IPCA_Mensal_Medio': '{:.2f}%',
            'IPCA_Acum_Ano': '{:.2f}%',
            'Dolar_Medio': 'R$ {:.2f}'
        }),
        use_container_width=True
    )

# ----------------- ABA 3: 03 INSIGHTS MACROECONÔMICOS -----------------
with tab_insights:
    st.subheader("💡 03 Insights Fundamentais Obtidos a Partir das Visualizações")
    
    with st.container(border=True):
        st.markdown("### 1️⃣ Mecanismo de Transmissão com Defasagem (*Lags* da Política Monetária)")
        st.markdown("""
        A elevação da taxa Selic não produz desinflação imediata. Observa-se um *lag* temporal de **6 a 12 meses** entre a subida inicial dos juros (iniciada em 2021) e o recuo consistente do IPCA 12 meses (que começou a ceder apenas no segundo semestre de 2022). A política monetária atua esfriando a demanda agregada de forma gradual.
        """)
    
    with st.container(border=True):
        st.markdown("### 2️⃣ Efeito *Pass-Through* Cambial e Inércia de Custos")
        st.markdown("""
        A taxa de câmbio atua como canal direto de transmissão de choques de oferta. Quando o dólar saltou de R$ 3,80 para mais de R$ 5,30 entre 2020 e 2021, o custo de insumos importados, combustíveis e commodities agrícolas aumentou no mercado doméstico, pressionando a inflação mesmo em um cenário de economia inicialmente retraída.
        """)
    
    with st.container(border=True):
        st.markdown("### 3️⃣ Alta Volatilidade de Regimes da Selic (Assimetria Cíclica)")
        st.markdown("""
        A amplitude da taxa Selic observada no período (de 2,00% em 2020 a 13,75% em 2022) evidencia um perfil de reação acentuado da autoridade monetária para restaurar a credibilidade da meta inflacionária. A manutenção dos juros em dois dígitos até 2024 demonstra a dificuldade de ancorar as expectativas inflacionárias em economias emergentes.
        """)

# ----------------- ABA 4: BASE DE DADOS TRATADA -----------------
with tab_dados:
    st.subheader("📋 Base de Dados Tratada (dados_macro_brasil_tratado.csv)")
    st.markdown(f"**Registros no filtro atual:** {len(df_view)} meses de dados.")
    
    col_d1, col_d2 = st.columns([3, 1])
    with col_d1:
        st.dataframe(df_view.style.format({
            'data': lambda x: x.strftime('%d/%m/%Y'),
            'selic': '{:.2f}%',
            'ipca': '{:.2f}%',
            'ipca_12m': lambda x: f"{x:.2f}%" if pd.notnull(x) else "—",
            'dolar': 'R$ {:.2f}'
        }), use_container_width=True)
    with col_d2:
        csv_data = df_view.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Baixar Dados Filtrados (CSV)",
            data=csv_data,
            file_name="dados_macro_brasil_filtrado.csv",
            mime="text/csv",
            use_container_width=True
        )
        st.info("Arquivo com tratamento completo: conversão de tipos, ordenação, interpolação e cálculo do IPCA 12m acumulado.")