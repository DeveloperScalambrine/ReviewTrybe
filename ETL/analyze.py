import pandas as pd

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
    print(df.head())
    return df
