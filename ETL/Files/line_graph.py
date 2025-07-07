import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Base: pasta onde o script está
BASE_DIR = os.path.dirname(__file__)
# Caminho para arquivos de entrada (Excel)
INPUT_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "Created_File"))
# Caminho para salvar imagens
OUTPUT_IMG_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "img"))

def plot_evolucao_top5(filepath: str, sheet_name: str = "Rodadas-2024", limite_rodada: int = 14, filename: str = "indicadores_top5_linha.png"):
    """
    Gera e salva um gráfico de linha com a evolução de pontos acumulados
    dos 5 melhores times até a rodada especificada.

    Parâmetros:
    - filepath: caminho para o arquivo Excel
    - sheet_name: nome da aba com os dados de rodadas
    - limite_rodada: rodada máxima para considerar (inclusiva)
    - filename: nome do arquivo de saída do gráfico (salvo dentro de OUTPUT_IMG_DIR)
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
    final_vals = pivot.iloc[-1].sort_values(ascending=False)
    pivot = pivot[final_vals.index]

    # Garante pasta de saída
    os.makedirs(OUTPUT_IMG_DIR, exist_ok=True)

    output_path = os.path.join(OUTPUT_IMG_DIR, filename)

    plt.style.use('ggplot')
    fig, ax = plt.subplots(figsize=(12, 7), facecolor='#f5f5f5')
    pivot.plot(ax=ax, marker='o', linewidth=2)

    # Customiza aparência
    ax.set_facecolor('#f5f5f5')
    ax.grid(color='white', linestyle='-', linewidth=1.5)
    ax.set_title(f"Evolução das Equipes - Top 5 até a {limite_rodada}ª Rodada", fontsize=18, color='#222222', pad=20)
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
    plt.savefig(output_path, dpi=300, facecolor=plt.gcf().get_facecolor(), bbox_inches='tight', pad_inches=0.1)
    plt.close()

def performance_analysis_use(general_performance):
    fig, ax = plt.subplots(figsize=(10, 6))

    # Largura das barras
    bar_width = 0.2

    # Posições das barras
    r1 = range(len(general_performance))
    r2 = [x + bar_width for x in r1]
    r3 = [x + bar_width for x in r2]

    # Criar barras
    ax.bar(r1, general_performance['PontosEmCasa'], color='blue', width=bar_width, edgecolor='grey', label='Pontos em Casa')
    ax.bar(r2, general_performance['PontosFora'], color='orange', width=bar_width, edgecolor='grey', label='Pontos Fora')
    ax.bar(r3, general_performance['PontosTotais'], color='green', width=bar_width, edgecolor='grey', label='Pontos Totais')

    # Adicionar labels
    ax.set_xlabel('Times')
    ax.set_ylabel('Pontos')
    ax.set_title('Desempenho Geral dos Times\nPontos ganhos em jogos', fontsize=14)
    ax.set_xticks([r + bar_width for r in range(len(general_performance))])
    ax.set_xticklabels(general_performance['Nome dos Time'])

    # Adicionar legenda e grid
    ax.legend()
    ax.grid(axis='y')

    # Exibir gráfico
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_IMG_DIR, "Pontuacao.png"), dpi=300)
    print("✅ Gráfico salvo em 'img/Pontuacao'")

def analysis_by_goal(gols):
    ig, ax = plt.subplots(figsize=(12, 8))

# Largura das barras
    bar_width = 0.2

    # Posições das barras
    r1 = range(len(gols))
    r2 = [x + bar_width for x in r1]
    r3 = [x + bar_width for x in r2]
    r4 = [x + bar_width for x in r3]

    # Criar as barras
    ax.bar(r1, gols['Gols Em Casa'], color='blue', width=bar_width, edgecolor='grey', label='Gols Em Casa')
    ax.bar(r2, gols['Gols Fora'], color='orange', width=bar_width, edgecolor='grey', label='Gols Fora')
    ax.bar(r3, gols['Gols Sofridos Em Casa'], color='green', width=bar_width, edgecolor='grey', label='Gols Sofridos Em Casa')
    ax.bar(r4, gols['Gols Sofridos Fora'], color='red', width=bar_width, edgecolor='grey', label='Gols Sofridos Fora')

    # Adicionando rótulos e títulos
    ax.set_xlabel('Times')
    ax.set_ylabel('Gols')
    ax.set_title('Desempenho de Gols dos Times')
    ax.set_xticks([r + 1.5 * bar_width for r in range(len(gols))])
    ax.set_xticklabels(gols['Time'])

    # Adicionando legenda e grid
    ax.legend()
    ax.grid(axis='y')

    # Mostrar gráfico
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    gols.to_excel("/home/carlos/ReviewTrybe/ETL/Created_File/Pontuacao Gol.xlsx", index=False)
    plt.savefig(os.path.join(OUTPUT_IMG_DIR, "Pontuacao Gol.png"), dpi=300)
    print("✅ Gráfico salvo em 'img/Pontuacao Gol'")

def analysis_performance_home(points_general):
    corr1 = points_general['VitoriasEmCasa'].corr(points_general['Gols Sofridos Em Casa'])
    fig, ax = plt.subplots()

    # Scatter plot original
    ax.scatter(points_general['VitoriasEmCasa'], points_general['Gols Sofridos Em Casa'])
    ax.set_title(f'Vitorias Em Casa vs. Gols Sofridos Em Casa')
    ax.set_xlabel('Vitorias Em Casa')
    ax.set_ylabel('Gols Sofridos Em Casa')

    # Eixo Y direito com nomes dos times
    ax2 = ax.twinx()
    ax2.set_ylim(ax.get_ylim())  # Garante que os limites fiquem iguais
    ax2.set_yticks(points_general['Gols Sofridos Em Casa'])
    ax2.set_yticklabels(points_general['Nome dos Time'])  # Substitua por points_general['Equipe'] se for o nome da coluna

    # Remove a marcação do eixo da direita para não ficar poluído
    ax2.tick_params(axis='y', which='both', length=0)

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_IMG_DIR, "Desempenho em casa.png"), dpi=300)
    plt.close()
    print("✅ Gráfico salvo em 'img/Analise Desempenho em Casa'")
    # corr1 = points_general['VitoriasEmCasa'].corr(points_general['Gols Sofridos Em Casa'])
    # plt.scatter(points_general['VitoriasEmCasa'], points_general['Gols Sofridos Em Casa'])
    # plt.title(f'VitoriasEmCasa vs. Gols Sofridos Em Casa (correlação: {corr1:.2f})')
    # plt.xlabel('VitoriasEmCasa')
    # plt.ylabel('Gols Sofridos Em Casa')
    # plt.savefig(os.path.join(OUTPUT_IMG_DIR, "Desempenho em casa.png"), dpi=300)
    # plt.close() 
    # print("✅ Gráfico salvo em 'img/Analise Desempenho em Casa'")

def analysis_win_out(points_general):
    corr2 = points_general['VitoriasFora'].corr(points_general['Gols Fora'])
    plt.scatter(points_general['VitoriasFora'], points_general['Gols Fora'])
    plt.title(f'VitoriasFora vs. Gols Fora (correlação: {corr2:.2f})')
    plt.xlabel('Vitorias Fora')
    plt.ylabel('Gols Fora')
    plt.savefig(os.path.join(OUTPUT_IMG_DIR, "Desempenho fora.png"), dpi=300)
    plt.close() 
    print("✅ Gráfico salvo em 'img/Analise Desempenho fora'")

def point_home_out(points_general):
  teams = points_general['Nome dos Time']
  vitorias_em_casa = points_general['VitoriasEmCasa']
  vitorias_fora = points_general['VitoriasFora']
    
    # Criando array de índices para os times
  teams_array = np.arange(len(teams))
    
    # Configurações do gráfico
  fig, ax = plt.subplots()
  bar_width = 0.35
    
  ax.bar(teams_array - bar_width/2, vitorias_em_casa, bar_width, label='Vitórias Em Casa')
  ax.bar(teams_array + bar_width/2, vitorias_fora, bar_width, label='Vitórias Fora')
    
  ax.set_xlabel('Times')
  ax.set_ylabel('Vitórias')
  ax.set_title('Comparação de Vitórias em Casa/Fora')
  ax.set_xticks(teams_array)
  ax.set_xticklabels(teams, rotation=45, ha='right')
  ax.legend()
    
    # Ajustando layout e salvando
  plt.tight_layout()
  plt.savefig(os.path.join(OUTPUT_IMG_DIR, "Pontos_em_casa_fora.png"), dpi=300)
  plt.close()
    
  print("✅ Gráfico salvo em 'img/Pontos_em_casa_fora'")

def plot_with_regression(points_general):
    # Extraindo dados
    vitorias_em_casa = points_general['VitoriasEmCasa']
    gols_sofridos_em_casa = points_general['Gols Sofridos Em Casa']
    
    # Criando o gráfico de dispersão
    plt.scatter(vitorias_em_casa, gols_sofridos_em_casa, label='Dados')
    
    # Calculando a linha de regressão
    coef = np.polyfit(vitorias_em_casa, gols_sofridos_em_casa, 1)
    poly1d_fn = np.poly1d(coef)
    
    # Desenhando a linha de regressão
    plt.plot(vitorias_em_casa, poly1d_fn(vitorias_em_casa), color='red', label='Linha de Regressão')
    
    # Configurações do gráfico
    plt.xlabel('Vitórias Em Casa')
    plt.ylabel('Gols Sofridos Em Casa')
    plt.title('Vitórias Em Casa vs. Gols Sofridos Em Casa')
    plt.legend()
    
    # Ajustando layout e salvando
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_IMG_DIR, "Regressao_vitorias_gols.png"), dpi=300)
    plt.close()
    
    print("✅ Gráfico com regressão salvo em 'img/Regressao_vitorias_gols'")
