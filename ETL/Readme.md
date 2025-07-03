# 🏆 Análise da Tabela do Campeonato Brasileiro 2024

Este projeto realiza uma análise completa da Tabela do Campeonato Brasileiro Série A - Edição 2024, aplicando os princípios de **ETL (Extract, Transform, Load)** e visualização de dados para gerar insights significativos sobre o desempenho dos clubes.

---

## 📌 Objetivo

O principal objetivo é aplicar técnicas de engenharia e análise de dados para extrair, tratar e interpretar informações da tabela oficial do Brasileirão 2024, respondendo perguntas como:

- Quais times estão se destacando?
- Como está o desempenho dentro e fora de casa?
- Quais rodadas foram mais produtivas para determinado time?
- Como construir uma classificação automática baseada nos resultados?

---

## ⚙️ Metodologia (ETL)

### 🔍 Etapa 1: Extração

- O arquivo oficial da tabela foi obtido diretamente do site da **CBF (Confederação Brasileira de Futebol)**:  
  🔗 [Plano Geral de Ação - Série A 2024 (PDF)](https://www.cbf.com.br/futebol-brasileiro/tabelas/campeonato-brasileiro/serie-a/2024?doc=Plano%20Geral%20de%20A%C3%A7%C3%A3o)

- O documento foi convertido de PDF para `.xlsx` utilizando bibliotecas como `pdfplumber` e `pandas`.

---

### 🧹 Etapa 2: Transformação

- Remoção de linhas nulas e padronização de colunas.
- Separação da coluna `DATA - DIA` em `DATA` e `DIA`.
- Extração dos times, UFs e resultados da coluna `JOGO`.
- Criação de colunas auxiliares como `GolMandante`, `GolVisitante`, `ROD_NUM` e mais.
- Tratamento de inconsistências (ex: nomes duplicados como “Atlético” resolvidos usando UF).
- Preenchimento de dados ausentes por forward fill (`ffill`) dentro de grupos de rodada.

---

### 📊 Etapa 3: Análise

Realizamos duas análises principais:

#### ✅ Análise 1: Gols do São Paulo SP nas 10 primeiras rodadas
- Filtramos os jogos do São Paulo como mandante e visitante.
- Calculamos o total de gols marcados e os distribuímos por rodada.
- Geramos um gráfico destacando a rodada com mais e menos gols.
- 📎 **Gráfico salvo em**: `img/grafico_sao_paulo_sp.png`

#### ✅ Análise 2: Classificação automática

- A aba **Classificação** foi construída usando **PROCV** e **SOMARPRODUTO** no Google Sheets.
- Dados como vitórias, derrotas, empates, pontos, gols marcados, sofridos e saldo de gols foram extraídos com base na aba `Rodadas-2024`.

🧮 Planilha usada:
🔗 [Google Sheets – Classificação](https://docs.google.com/spreadsheets/d/1lDTPz1PrWOYceKmN7aR4eJ5AlIIXIVcBDxSVV_WxpK4/edit?gid=1209557442#gid=1209557442)

---

### 📈 Etapa 4: Visualização

Além dos gráficos de rodada, criamos uma visualização com os 5 primeiros colocados:

#### 📊 Gráfico de barras dos 5 primeiros colocados
- Utilizamos a aba "Classificação" da planilha.
- Selecionamos os 5 primeiros times com maior pontuação.
- Visualização gerada com Matplotlib.

📎 **Gráfico salvo em**: `img/grafico_top5_classificacao.png`

---

## 📁 Estrutura do Projeto

ETL/
├── File/
│ ├── Tables.xlsx
│ ├── Brasileirao_2024_limpo.xlsx
├── img/
│ ├── grafico_sao_paulo_sp.png
│ ├── grafico_top5_classificacao.png
├── analyze_brasileirao2024.py
├── graphs.py
├── README.md


---

## 🛠️ Ferramentas Utilizadas

- Python 3.12+
- Pandas
- Matplotlib
- openpyxl
- pdfplumber (para conversão PDF → Excel)
- Google Sheets (para fórmulas e validação de classificação)
- VS Code / Jupyter Notebook

---

## 💡 Próximos passos

- Aplicar web scraping para atualizações em tempo real.
- Criar uma interface gráfica com Streamlit para visualização interativa.
- Expandir análises para performance por estádio e público.

---

## 📬 Contato

Caso queira colaborar ou tirar dúvidas sobre o projeto, entre em contato por GitHub ou LinkedIn.

---

🚀 Projeto 100% em código aberto — sinta-se à vontade para reutilizar e melhorar!

