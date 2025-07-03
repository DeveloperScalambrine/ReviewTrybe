import pandas as pd
import matplotlib.pyplot as plt
import os

# Caminho para o arquivo Excel
path_excel = "File/Tables.xlsx"
all_able = pd.read_excel(path_excel, sheet_name=None)
# df = pd.read_excel(path_excel, sheet_name="Rodadas-2024")
# df_classificacao = pd.read_excel(path_excel, sheet_name="Classificação")

df = all_able["Rodadas-2024"]
df_classificacao = all_able["Classificação"]

# Exemplo: visualizar as 5 primeiras linhas de cada aba
print(df.head())
print(df_classificacao.head())
print(len(df_classificacao) + len(df))

# Remove a primeira linha (totalmente nula) e reinicia o índice
df = df.drop(index=0).reset_index(drop=True)

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
df.to_excel('File/Brasileiro_2024_limpo.xlsx', index=False)
print("📁 Arquivo salvo como 'File/Brasileiro_2024_limpo.xlsx'")

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

