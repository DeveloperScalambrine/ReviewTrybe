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

#     # Gerando Grafico

# # if 'ROD_NUM' not in df.columns:
# #     df['ROD_NUM'] = df['ROD'].str.extract(r'(\d+)').astype(int)

# # # Filtra jogos com São Paulo SP como mandante ou visitante
# # sp_mandante = df_filter_2rod[df_filter_2rod['GolMandante'].str.contains(r'^São Paulo SP', regex=True)].copy()
# # sp_visitante = df_filter_2rod[df_filter_2rod['GolVisitante'].str.contains(r'^São Paulo SP', regex=True)].copy()

# # # Extrai gols e rodada
# # sp_mandante['GOLS'] = sp_mandante['GolMandante'].str.extract(r' - (\d+)$').astype(int)
# # sp_mandante['TIME'] = 'São Paulo SP'
# # sp_mandante['TIPO'] = 'Mandante'

# # sp_visitante['GOLS'] = sp_visitante['GolVisitante'].str.extract(r' - (\d+)$').astype(int)
# # sp_visitante['TIME'] = 'São Paulo SP'
# # sp_visitante['TIPO'] = 'Visitante'

# # # Junta os dois dataframes
# # sp_total = pd.concat([sp_mandante, sp_visitante])

# # # Agrupa por rodada e soma os gols
# # gols_por_rodada = sp_total.groupby('ROD_NUM')['GOLS'].sum()

# # # Identifica a rodada com mais e menos gols
# # rodada_max = gols_por_rodada.idxmax()
# # rodada_min = gols_por_rodada.idxmin()

# # # --- 📊 Gráfico ---
# # plt.figure(figsize=(10, 6))
# # bars = plt.bar(gols_por_rodada.index, gols_por_rodada.values, color='skyblue')

# # # Destaca as rodadas com mais e menos gols
# # bars[gols_por_rodada.index.get_loc(rodada_max)].set_color('green')
# # bars[gols_por_rodada.index.get_loc(rodada_min)].set_color('red')

# # # Rótulos
# # plt.title('Gols do São Paulo SP até a decima Rodada')
# # plt.xlabel('Rodada')
# # plt.ylabel('Gols Marcados')
# # plt.xticks(gols_por_rodada.index)

# # # Anotações
# # plt.text(rodada_max, gols_por_rodada[rodada_max] + 0.2, f'Máx: {gols_por_rodada[rodada_max]}', ha='center', color='green')
# # plt.text(rodada_min, gols_por_rodada[rodada_min] + 0.2, f'Mín: {gols_por_rodada[rodada_min]}', ha='center', color='red')

# # os.makedirs('img', exist_ok=True)

# # plt.tight_layout()
# # plt.savefig('img/grafico_sao_paulo_sp.png', dpi=300)
# # print("✅ Gráfico salvo como 'grafico_sao_paulo_sp.png'")
