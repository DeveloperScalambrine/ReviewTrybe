import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
from graphs import better_team, top5_filtered, pred_Winner, plot_previsao_cores_times
from line_graph import plot_evolucao_top5

# Caminho para o arquivo Excel
path_excel = "File/Tables.xlsx"
# all_able = pd.read_excel(path_excel, sheet_name=None)
df = pd.read_excel(path_excel, sheet_name="Rodadas-2024")
# df_classificacao = pd.read_excel(path_excel, sheet_name="Classificação")
# df = all_able["Rodadas-2024"]
# df_classificacao = all_able["Classificação"]
top5_df = better_team(df)
forecast = pred_Winner(df, top5_df)
# plot_previsao(forecast)
# Exemplo de uso em main

    # Ajuste o caminho conforme seu diretório de projeto
# plot_evolucao_top5(path_excel)
# print(f"✅ Gráfico salvo em {os.path.abspath('img/indicadores_top5_linha.png')}")

graf_data = forecast[['Time','PontosPrevistos','MediaPontos']]

plot_previsao_cores_times(
    table=forecast[['Time', 'PontosPrevistos', 'MediaPontos']],
    limiar_campeao=75,
    jogos=14,
    total_rodadas=38,
    output_path="img/previsao_cores.png"
)

# top5 = better_team(df)

# # Gera gráfico de linhas
# plt.figure(figsize=(10, 6))
# plt.plot(top5['Time'], top5['Pontos'], marker='o', color='royalblue', linestyle='-', linewidth=2)

# plt.title("Top 5 Times com Mais Pontos até a 14ª Rodada")
# plt.xlabel("Times")
# plt.ylabel("Total de Pontos")
# plt.grid(True)
# plt.xticks(rotation=45)

# # Adiciona os valores no gráfico
# for i, v in enumerate(top5['Pontos']):
#     plt.text(i, v + 0.5, str(v), ha='center')

# caminho_grafico = "img/indicadores-14-melhores.png"
# plt.tight_layout()
# plt.savefig(caminho_grafico, dpi=300)
# print(f"✅ Gráfico salvo em: {caminho_grafico}")


# top5 = better_team(df)
# # Gera gráfico
# plt.figure(figsize=(10, 6))
# plt.barh(top5['Time'], top5['TotalPontos'], color='royalblue')
# plt.xlabel("Total de Pontos")
# plt.title("Top 5 Times com Mais Pontos até a 14ª Rodada")
# plt.gca().invert_yaxis()  # Coloca o 1º no topo

# # Adiciona valores nas barras
# for i, v in enumerate(top5['TotalPontos']):
#     plt.text(v + 0.5, i, str(v), va='center')

# # Salva o gráfico
# caminho_grafico = "img/indicadores-14-melhores.png"
# plt.tight_layout()
# plt.savefig(caminho_grafico, dpi=300)
# print(f"✅ Gráfico salvo em: {caminho_grafico}")

# A informação aparece apenas uma vez por rodada, e as demais partidas não têm o número da rodada preenchido 
# o que torna a análise inconsistente.
# preencher valores nulos da coluna ROD com o último valor não nulo acima
df['ROD'] = df['ROD'].ffill()

df.at[0, 'DATA'] = '13/04'
df.at[0, 'DIA']  = 'sab'

# Preenche DATA e DIA apenas dentro de cada grupo de ROD
df[['DATA', 'DIA']] = df.groupby('ROD')[['DATA', 'DIA']].ffill()

df['JOGO'] = df['JOGO'].astype(str)
df[['TimeMandante', 'UF_M', 'Gols_M', 'Gols_V', 'TimeVisitante', 'UF_V']] = df['JOGO'].str.extract(
    r'^(.*?)\s+([A-Z]{2})\s+(\d+)\s+x\s+(\d+)\s+(.*?)\s+([A-Z]{2})$'
)

mask_invalid = df[['TimeMandante', 'UF_M', 'Gols_M', 'Gols_V', 'TimeVisitante', 'UF_V']].isnull().any(axis=1)
df_error_extract = df[mask_invalid]

df['GolMandante'] = df['TimeMandante'].str.strip() + ' ' + df['UF_M'] + ' - ' + df['Gols_M']
df['GolVisitante'] = df['TimeVisitante'].str.strip() + ' ' + df['UF_V'] + ' - ' + df['Gols_V']

    #  Pequena analise filtrando por equipe e rodada
# df_filter_2rod = df[df['ROD'].isin(['1ª', '2ª', '3ª'])]
df['ROD_NUM'] = df['ROD'].str.extract(r'(\d+)').astype(int)

# Filtra do início até a segunda rodada
df_filter_2rod = df[df['ROD_NUM'] <= 10]

principal = df_filter_2rod[df_filter_2rod['GolMandante'].str.contains(r'^São Paulo SP', regex=True)]

visitor = df_filter_2rod[df_filter_2rod['GolVisitante'].str.contains(r'^São Paulo SP', regex=True)]

gols_principal = principal['GolMandante'].str.extract(r' - (\d+)$').astype(int).sum().values[0]
gols_visitor = visitor['GolVisitante'].str.extract(r' - (\d+)$').astype(int).sum().values[0]

total_gols_sp = gols_principal + gols_visitor


# df.to_excel('File/Brasileiro_2024_limpo.xlsx', index=False)
# print("📁 Arquivo salvo como 'File/Brasileiro_2024_limpo.xlsx'")

