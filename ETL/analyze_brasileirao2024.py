import pandas as pd

path_excel = 'File/Brasileiro_2024.xlsx'
df = pd.read_excel(path_excel)

#     Confirmando os registros retornados
# print(f"Total de registros: {len(df)}")

df = df.drop(index=0).reset_index(drop=True)

# A informação aparece apenas uma vez por rodada, e as demais partidas não têm o número da rodada preenchido 
# o que torna a análise inconsistente, para a coluna DATA - DIA tambem é verdadeiro
# preencher valores nulos da coluna ROD com o último valor não nulo acima
df['ROD'] = df['ROD'].fillna(method='ffill')
df['DATA - DIA'] = df['DATA - DIA'].fillna(method='ffill')
print(df.head(13))




