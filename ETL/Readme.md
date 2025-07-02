# 🏆 Análise da Tabela do Campeonato Brasileiro 2024

Este projeto realiza uma análise da tabela do Campeonato Brasileiro de 2024, utilizando a metodologia **ETL (Extract, Transform, Load)** para explorar e visualizar os dados de forma eficiente.

---

## 📌 Objetivo

O principal objetivo é aplicar conceitos de engenharia e análise de dados para extrair insights da tabela do Brasileirão 2024, explorando desempenho de times, evolução de pontuação, mandantes vs visitantes, e muito mais.

---

## ⚙️ Metodologia (ETL)

- **🗃️ Extração:** 
  - Conversão automatizada de um arquivo PDF contendo a tabela do Brasileirão 2024 para o formato Excel (`.xlsx`) utilizando `pdfplumber` e `pandas`.
  - Coleta dos dados da tabela oficial (caso necessário, via scraping, API ou CSV adicional).

- **🔄 Transformação:** 
  - Limpeza e padronização dos dados (tratamento de nulos, conversões de tipos, normalização de nomes de times).
  - Cálculo de métricas como aproveitamento, saldo de gols, pontos por rodada, etc.

- **📥 Carga:** 
  - Armazenamento dos dados tratados em DataFrames e exportação para arquivos `.csv` ou visualizações.

---

## 📊 Ferramentas Utilizadas

- Python
- Pandas
- Jupyter Notebook
- Matplotlib / Seaborn
- Requests / BeautifulSoup (se scraping foi usado)

---

## 🔍 Insights Gerados

- Ranking por desempenho geral
- Comparativo entre desempenho em casa vs fora
- Evolução da pontuação por rodada
- Análise de tendências de vitória/empate/derrota

---

## 📁 Estrutura do Projeto

