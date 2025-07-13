import matplotlib.pyplot as plt
import pandas as pd
import os
from analyze import pred_Winner
import os
from analyze import round_favority

# Base: pasta onde o script está
BASE_DIR = os.path.dirname(__file__)

# Caminho para arquivos de entrada (Excel)
INPUT_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "Created_File"))

# Caminho para salvar imagens
OUTPUT_IMG_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "img"))


def graph_team_round_gol(gol_per_round, round_max, round_min):
    
    # --- 📊 Gráfico ---
    plt.figure(figsize=(10, 6))
    bars = plt.bar(gol_per_round.index, gol_per_round.values, color='skyblue')

    bars[gol_per_round.index.get_loc(round_max)].set_color('green')
    bars[gol_per_round.index.get_loc(round_min)].set_color('red')

    # Rótulos
    plt.title('Gols do São Paulo SP por Rodada')
    plt.xlabel('Rodada')
    plt.ylabel('Gols Marcados')
    plt.xticks(gol_per_round.index)

    plt.text(round_max, gol_per_round[round_max] + 0.2, f'Máx: {gol_per_round[round_max]}', ha='center', color='green')
    plt.text(round_min, gol_per_round[round_min] + 0.2, f'Mín: {gol_per_round[round_min]}', ha='center', color='red')

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_IMG_DIR, 'Gols Sao Paulo.png'), dpi=300)
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
    plt.savefig(os.path.join(OUTPUT_IMG_DIR, "Cinco primeiros.png"), dpi=300)
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
    path_graph = "/home/carlos/ReviewTrybe/ETL/img/Os 5 melhores 14 Rodada.png"

    # Garante que a pasta 'img/' exista

    plt.tight_layout()
    plt.savefig(path_graph, dpi=300)
    print(f"✅ Gráfico salvo em: {path_graph}")

def plot_previsao(limiar_campeao=75, jogos=14, total_rodadas=38, output_path="/home/carlos/ReviewTrybe/ETL/img/previsao_pontuacao.png"):
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
    # plt.savefig(os.path.join(OUTPUT_IMG_DIR, 'Previsao.png'), dpi=300)
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    fig.savefig(output_path, dpi=300, facecolor=fig.get_facecolor())
    plt.close(fig)

    print(f"✅ Previsão salva como '{output_path}'")

def graph_better_round(better_round):
    # Ordena os dados e reseta o índice para garantir alinhamento com as barras
    better_round = better_round.sort_values('Saldo de Gols', ascending=True).reset_index(drop=True)

    plt.figure(figsize=(10, 8))
    bars = plt.barh(better_round['Time'], better_round['Saldo de Gols'], color='skyblue')

    for i, bar in enumerate(bars):
        gols = better_round.loc[i, 'Gols Feitos']
        rodada = better_round.loc[i, 'Rodada']
        width = bar.get_width()
        plt.text(
            width + 0.2,
            bar.get_y() + bar.get_height() / 2,
            f'{gols} gols (Rodada {rodada} )',
            va='center',
            fontsize=9,
            color='black'
        )

    plt.xlabel('Saldo de Gols na Rodada Mais Produtiva')
    plt.ylabel('Times')
    plt.title('Rodada Mais Produtiva de Cada Time no Brasileirão 2024')
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()

    path_output = os.path.join(OUTPUT_IMG_DIR, "Melhor rodada.png")
    plt.savefig(path_output, dpi=300)
    plt.close() 

    print(f"✅ Gráfico salvo em: {path_output}")

