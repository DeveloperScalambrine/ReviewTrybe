import os
import pdfplumber
import pandas as pd

def extract_pdf_tables_to_excel(pdf_input_path: str, output_excel_filename: str):
   
    output_folder = os.path.dirname(pdf_input_path) if os.path.dirname(pdf_input_path) else "File"

    os.makedirs(output_folder, exist_ok=True)

    if not os.path.exists(pdf_input_path):
        print(f"Erro: O arquivo PDF não foi encontrado em '{pdf_input_path}'")
        return False

    all_tables = []

    try:
        with pdfplumber.open(pdf_input_path) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                for table in tables:
                    # Garante que a tabela tenha cabeçalho e pelo menos uma linha de dados
                    if table and len(table) > 1:
                        # Usa a primeira linha como cabeçalhos e as linhas subsequentes como dados
                        df = pd.DataFrame(table[1:], columns=table[0])
                        all_tables.append(df)
                    else:
                        print(f"Aviso: Tabela vazia ou sem cabeçalho encontrada na página {page.page_number}. Ignorando.")

    except Exception as e:
        print(f"Erro ao processar o PDF: {e}")
        return False

    if not all_tables:
        print(f"Nenhuma tabela foi extraída do PDF '{pdf_input_path}'.")
        return False

    print(f"Número de tabelas extraídas: {len(all_tables)}")

    column_reference = all_tables[0].columns

    filtered_tables = [
        df for df in all_tables
        if tuple(df.columns.tolist()) == tuple(column_reference.tolist())
    ]

    if not filtered_tables:
        print("Nenhuma tabela com a estrutura de coluna de referência foi encontrada após a filtragem.")
        return False

    df_result = pd.concat(filtered_tables, ignore_index=True)

    path_file_excel = os.path.join(output_folder, output_excel_filename)

    try:
        df_result.to_excel(path_file_excel, index=False)
        print(f"✅ Conversão concluída! Arquivo salvo como '{output_excel_filename}' em '{output_folder}'")
        return True
    except Exception as e:
        print(f"Erro ao salvar o arquivo Excel: {e}")
        return False