# arquivo: plot_evolution.py
import os
import pandas as pd
import matplotlib.pyplot as plt

def plot_evolucao_top5(filepath: str, sheet_name: str = "Rodadas-2024", limite_rodada: int = 14, output_path: str = "img/indicadores_top5_linha.png"):
    """
    Gera e salva um gráfico de linha com a evolução de pontos acumulados
    dos 5 melhores times até a rodada especificada.

    Parâmetros:
    - filepath: caminho para o arquivo Excel
    - sheet_name: nome da aba com os dados de rodadas
    - limite_rodada: rodada máxima para considerar (inclusiva)
    - output_path: caminho do arquivo de saída do gráfico
    """
    # Carrega os dados
    df = pd.read_excel(filepath, sheet_name=sheet_name)

    # Remove linha inicial e preenche rodadas
    df = df.drop(index=0).reset_index(drop=True)
    df['ROD'] = df['ROD'].ffill()
    df['ROD_NUM'] = df['ROD'].str.extract(r'(\d+)').astype(int)

    # Converte gols e filtra rodadas
    df['Gols_M'] = df['Gols_M'].astype(int)
    df['Gols_V'] = df['Gols_V'].astype(int)
    df = df[df['ROD_NUM'] <= limite_rodada]

    # Normaliza nomes de times
    df['TimeMandante'] = df['TimeMandante'].str.strip() + ' ' + df['UF_M']
    df['TimeVisitante'] = df['TimeVisitante'].str.strip() + ' ' + df['UF_V']

    # Pontos por jogo
    df['Pontos_M'] = df.apply(lambda r: 3 if r['Gols_M'] > r['Gols_V'] else 1 if r['Gols_M'] == r['Gols_V'] else 0, axis=1)
    df['Pontos_V'] = df.apply(lambda r: 3 if r['Gols_V'] > r['Gols_M'] else 1 if r['Gols_V'] == r['Gols_M'] else 0, axis=1)

    # Prepara DataFrame unificado
    mand = df[['ROD_NUM', 'TimeMandante', 'Pontos_M']].rename(columns={'TimeMandante': 'Time', 'Pontos_M': 'Pontos'})
    vis = df[['ROD_NUM', 'TimeVisitante', 'Pontos_V']].rename(columns={'TimeVisitante': 'Time', 'Pontos_V': 'Pontos'})
    pont = pd.concat([mand, vis])

    # Seleciona top 5 por pontos totais
    soma_pontos = pont.groupby('Time')['Pontos'].sum()
    top5 = soma_pontos.nlargest(5).index.tolist()
    pont = pont[pont['Time'].isin(top5)].sort_values(by=['Time', 'ROD_NUM'])

    # Calcula acumulado por rodada
    pont['PontosAcumulados'] = pont.groupby('Time')['Pontos'].cumsum()

    # Pivot para gráfico
    pivot = pont.pivot(index='ROD_NUM', columns='Time', values='PontosAcumulados').fillna(method='ffill').fillna(0)

    # Garante pasta de saída
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Plota
    # plt.figure(figsize=(12, 7))
    # pivot.plot(marker='o', linewidth=2)
    # plt.title(f"Evolução das Equipes - Top 5 até a {limite_rodada}ª Rodada")
    # plt.xlabel("Rodada")
    # plt.ylabel("Pontos Acumulados")
    # plt.grid(True)
    # plt.legend(title='Time', bbox_to_anchor=(1.05, 1), loc='upper left')
    # plt.gca().yaxis.tick_right()
    # plt.tight_layout()
    # plt.savefig(output_path, dpi=300)
    # plt.close()

    plt.style.use('ggplot')
    fig, ax = plt.subplots(figsize=(12, 7), facecolor='#f5f5f5')
    pivot.plot(ax=ax, marker='o', linewidth=2)

    # Customiza aparência
    ax.set_facecolor('#f5f5f5')
    ax.grid(color='white', linestyle='-', linewidth=1.5)
    ax.set_title(f"Evolução dos Pontos Acumulados - Top 5 até a {limite_rodada}ª Rodada", fontsize=18, color='#222222', pad=20)
    ax.set_xlabel("Rodada", fontsize=14, color='#333333', labelpad=10)
    ax.set_ylabel("Pontos Acumulados", fontsize=14, color='#333333', labelpad=10)
    ax.tick_params(axis='x', colors='#444444', labelsize=12)
    ax.tick_params(axis='y', colors='#444444', labelsize=12)
    ax.legend(title='Time', title_fontsize=12, fontsize=11, frameon=False, loc='upper left', bbox_to_anchor=(1.02,1))

    # Anota valores finais
    max_rod = pivot.index.max()
    for team in pivot.columns:
        y = pivot.at[max_rod, team]
        ax.text(max_rod + 0.2, y, str(int(y)), color='#222222', va='center', fontweight='bold')

    plt.tight_layout()
    fig.savefig(output_path, dpi=300, facecolor=fig.get_facecolor())
    plt.close(fig)