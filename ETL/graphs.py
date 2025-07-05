import matplotlib.pyplot as plt
# from sklearn.linear_model import LinearRegression
# import numpy as np

def graph_team_round_gol(gols_por_rodada, rodada_max, rodada_min):
    
    # --- 📊 Gráfico ---
    plt.figure(figsize=(10, 6))
    bars = plt.bar(gols_por_rodada.index, gols_por_rodada.values, color='skyblue')

    bars[gols_por_rodada.index.get_loc(rodada_max)].set_color('green')
    bars[gols_por_rodada.index.get_loc(rodada_min)].set_color('red')

    # Rótulos
    plt.title('Gols do São Paulo SP por Rodada')
    plt.xlabel('Rodada')
    plt.ylabel('Gols Marcados')
    plt.xticks(gols_por_rodada.index)

    plt.text(rodada_max, gols_por_rodada[rodada_max] + 0.2, f'Máx: {gols_por_rodada[rodada_max]}', ha='center', color='green')
    plt.text(rodada_min, gols_por_rodada[rodada_min] + 0.2, f'Mín: {gols_por_rodada[rodada_min]}', ha='center', color='red')

    plt.tight_layout()
    plt.savefig('img/Gols Sao Paulo.png', dpi=300)
    print("✅ Gráfico salvo como 'Gols Sao Paulo.png'")

# def better_team(df):
#     # Etapa de preparação
#     df['ROD_NUM'] = df['ROD'].str.extract(r'(\d+)').astype(int)
#     df = df[df['ROD_NUM'] <= 14].copy()
#     df['Gols_M'] = df['Gols_M'].astype(int)
#     df['Gols_V'] = df['Gols_V'].astype(int)

#     # Nome dos times
#     df['Mandante'] = df['TimeMandante'].str.strip() + ' ' + df['UF_M']
#     df['Visitante'] = df['TimeVisitante'].str.strip() + ' ' + df['UF_V']

#     # Mandantes
#     mandante = df[['Mandante', 'Gols_M', 'Gols_V']].copy()
#     mandante.columns = ['Time', 'GolsFeitos', 'GolsSofridos']
#     mandante['Vitoria'] = (mandante['GolsFeitos'] > mandante['GolsSofridos']).astype(int)
#     mandante['Empate'] = (mandante['GolsFeitos'] == mandante['GolsSofridos']).astype(int)
#     mandante['PartidasMandante'] = 1
#     mandante['PartidasVisitante'] = 0

#     # Visitantes
#     visitante = df[['Visitante', 'Gols_V', 'Gols_M']].copy()
#     visitante.columns = ['Time', 'GolsFeitos', 'GolsSofridos']
#     visitante['Vitoria'] = (visitante['GolsFeitos'] > visitante['GolsSofridos']).astype(int)
#     visitante['Empate'] = (visitante['GolsFeitos'] == visitante['GolsSofridos']).astype(int)
#     visitante['PartidasMandante'] = 0
#     visitante['PartidasVisitante'] = 1

#     # Junta tudo
#     df_total = pd.concat([mandante, visitante])

#     # Agrupa
#     resumo = df_total.groupby('Time').agg({
#         'GolsFeitos': 'sum',
#         'PartidasMandante': 'sum',
#         'PartidasVisitante': 'sum',
#         'Vitoria': 'sum',
#         'Empate': 'sum'
#     }).reset_index()

#     # Pontuação total
#     resumo['Pontos'] = (resumo['Vitoria'] * 3) + (resumo['Empate'] * 1)

#     # Ordena
#     top5 = resumo.sort_values(by='Pontos', ascending=False).head(5)

#     # Conversão para inteiros
#     cols_int = ['GolsFeitos', 'PartidasMandante', 'PartidasVisitante', 'Vitoria', 'Empate', 'Pontos']
#     top5[cols_int] = top5[cols_int].astype(int)

#     return top5

# def top5_filtered(df_original, top5):
#     # Filtra somente os 5 melhores times
#     times_top5 = top5['Time'].tolist()

#     df = df_original.copy()
#     df['ROD_NUM'] = df['ROD'].str.extract(r'(\d+)').astype(int)
#     df = df[df['ROD_NUM'] <= 14].copy()
#     df['Gols_M'] = df['Gols_M'].astype(int)
#     df['Gols_V'] = df['Gols_V'].astype(int)

