import pdfplumber
import pandas as pd
import os

path_pdf = "File/Brasileiro_2024.pdf"

out_folder = "File"
os.makedirs(out_folder, exist_ok=True)

all_tables = []

with pdfplumber.open(path_pdf) as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            df = pd.DataFrame(table[1:], columns=table[0])
            all_tables.append(df)

if all_tables:
    print(f"Número de tabelas extraídas: {len(all_tables)}")

column_reference = all_tables[0].columns

table_filter = [df for df in all_tables if list(df.columns) == list(column_reference)]

result = pd.concat(table_filter, ignore_index=True)
file_excel = os.path.join(out_folder, "Brasileiro_2024.xlsx")
result.to_excel(file_excel, index=False)
print("✅ Conversão concluída! Arquivo salvo como Brasileiro_2024.xlsx")