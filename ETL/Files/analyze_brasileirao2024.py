import os
import pandas as pd
# Base: pasta onde o script está
BASE_DIR = os.path.dirname(__file__)

# Caminho para arquivos de entrada (Excel)
INPUT_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "Created_File"))

# Caminho para salvar imagens
OUTPUT_IMG_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "img"))

paths = [
    os.path.join(INPUT_DIR, 'Brasileiro_2024.xlsx'),
    os.path.join(INPUT_DIR, 'Tables.xlsx')
]


# analyze.py → Funções principais de análise
from analyze import (
    pred_Winner,
    analyze_Gol_Per_Round,
    plot_previsao_cores_times,
    better_team,
    reading_tabs,
    analyze_Per_Round,
    perfor_inside_outside,
    round_favority
    # records_general
    # extract_pdf_tables_to_excel  # Ative se for usar conversão de PDF
)

# graphs.py → Funções para gráficos de barras
from graphs import (
    graph_team_round_gol,
    graph_five_top,
    graph_better_team,
    plot_previsao,
    graph_better_round
)

# line_graph.py → Gráfico de linha de evolução
from line_graph import (
    plot_evolucao_top5, 
    performance_analysis_use, 
    analysis_by_goal, 
    analysis_performance_home,
    analysis_win_out,
    point_home_out,
    plot_with_regression
)
#---------------------------------------------------------------#
# 💼 ETAPA OPCIONAL: Converter PDF para Excel
#---------------------------------------------------------------#
# path_pdf_input = "File/Brasileiro_2024.pdf"
# file_excel = "Brasileiro_2024.xlsx"
# success = extract_pdf_tables_to_excel(path_pdf_input, file_excel)
# print("\n✅ Conversão concluída!" if success else "\n❌ Erro na conversão.")

#---------------------------------------------------------------#
# 🎯 FUNÇÃO PRINCIPAL
#---------------------------------------------------------------#
def main():
    # print("🔎 Gerando previsão de pontos para o Brasileirão 2024...")

    # forecast = pred_Winner()

    # plot_previsao_cores_times(
    #     table=forecast,
    #     limiar_campeao=75,
    #     jogos=14,
    #     total_rodadas=38,
    #     output_path="/home/carlos/ReviewTrybe/ETL/img/previsao_cores.png"
    # )

    # # 🟡 Ative conforme necessidade:
    # analyze_Gol_Per_Round(graph_team_round_gol)
    # better_team(graph_better_team)
    # reading_tabs(graph_five_top)
    # plot_previsao()
    # plot_evolucao_top5(paths[1])
    # # analyze_Per_Round(7)
    # perfor_inside_outside(analysis_performance_home)
    # perfor_inside_outside(analysis_win_out)
    # perfor_inside_outside(point_home_out)
    # perfor_inside_outside(plot_with_regression)
    round_favority(graph_better_round)

    print("✅ Análise finalizada com sucesso!")

#---------------------------------------------------------------#
if __name__ == "__main__":
    main()