#     df['Mandante'] = df['TimeMandante'].str.strip() + ' ' + df['UF_M']
#     df['Visitante'] = df['TimeVisitante'].str.strip() + ' ' + df['UF_V']

#     # Mandantes
#     mandante = df[df['Mandante'].isin(times_top5)].copy()
#     mandante['Time'] = mandante['Mandante']
#     mandante['GolsFeitos'] = mandante['Gols_M']
#     mandante['Vitoria'] = (mandante['Gols_M'] > mandante['Gols_V']).astype(int)
#     mandante['Empate'] = (mandante['Gols_M'] == mandante['Gols_V']).astype(int)
#     mandante['Pontos'] = mandante['Vitoria'] * 3 + mandante['Empate'] * 1

#     # Visitantes
#     visitante = df[df['Visitante'].isin(times_top5)].copy()
#     visitante['Time'] = visitante['Visitante']
#     visitante['GolsFeitos'] = visitante['Gols_V']
#     visitante['Vitoria'] = (visitante['Gols_V'] > visitante['Gols_M']).astype(int)
#     visitante['Empate'] = (visitante['Gols_V'] == visitante['Gols_M']).astype(int)
#     visitante['Pontos'] = visitante['Vitoria'] * 3 + visitante['Empate'] * 1

#     # Agrupamento
#     resumo_mandante = mandante.groupby('Time').agg({
#         'GolsFeitos': 'sum',
#         'Pontos': 'sum'
#     }).rename(columns={
#         'GolsFeitos': 'GolsMandante',
#         'Pontos': 'PontosMandante'
#     })

#     resumo_visitante = visitante.groupby('Time').agg({
#         'GolsFeitos': 'sum',
#         'Pontos': 'sum'
#     }).rename(columns={
#         'GolsFeitos': 'GolsVisitante',
#         'Pontos': 'PontosVisitante'
#     })

#     # Junta as análises
#     analise_final = resumo_mandante.join(resumo_visitante, how='outer').fillna(0).astype(int)
#     analise_final['PontosTotal'] = analise_final['PontosMandante'] + analise_final['PontosVisitante']
#     analise_final = analise_final.reset_index()

#     return analise_final

# def pred_Winner(df_original, top5):
#     summary = top5_filtered(df_original, top5)

#     summary['Jogos'] = 14

#     summary['MediaPontos'] = summary['PontosTotal'] / summary['Jogos']

#     summary['PontosPrevistos'] = summary['MediaPontos'] * 38

#     summary['MediaPontos'] = summary['MediaPontos'].round(2).astype(float)
#     summary['PontosPrevistos'] = summary['PontosPrevistos'].round().astype(int)

#     LIMIT_WINNER = 79

#     summary['ProbabilidadeCampeao'] = np.where(
#         summary['PontosPrevistos'] >= LIMIT_WINNER, 'Alta',
#         np.where(summary['PontosPrevistos'] >= 70, 'Média', 'Baixa')
#     )

#     return summary[['Time', 'PontosTotal', 'MediaPontos', 'PontosPrevistos', 'ProbabilidadeCampeao']]

# # def plot_previsao(table, limiar_campeao=75, jogos=14, total_rodadas=38, output_path="img/previsao_pontuacao.png"):
# #     """
# #     Plota a previsão de pontuação final para o Brasileirão 2024.

# #     Parâmetros:
# #     - table: DataFrame com colunas ['Time', 'PontosPrevistos', 'MediaPontos']
# #     - limiar_campeao: pontos mínimos para alta probabilidade de título
# #     - jogos: número de rodadas já disputadas
# #     - total_rodadas: total de rodadas no campeonato
# #     - output_path: caminho para salvar o gráfico
# #     """
# #     # Ordena para barras horizontais de baixo (menores) para cima (maiores)
# #     table = table.sort_values("PontosPrevistos", ascending=True)

# #     # Normaliza cores entre min e máx previstos
# #     vals = table["PontosPrevistos"]
# #     norm = plt.Normalize(vals.min(), vals.max())
# #     cmap = plt.cm.get_cmap("viridis")
# #     colors = cmap(norm(vals))

# #     # Cria figura
# #     fig, ax = plt.subplots(figsize=(10, 6), facecolor="#f0f0f0")
# #     ax.set_facecolor("#f0f0f0")

# #     # Barras horizontais
# #     bars = ax.barh(table["Time"], table["PontosPrevistos"], color=colors, edgecolor="#ffffff", height=0.6)

