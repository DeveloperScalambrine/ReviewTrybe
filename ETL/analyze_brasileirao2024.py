from analyze import analyze_Gol_Per_Round, analyze_Per_Round, analyze_Per_Team, reading_tabs
from graphs import graph_team_round_gol, graph_five_top

# from convert_file import extract_pdf_tables_to_excel
# from graphs import better_team, top5_filtered, pred_Winner, plot_previsao_cores_times, graph_nome
# # from line_graph import plot_evolucao_top5

## Chamada para função de converter arquivo > extract_pdf_tables_to_excel ##

# path_pdf_input = "File/Brasileiro_2024.pdf"

# file_excel = "Brasileiro_2024.xlsx"

# print("Iniciando o processo de extração e conversão...")

# success = extract_pdf_tables_to_excel(path_pdf_input, file_excel)

# if success:
#         print("\nProcesso concluído com sucesso!")
# else:
#         print("\nO processo encontrou erros ou falhou.")
        #---------------------------------------------------------------##

## Chamando a função para analise de gols por rodada da equipe São Paulo, recebe como parametro uma função de grafico ##
# analyze_Gol_Per_Round(graph_team_round_gol)
##--------------------------------------------------------------------------------------------------##

## Chamando função para pesquisar por rodada especifica
# analyze_Per_Round(7)
#-------------------------------------------------#

reading_tabs(graph_five_top)
# # top5_df = better_team(df)
# # forecast = pred_Winner(df, top5_df)
# # plot_previsao(forecast)
# # Exemplo de uso em main

#     # Ajuste o caminho conforme seu diretório de projeto
# # plot_evolucao_top5(path_excel)
# # print(f"✅ Gráfico salvo em {os.path.abspath('img/indicadores_top5_linha.png')}")

# # graf_data = forecast[['Time','PontosPrevistos','MediaPontos']]

# # plot_previsao_cores_times(
# #     table=forecast[['Time', 'PontosPrevistos', 'MediaPontos']],
# #     limiar_campeao=75,
# #     jogos=14,
# #     total_rodadas=38,
# #     output_path="img/previsao_cores.png"
# # )

# # top5 = better_team(df)

# # # Gera gráfico de linhas
# # plt.figure(figsize=(10, 6))
# # plt.plot(top5['Time'], top5['Pontos'], marker='o', color='royalblue', linestyle='-', linewidth=2)

# # plt.title("Top 5 Times com Mais Pontos até a 14ª Rodada")
# # plt.xlabel("Times")
# # plt.ylabel("Total de Pontos")
# # plt.grid(True)
# # plt.xticks(rotation=45)

# # # Adiciona os valores no gráfico
# # for i, v in enumerate(top5['Pontos']):
# #     plt.text(i, v + 0.5, str(v), ha='center')

# # caminho_grafico = "img/indicadores-14-melhores.png"
# # plt.tight_layout()
# # plt.savefig(caminho_grafico, dpi=300)
# # print(f"✅ Gráfico salvo em: {caminho_grafico}")


# # top5 = better_team(df)
# # # Gera gráfico
# # plt.figure(figsize=(10, 6))
# # plt.barh(top5['Time'], top5['TotalPontos'], color='royalblue')
# # plt.xlabel("Total de Pontos")
# # plt.title("Top 5 Times com Mais Pontos até a 14ª Rodada")
# # plt.gca().invert_yaxis()  # Coloca o 1º no topo

# # # Adiciona valores nas barras
# # for i, v in enumerate(top5['TotalPontos']):
# #     plt.text(v + 0.5, i, str(v), va='center')

# # # Salva o gráfico
# # caminho_grafico = "img/indicadores-14-melhores.png"
# # plt.tight_layout()
# # plt.savefig(caminho_grafico, dpi=300)
# # print(f"✅ Gráfico salvo em: {caminho_grafico}")

