import pandas as pd

# Caminho para o arquivo Excel
path_excel = 'File/Brasileiro_2024.xlsx'
df = pd.read_excel(path_excel)

# Remove a primeira linha (totalmente nula) e reinicia o índice
df = df.drop(index=0).reset_index(drop=True)

# Converte 'DATA - DIA' para string e extrai DATA e DIA
df['DATA - DIA'] = df['DATA - DIA'].astype(str)
df[['DATA', 'DIA']] = df['DATA - DIA'].str.extract(
    r'(\d{2}/\d{2})\s+([a-zç]{3})', expand=True
)

df = df.drop(columns=['DATA - DIA'])

# A informação aparece apenas uma vez por rodada, e as demais partidas não têm o número da rodada preenchido 
# o que torna a análise inconsistente.
# preencher valores nulos da coluna ROD com o último valor não nulo acima
df['ROD'] = df['ROD'].ffill()

df.at[0, 'DATA'] = '13/04'
df.at[0, 'DIA']  = 'sab'

# Preenche DATA e DIA apenas dentro de cada grupo de ROD
df[['DATA', 'DIA']] = df.groupby('ROD')[['DATA', 'DIA']].ffill()

print(df.head(10))