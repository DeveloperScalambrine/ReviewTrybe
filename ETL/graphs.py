import pandas as pd
import matplotlib.pyplot as plt
import os

path_excel = "File/Tables.xlsx" 


if not os.path.exists(path_excel):
    raise FileNotFoundError(f"Arquivo não encontrado: {path_excel}")

df_classificacao = pd.read_excel(path_excel, sheet_name="Classificação")

# Remove espaços extras nos nomes das colunas
df_classificacao.columns = df_classificacao.columns.str.strip()

# Ordena os times por Pontos e seleciona os 5 primeiros
top5 = df_classificacao.sort_values(by="Pontos", ascending=False).head(5)

# Cria o gráfico
plt.figure(figsize=(10, 6))
plt.bar(top5["Nome dos Times"], top5["Pontos"], color="royalblue")
plt.title("Top 5 Times - Pontuação")
plt.xlabel("Times")
plt.ylabel("Pontos")
plt.xticks(rotation=45)
plt.tight_layout()

# Salva o gráfico
plt.savefig("img/top5_pontos_classificacao.png", dpi=300)
print("✅ Gráfico salvo em 'graphs/top5_pontos_classificacao.png'")
