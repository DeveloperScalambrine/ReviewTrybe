import pandas as pd

path_excel = 'File/Brasileiro_2024.xlsx'
df = pd.read_excel(path_excel)
print(df.head())