# #     # Linha de limiar de campeão
# #     ax.axvline(limiar_campeao, color="crimson", linestyle="--", linewidth=2,
# #                label=f"Limiar Campeão: {limiar_campeao} pts")

# #     # Anotações: pontos e média
# #     for bar, m in zip(bars, table["MediaPontos"]):
# #         x = bar.get_width()
# #         y = bar.get_y() + bar.get_height()/2
# #         ax.text(x + 0.5, y,
# #                 f"{int(x)} pts\nMédia/jogo: {m:.2f}",
# #                 va="center", ha="left", fontsize=9, color="#222222")

# #     # Títulos e rótulos
# #     ax.set_title("🏆 Previsão de Pontos Finais – Brasileirão 2024", fontsize=16, color="#222222", pad=15)
# #     ax.set_xlabel(f"Pontos Previstos (até {jogos}/{total_rodadas} rodadas)", fontsize=12, color="#444444", labelpad=10)
# #     ax.set_ylabel("Time", fontsize=12, color="#444444", labelpad=10)
# #     ax.tick_params(axis='both', colors="#555555", labelsize=10)
# #     ax.grid(axis="x", color="white", linestyle="-", linewidth=1)

# #     # Legenda
# #     ax.legend(frameon=False, fontsize=10, loc="lower right")

# #     plt.tight_layout()
# #     os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
# #     fig.savefig(output_path, dpi=300, facecolor=fig.get_facecolor())
# #     plt.close(fig)
# def plot_previsao_cores_times(table, limiar_campeao=75, jogos=14, total_rodadas=38, output_path="img/previsao_cores.png"):

#     cores_times = {
#         'Flamengo RJ': '#C80000',
#         'Palmeiras SP': '#1C9240',
#         'São Paulo SP': '#DF0A0A',
#         'Botafogo RJ': '#000000',
#         'Grêmio RS': '#0099DA',
#         'Internacional RS': '#ED1B24',
#         'Corinthians SP': '#111111',
#         'Atlético MG': '#222222',
#         'Atlético GO': '#D70000',
#         'Cruzeiro MG': '#0033A0',
#         'Fortaleza CE': '#004AAD',
#         'Fluminense RJ': '#006600',
#         'Bahia BA': '#005CA9',
#         'Cuiabá MT': '#007F3E',
#         'Vasco da Gama RJ': '#231F20',
#         'Red Bull Bragantino SP': '#FFFFFF',
#         'Juventude RS': '#007B3A',
#         'Vitória BA': '#CC0000',
#         'Athletico PR': '#D10000',
#         'Criciúma SC': '#FFD700'
#     }

#     table = table.sort_values("PontosPrevistos", ascending=True)

#     fig, ax = plt.subplots(figsize=(10, 6), facecolor="#f7f7f7")
#     ax.set_facecolor("#f7f7f7")

#     # Aplica a cor do time (ou fallback azul)
#     cores = [cores_times.get(time, 'steelblue') for time in table["Time"]]

#     bars = ax.barh(table["Time"], table["PontosPrevistos"], color=cores, edgecolor="white", height=0.6)

#     # Linha de limiar para título
#     ax.axvline(limiar_campeao, color="crimson", linestyle="--", linewidth=2,
#                label=f"Limiar Campeão: {limiar_campeao} pts")

#     # Anotações
#     for bar, media in zip(bars, table["MediaPontos"]):
#         x = bar.get_width()
#         y = bar.get_y() + bar.get_height() / 2
#         ax.text(x + 0.8, y,
#                 f"{int(x)} pts\n{media:.2f}/jogo",
#                 va="center", ha="left", fontsize=9, color="#222")

#     ax.set_title("Previsão Final do Brasileirão 2024", fontsize=16, color="#111", pad=15)
#     ax.set_xlabel(f"Pontos Previstos (após {jogos}/{total_rodadas} rodadas)", fontsize=12)
#     ax.set_ylabel("Time", fontsize=12)
#     ax.tick_params(axis='both', labelsize=10, colors="#333")
#     ax.grid(axis="x", linestyle="--", linewidth=0.5, color="#cccccc")

#     ax.legend(loc="lower right", fontsize=10, frameon=False)

#     plt.tight_layout()
#     os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
#     fig.savefig(output_path, dpi=300, facecolor=fig.get_facecolor())
#     plt.close(fig)
