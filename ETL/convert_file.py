import pdfplumber
import pandas as pd

path_pdf = "File/Tabela Brasileirão Série A 2024 - 06.12.24.pdf"

all_tables = []

with pdfplumber.open(path_pdf) as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            df = pd.DataFrame(table[1:], columns=table[0])
            all_tables.append(df)