import pandas as pd

path = 'File/Brasileiro_2024.xlsx'

def read(table, type_file):
   
    readers = {
        'csv': pd.read_csv,
        'excel': pd.read_excel,
        'json': pd.read_json,
        'parquet': pd.read_parquet,
        'html': pd.read_html,
        'feather': pd.read_feather,
        'stata': pd.read_stata
        # Adicione outros formatos aqui se necessário
    }

    if type_file not in readers:
        raise ValueError(f"Tipo de arquivo '{type_file}' não suportado.")

    df = readers[type_file](table)
    
    return df

def analyze_Per_Team():
    df = read(path, "excel")
    
    df['JOGO'] = df['JOGO'].astype(str)

    # Extrai os dados usando expressão regular
    df[['TimeMandante', 'UF_M', 'Gols_M', 'Gols_V', 'TimeVisitante', 'UF_V']] = df['JOGO'].str.extract(
        r'^(.*?)\s+([A-Z]{2})\s+(\d+)\s+x\s+(\d+)\s+(.*?)\s+([A-Z]{2})$'
    )

    # Cria colunas com os textos formatados
    df['GolMandante'] = df['TimeMandante'].str.strip() + ' ' + df['UF_M'] + ' - ' + df['Gols_M']
    df['GolVisitante'] = df['TimeVisitante'].str.strip() + ' ' + df['UF_V'] + ' - ' + df['Gols_V']

    # df_filter_2rod = df[df['ROD'].isin(['1ª', '2ª', '3ª'])]
    df['ROD_NUM'] = df['ROD'].str.extract(r'(\d+)').astype(int)

# Filtra do início até a segunda rodada
    df_filter_2rod = df[df['ROD_NUM'] <= 10]

    principal = df_filter_2rod[df_filter_2rod['GolMandante'].str.contains(r'^São Paulo SP', regex=True)]

    visitor = df_filter_2rod[df_filter_2rod['GolVisitante'].str.contains(r'^São Paulo SP', regex=True)]

    gols_principal = principal['GolMandante'].str.extract(r' - (\d+)$').astype(int).sum().values[0]
    gols_visitor = visitor['GolVisitante'].str.extract(r' - (\d+)$').astype(int).sum().values[0]

    total_gols_sp = gols_principal + gols_visitor

    print(f"Gols marcados por São Paulo SP na primeira e segunda rodada: {total_gols_sp}")