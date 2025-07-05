import matplotlib.pyplot as plt
import pandas as pd
import os
from analyze import pred_Winner
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

def graph_five_top(top_five):
    plt.figure(figsize=(10, 6))
    plt.bar(top_five["Nome dos Times"], top_five["Pontos"], color="royalblue")
    plt.title("Top 5 Times - Pontuação")
    plt.xlabel("Times")
    plt.ylabel("Pontos")
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Salva o gráfico
    plt.savefig("img/Cinco primeiros.png", dpi=300)
    print("✅ Gráfico salvo em 'img/Cinco primeiros'")

def graph_better_team(top5):
    plt.figure(figsize=(10, 6))
    plt.barh(top5['Time'], top5['Pontos'], color='royalblue')
    plt.xlabel("Total de Pontos")
    plt.title("Top 5 Times com Mais Pontos até a 14ª Rodada")
    plt.gca().invert_yaxis()  # Coloca o 1º no topo

    # Adiciona os valores nas barras
    for i, v in enumerate(top5['Pontos']):
        plt.text(v + 0.5, i, str(v), va='center')

    # Salva o gráfico
    path_graph = "img/5 melhores 14 Rodada.png"
    plt.tight_layout()
    plt.savefig(path_graph, dpi=300)
    print(f"✅ Gráfico salvo em: {path_graph}")

def plot_previsao(limiar_campeao=75, jogos=14, total_rodadas=38, output_path="img/previsao_pontuacao.png"):
    """
    Gera gráfico com previsão de pontuação final do Brasileirão 2024 para os times do top 5.
    """

    # Busca os dados previstos
    table = pred_Winner()

    # Ordena para barras horizontais de baixo (menores) para cima (maiores)
    table = table.sort_values("PontosPrevistos", ascending=True)

    # Normaliza cores entre min e máx previstos
    vals = table["PontosPrevistos"]
    norm = plt.Normalize(vals.min(), vals.max())
    cmap = plt.cm.get_cmap("viridis")
    colors = cmap(norm(vals))

    # Cria figura
    fig, ax = plt.subplots(figsize=(10, 6), facecolor="#f0f0f0")
    ax.set_facecolor("#f0f0f0")

    # Barras horizontais
    bars = ax.barh(table["Time"], table["PontosPrevistos"], color=colors, edgecolor="#ffffff", height=0.6)

    # Linha de limiar de campeão
    ax.axvline(limiar_campeao, color="crimson", linestyle="--", linewidth=2,
               label=f"Limiar Campeão: {limiar_campeao} pts")

    # Anotações
    for bar, m in zip(bars, table["MediaPontos"]):
        x = bar.get_width()
        y = bar.get_y() + bar.get_height() / 2
        ax.text(x + 0.5, y,
                f"{int(x)} pts\nMédia/jogo: {m:.2f}",
                va="center", ha="left", fontsize=9, color="#222222")

    # Títulos e rótulos
    ax.set_title("🏆 Previsão de Pontos Finais – Brasileirão 2024", fontsize=16, color="#222222", pad=15)
    ax.set_xlabel(f"Pontos Previstos (até {jogos}/{total_rodadas} rodadas)", fontsize=12, color="#444444", labelpad=10)
    ax.set_ylabel("Time", fontsize=12, color="#444444", labelpad=10)
    ax.tick_params(axis='both', colors="#555555", labelsize=10)
    ax.grid(axis="x", color="white", linestyle="-", linewidth=1)

    # Legenda
    ax.legend(frameon=False, fontsize=10, loc="lower right")

    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    fig.savefig(output_path, dpi=300, facecolor=fig.get_facecolor())
    plt.close(fig)

    print(f"✅ Previsão salva como '{output_path}'")


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
