# 📊 Painel Macroeconômico: Inflação, Juros e Câmbio (Brasil: 2018–2024)

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.50.0-FF4B4B.svg)](https://streamlit.io/)
[![UEMS](https://img.shields.io/badge/UEMS-Especializa%C3%A7%C3%A3o%20em%20Ci%C3%AAncia%20de%20Dados%20e%20IA-065F46.svg)](https://www.uems.br/)

Projeto Integrador desenvolvido para a **Agenda 4: Da Captura à Visualização** da disciplina de **Captura, Tratamento e Visualização de Dados** na **Especialização em Ciência de Dados e Inteligência Artificial (EaD)** da **Universidade Estadual de Mato Grosso do Sul (UEMS Virtual)**.

---

## 🎯 Objetivo do Projeto
Analisar as inter-relações entre três dos principais indicadores da economia brasileira contemporânea no período de **2018 a 2024**:
- **Taxa Selic Meta (% a.a.)**: Política monetária definida pelo COPOM/Banco Central.
- **IPCA (% mensal e acumulado 12M)**: Índice oficial de inflação ao consumidor apurado pelo IBGE.
- **Câmbio Comercial (USD/BRL)**: Cotação média do Dólar americano.

---

## 🏗️ Estrutura do Repositório

```text
├── app.py                         # Aplicação interativa e Dashboard em Streamlit
├── analise.ipynb                  # Notebook Jupyter com documentação e visualizações
├── dados_macro_brasil_raw.csv     # Base de dados bruta capturada via API SGS/BCB
├── dados_macro_brasil_tratado.csv # Base tratada com feature engineering (IPCA 12M)
├── gerar_relatorio_pdf.py         # Script para geração automatizada do relatório acadêmico
├── Relatorio_Final_Agenda4_UEMS.pdf # Relatório executivo final para submissão
├── requirements.txt               # Dependências do projeto para deploy na nuvem
├── .gitignore                     # Arquivos e diretórios ignorados pelo Git
└── README.md                      # Documentação completa do projeto
```

---

## 💡 Principais Insights Macroeconômicos

1. **Defasagem Temporal (*Lags* da Política Monetária):** A taxa Selic opera com retardo de **6 a 12 meses** sobre o IPCA acumulado. O choque de estímulo de 2020 (Selic a 2%) gerou repique inflacionário em 2021; já a alta para 13,75% levou cerca de um ano para conter a inflação.
2. **Efeito *Pass-Through* Cambial:** O salto do dólar de R$ 3,80 para mais de R$ 5,30 encareceu insumos importados, combustíveis e commodities, gerando pressões inflacionárias de custos.
3. **Assimetria Cíclica da Selic:** Oscilação extrema de mais de 11 pontos percentuais em menos de 2 anos (2,00% a 13,75%), refletindo a intensidade necessária para reancorar expectativas em mercados emergentes.

---

## 🚀 Como Executar Localmente

### 1. Clonar o repositório:
```bash
git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
cd SEU_REPOSITORIO
```

### 2. Criar e ativar o ambiente virtual:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar as dependências:
```bash
pip install -r requirements.txt
```

### 4. Executar o Dashboard Streamlit:
```bash
streamlit run app.py
```
O dashboard abrirá automaticamente no navegador em `http://localhost:8501`.

---

## 🌐 Deploy na Nuvem (Streamlit Community Cloud)

A aplicação pode ser publicada gratuitamente via **Streamlit Community Cloud**:
1. Conecte sua conta do GitHub em [share.streamlit.io](https://share.streamlit.io/).
2. Clique em **"New app"** e selecione este repositório.
3. Defina o arquivo principal como `app.py`.
4. Clique em **"Deploy"**!
