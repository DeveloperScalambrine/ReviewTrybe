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


paths = [
    os.path.join(INPUT_DIR, 'Brasileiro_2024.xlsx'),
    os.path.join(INPUT_DIR, 'Tables.xlsx'),
    os.path.join(INPUT_DIR, 'Records_Points.xlsx'),
    os.path.join(INPUT_DIR, 'Points.xlsx'),
    
]

def read(table, type_file):
   
    readers = {
        'csv': pd.read_csv,
        'excel': pd.read_excel,
        'json': pd.read_json,
        'parquet': pd.read_parquet,
        'html': pd.read_html,
        'feather': pd.read_feather,
        'stata': pd.read_stata
        # Adicione outros formatos aqui se necessário
    }

    if type_file not in readers:
        raise ValueError(f"Tipo de arquivo '{type_file}' não suportado.")

    df = readers[type_file](table)
    
    return df

def analyze_Per_Team():
    df = read(paths[0], "excel")
    
    df['JOGO'] = df['JOGO'].astype(str)
    df[['TimeMandante', 'UF_M', 'Gols_M', 'Gols_V', 'TimeVisitante', 'UF_V']] = df['JOGO'].str.extract(
    r'^(.*?)\s+([A-Z]{2})\s+(\d+)\s+x\s+(\d+)\s+(.*?)\s+([A-Z]{2})$'
    )

    mask_invalid = df[['TimeMandante', 'UF_M', 'Gols_M', 'Gols_V', 'TimeVisitante', 'UF_V']].isnull().any(axis=1)
    df_error_extract = df[mask_invalid]

    df['GolMandante'] = df['TimeMandante'].str.strip() + ' ' + df['UF_M'] + ' - ' + df['Gols_M']
    df['GolVisitante'] = df['TimeVisitante'].str.strip() + ' ' + df['UF_V'] + ' - ' + df['Gols_V']

    # Cria colunas com os textos formatados
    df['GolMandante'] = df['TimeMandante'].str.strip() + ' ' + df['UF_M'] + ' - ' + df['Gols_M']
    df['GolVisitante'] = df['TimeVisitante'].str.strip() + ' ' + df['UF_V'] + ' - ' + df['Gols_V']

    df['ROD_NUM'] = df['ROD'].str.extract(r'(\d+)').astype(int)

# Filtra do início até a segunda rodada
    df_filter_2rod = df[df['ROD_NUM'] <= 10]

    principal = df_filter_2rod[df_filter_2rod['GolMandante'].str.contains(r'^São Paulo SP', regex=True)]

    visitor = df_filter_2rod[df_filter_2rod['GolVisitante'].str.contains(r'^São Paulo SP', regex=True)]

    gols_principal = principal['GolMandante'].str.extract(r' - (\d+)$').astype(int).sum().values[0]
    gols_visitor = visitor['GolVisitante'].str.extract(r' - (\d+)$').astype(int).sum().values[0]

    total_gols_sp = gols_principal + gols_visitor

    return df

def analyze_Gol_Per_Round(graph_func=None):
    df = analyze_Per_Team()

    # Filtra São Paulo como mandante e visitante
    sp_mandante = df[df['GolMandante'].str.strip().str.contains(r'^São Paulo SP', case=False, regex=True)].copy()
    sp_visitante = df[df['GolVisitante'].str.strip().str.contains(r'^São Paulo SP', case=False, regex=True)].copy()

    sp_mandante['GOLS'] = sp_mandante['GolMandante'].str.extract(r'(\d+)$').astype(int)
    sp_mandante['TIME'] = 'São Paulo SP'
    sp_mandante['TIPO'] = 'Mandante'

    sp_visitante['GOLS'] = sp_visitante['GolVisitante'].str.extract(r'(\d+)$').astype(int)
    sp_visitante['TIME'] = 'São Paulo SP'
    sp_visitante['TIPO'] = 'Visitante'

    # Junta os dois dataframes
    sp_total = pd.concat([sp_mandante, sp_visitante])

    sp_total['ROD_NUM'] = sp_total['ROD_NUM'].astype(int)

    gols_por_rodada = sp_total.groupby('ROD_NUM')['GOLS'].sum()

    rodada_max = gols_por_rodada.idxmax()
    rodada_min = gols_por_rodada.idxmin()
    
    if graph_func:
       graph_func(gols_por_rodada, rodada_max, rodada_min)
    
    return gols_por_rodada, rodada_max, rodada_min

def analyze_Per_Round(round):
    df = analyze_Per_Team()
    df_filter_round = df[df['ROD_NUM'] == round]

# Para acessar uma aba específica por nome passa o nome da aba no segundo parametro
def reading_tabs(graph_func=None):

    all_tabs = pd.read_excel(paths[1], sheet_name=None)
    if graph_func:
       graph_func(all_tabs)

    return  all_tabs
    
    # points_general = all_tabs.get("Points")
    # points = all_tabs.get("Records_Points")
    # df_rounds = all_tabs.get("Rodadas-2024")
    # df_classification = all_tabs.get("Classificação")
    # df_classification.columns = df_classification.columns.str.strip()
    # top_five = df_classification.sort_values(by="Pontos", ascending=False).head(5)

def better_team(graph_func=None):
    df = analyze_Per_Team()  
    # Etapa de preparação
    df['ROD_NUM'] = df['ROD'].str.extract(r'(\d+)').astype(int)
    df = df[df['ROD_NUM'] <= 14].copy()
    df['Gols_M'] = df['Gols_M'].astype(int)
    df['Gols_V'] = df['Gols_V'].astype(int)

    # Nome dos times
    df['Mandante'] = df['TimeMandante'].str.strip() + ' ' + df['UF_M']
    df['Visitante'] = df['TimeVisitante'].str.strip() + ' ' + df['UF_V']

    # Mandantes
    principal = df[['Mandante', 'Gols_M', 'Gols_V']].copy()
    principal.columns = ['Time', 'GolsFeitos', 'GolsSofridos']
    principal['Vitoria'] = (principal['GolsFeitos'] > principal['GolsSofridos']).astype(int)
    principal['Empate'] = (principal['GolsFeitos'] == principal['GolsSofridos']).astype(int)
    principal['PartidasMandante'] = 1
    principal['PartidasVisitante'] = 0

    # Visitantes
    visitor = df[['Visitante', 'Gols_V', 'Gols_M']].copy()
    visitor.columns = ['Time', 'GolsFeitos', 'GolsSofridos']
    visitor['Vitoria'] = (visitor['GolsFeitos'] > visitor['GolsSofridos']).astype(int)
    visitor['Empate'] = (visitor['GolsFeitos'] == visitor['GolsSofridos']).astype(int)
    visitor['PartidasMandante'] = 0
    visitor['PartidasVisitante'] = 1

    # Junta tudo
    df_total = pd.concat([principal, visitor])

    # Agrupa por time
    summary = df_total.groupby('Time').agg({
        'GolsFeitos': 'sum',
        'PartidasMandante': 'sum',
        'PartidasVisitante': 'sum',
        'Vitoria': 'sum',
        'Empate': 'sum'
    }).reset_index()

    # Pontuação
    summary['Pontos'] = (summary['Vitoria'] * 3) + (summary['Empate'] * 1)

    # Ordena por pontos
    top5 = summary.sort_values(by='Pontos', ascending=False).head(5)

    # Converte colunas para inteiros
    cols_int = ['GolsFeitos', 'PartidasMandante', 'PartidasVisitante', 'Vitoria', 'Empate', 'Pontos']
    top5[cols_int] = top5[cols_int].astype(int)

    # Gera gráfico se função for passada
    if graph_func:
        graph_func(top5)

    return top5

def top5_filtered(df_original, top5):
    # Filtra somente os 5 melhores times
    times_top5 = top5['Time'].tolist()

    df = df_original.copy()
    df['ROD_NUM'] = df['ROD'].str.extract(r'(\d+)').astype(int)
    df = df[df['ROD_NUM'] <= 14].copy()
    df['Gols_M'] = df['Gols_M'].astype(int)
    df['Gols_V'] = df['Gols_V'].astype(int)

    df['Mandante'] = df['TimeMandante'].str.strip() + ' ' + df['UF_M']
    df['Visitante'] = df['TimeVisitante'].str.strip() + ' ' + df['UF_V']

    # Mandantes
    mandante = df[df['Mandante'].isin(times_top5)].copy()
    mandante['Time'] = mandante['Mandante']
    mandante['GolsFeitos'] = mandante['Gols_M']
    mandante['Vitoria'] = (mandante['Gols_M'] > mandante['Gols_V']).astype(int)
    mandante['Empate'] = (mandante['Gols_M'] == mandante['Gols_V']).astype(int)
    mandante['Pontos'] = mandante['Vitoria'] * 3 + mandante['Empate'] * 1

    # Visitantes
    visitante = df[df['Visitante'].isin(times_top5)].copy()
    visitante['Time'] = visitante['Visitante']
    visitante['GolsFeitos'] = visitante['Gols_V']
    visitante['Vitoria'] = (visitante['Gols_V'] > visitante['Gols_M']).astype(int)
    visitante['Empate'] = (visitante['Gols_V'] == visitante['Gols_M']).astype(int)
    visitante['Pontos'] = visitante['Vitoria'] * 3 + visitante['Empate'] * 1

    # Agrupamento
    resumo_mandante = mandante.groupby('Time').agg({
        'GolsFeitos': 'sum',
        'Pontos': 'sum'
    }).rename(columns={
        'GolsFeitos': 'GolsMandante',
        'Pontos': 'PontosMandante'
    })

    resumo_visitante = visitante.groupby('Time').agg({
        'GolsFeitos': 'sum',
        'Pontos': 'sum'
    }).rename(columns={
        'GolsFeitos': 'GolsVisitante',
        'Pontos': 'PontosVisitante'
    })

    # Junta as análises
    analise_final = resumo_mandante.join(resumo_visitante, how='outer').fillna(0).astype(int)
    analise_final['PontosTotal'] = analise_final['PontosMandante'] + analise_final['PontosVisitante']
    analise_final = analise_final.reset_index()

    return analise_final

def pred_Winner():


    df = analyze_Per_Team()
    top5_df = better_team()
    
    summary = top5_filtered(df, top5_df)
    
    summary['Jogos'] = 14

    summary['MediaPontos'] = summary['PontosTotal'] / summary['Jogos']

    summary['PontosPrevistos'] = summary['MediaPontos'] * 38

    summary['MediaPontos'] = summary['MediaPontos'].round(2).astype(float)
    summary['PontosPrevistos'] = summary['PontosPrevistos'].round().astype(int)

    LIMIT_WINNER = 79

    summary['ProbabilidadeCampeao'] = np.where(
        summary['PontosPrevistos'] >= LIMIT_WINNER, 'Alta',
        np.where(summary['PontosPrevistos'] >= 70, 'Média', 'Baixa')
    )

    return summary[['Time', 'PontosTotal', 'MediaPontos', 'PontosPrevistos', 'ProbabilidadeCampeao']]

def plot_previsao_cores_times(table, limiar_campeao=75, jogos=14, total_rodadas=38, output_path="img/previsao_pontuacao.png"):

    cores_times = {
        'Flamengo RJ': '#C80000',
        'Palmeiras SP': '#1C9240',
        'São Paulo SP': '#DF0A0A',
        'Botafogo RJ': '#000000',
        'Grêmio RS': '#0099DA',
        'Internacional RS': '#ED1B24',
        'Corinthians SP': '#111111',
        'Atlético MG': '#222222',
        'Atlético GO': '#D70000',
        'Cruzeiro MG': '#0033A0',
        'Fortaleza CE': '#004AAD',
        'Fluminense RJ': '#006600',
        'Bahia BA': '#005CA9',
        'Cuiabá MT': '#007F3E',
        'Vasco da Gama RJ': '#231F20',
        'Red Bull Bragantino SP': '#FFFFFF',
        'Juventude RS': '#007B3A',
        'Vitória BA': '#CC0000',
        'Athletico PR': '#D10000',
        'Criciúma SC': '#FFD700'
    }

    table = table.sort_values("PontosPrevistos", ascending=True)

    fig, ax = plt.subplots(figsize=(10, 6), facecolor="#f7f7f7")
    ax.set_facecolor("#f7f7f7")

    # Aplica a cor do time (ou fallback azul)
    cores = [cores_times.get(time, 'steelblue') for time in table["Time"]]

    bars = ax.barh(table["Time"], table["PontosPrevistos"], color=cores, edgecolor="white", height=0.6)

    # Linha de limiar para título
    ax.axvline(limiar_campeao, color="crimson", linestyle="--", linewidth=2,
               label=f"Limiar Campeão: {limiar_campeao} pts")

    # Anotações
    for bar, media in zip(bars, table["MediaPontos"]):
        x = bar.get_width()
        y = bar.get_y() + bar.get_height() / 2
        ax.text(x + 0.8, y,
                f"{int(x)} pts\n{media:.2f}/jogo",
                va="center", ha="left", fontsize=9, color="#222")

    ax.set_title("🎯 Previsão Final do Brasileirão 2024", fontsize=16, color="#111", pad=15)
    ax.set_xlabel(f"Pontos Previstos (após {jogos}/{total_rodadas} rodadas)", fontsize=12)
    ax.set_ylabel("Time", fontsize=12)
    ax.tick_params(axis='both', labelsize=10, colors="#333")
    ax.grid(axis="x", linestyle="--", linewidth=0.5, color="#cccccc")

    ax.legend(loc="lower right", fontsize=10, frameon=False)

    plt.tight_layout()

    # Cria a pasta do output_path caso não exista
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    # Salva a figura usando output_path
    fig.savefig(output_path, dpi=300, facecolor=fig.get_facecolor())
    plt.close(fig)

def perfor_inside_outside(graph_func=None):
    all_tabs = reading_tabs()
    # points_general = all_tabs['Points']
    # points_general_home = all_tabs['Points']
    # points_general_home_out = all_tabs['Points']
    # plot_regression = all_tabs['Points']
    round = all_tabs['Rodadas-2024']
    points_general = all_tabs['Points']
    if graph_func:
       graph_func(round, points_general)    
    return round

def round_favority(graph_func=None):
    df_round = perfor_inside_outside()

    dict = {
    ('Atlético', 'MG'): 'Atlético-MG',
    ('Atlético', 'GO'): 'Atlético-GO',
    ('Athletico', 'PR'): 'Athletico-PR',
}

    df_round['TimeMandante'] = df_round.apply(
    lambda row: dict.get((row['TimeMandante'], row['UF_M']), row['TimeMandante']),
    axis=1
)

    df_round['TimeVisitante'] = df_round.apply(
    lambda row: dict.get((row['TimeVisitante'], row['UF_V']), row['TimeVisitante']),
    axis=1
)

    home = df_round[['ROD_NUM', 'TimeMandante', 'Gols_M', 'Gols_V']].copy()
    home.columns = ['Rodada', 'Time', 'Gols Feitos', 'Gols Sofridos']
    home['Pontos'] = home.apply(
        lambda x: 3 if x['Gols Feitos'] > x['Gols Sofridos'] else 0,
        axis=1
    )
    home['Local'] = 'Casa'

    visitor = df_round[['ROD_NUM', 'TimeVisitante', 'Gols_V', 'Gols_M']].copy()
    visitor.columns = ['Rodada', 'Time', 'Gols Feitos', 'Gols Sofridos']
    visitor['Pontos'] =visitor.apply(
        lambda x: 3 if x['Gols Feitos'] > x['Gols Sofridos'] else 0,
        axis=1
    )
    visitor['Local'] = 'Fora'

    all_games = pd.concat([home,visitor], ignore_index=True)

    all_games['Saldo de Gols'] = all_games['Gols Feitos'] - all_games['Gols Sofridos']

    vitorias = all_games[
        (all_games['Pontos'] == 3) &
        (all_games['Saldo de Gols'] > 0)
    ]

    better_round = (
        vitorias.sort_values(['Time', 'Saldo de Gols'], ascending=[True, False])
        .drop_duplicates(subset='Time')
        .reset_index(drop=True)
    )
    if graph_func:
       graph_func(better_round)

    return better_round




    #UMA ANALISE
    # performance_analysis_use = points[['Nome dos Time', 'VitoriasEmCasa', 'VitoriasFora', 'PontosEmCasa', 'PontosFora', 'PontosTotais']]
    # if graph_func:
    #   graph_func(performance_analysis_use)
    # return performance_analysis_use
    

    #OUTRA ANALISE
    # df['TimeMandante'] = df['TimeMandante'] + " (" + df['UF_M'] + ")"
    # df['TimeVisitante'] = df['TimeVisitante'] + " (" + df['UF_V'] + ")"

    # goal_of_home = df.groupby('TimeMandante')['Gols_M'].sum().reset_index()
    # goal_of_home.columns = ['Time', 'Gols Em Casa']

    # goal_out = df.groupby('TimeVisitante')['Gols_V'].sum().reset_index()
    # goal_out.columns = ['Time', 'Gols Fora']

    # goal_conceded_home = df.groupby('TimeMandante')['Gols_V'].sum().reset_index()
    # goal_conceded_home.columns = ['Time', 'Gols Sofridos Em Casa']

    # gols_sofridos_fora = df.groupby('TimeVisitante')['Gols_M'].sum().reset_index()
    # gols_sofridos_fora.columns = ['Time', 'Gols Sofridos Fora']

    # gols = pd.merge(goal_of_home, goal_out, on='Time', how='outer')
    # gols = pd.merge(gols, goal_conceded_home, on='Time', how='outer')
    # gols = pd.merge(gols, gols_sofridos_fora, on='Time', how='outer')

    # gols = gols.fillna(0)

    # if graph_func:
    #     graph_func(gols)
    
    # return gols
    
    # visao estatistica das colunas 
    # print(df.describe())


    #somar e tirar a media dos pontos em casa e fora
    # soma_casa = points['PontosEmCasa'].sum()
    # media_casa = points['PontosEmCasa'].mean()

    # soma_fora = points['PontosFora'].sum()
    # media_fora = points['PontosFora'].mean()

    
    #Analisar o número de vitórias, derrotas e empates em casa e fora:
    # vitorias_casa = points['VitoriasEmCasa']
    # vitorias_fora = points['VitoriasFora'].sum()

    # derrotas_casa = points['DerrotasEmCasa'].sum()
    # derrotas_fora = points['DerrotasFora'].sum()

    # empates_casa = points['EmpatesEmCasa'].sum()
    # empates_fora = points['EmpatesFora'].sum()

    # times_com_vitoria_em_casa =  points['Nome dos Time']
    # times_com_vitoria_em_casa = vitorias_casa
    
    # print("Vitórias em Casa:", vitorias_casa, "Vitórias Fora:", vitorias_fora)
    # print("Derrotas em Casa:", derrotas_casa, "Derrotas Fora:", derrotas_fora)
    # print("Empates em Casa:", empates_casa, "Empates Fora:", empates_fora)    
    # print(f"Soma Pontos em Casa: {soma_casa}, Média Pontos em Casa: {media_casa}")
    # print(f"Soma Pontos Fora: {soma_fora}, Média Pontos Fora: {media_fora}")
    
    #ANALISE FINAL SOBRE DESEMPENHO EM CASA USANDO COMO PARAMETROS
    # PONTOS EM CASA E PONTOS FORA 
  
   # Melhor desempenho em casa
#     melhor_casa = points.loc[points['PontosEmCasa'].idxmax()]
#     nome_melhor_casa = melhor_casa['Nome dos Time']
#     pontos_melhor_casa = melhor_casa['PontosEmCasa']

#     # Melhor desempenho fora
#     melhor_fora = points.loc[points['PontosFora'].idxmax()]
#     nome_melhor_fora = melhor_fora['Nome dos Time']
#     pontos_melhor_fora = melhor_fora['PontosFora']

#     # Pior desempenho em casa
#     pior_casa = points.loc[points['PontosEmCasa'].idxmin()]
#     nome_pior_casa = pior_casa['Nome dos Time']
#     pontos_pior_casa = pior_casa['PontosEmCasa']

#     # Pior desempenho fora
#     pior_fora = points.loc[points['PontosFora'].idxmin()]
#     nome_pior_fora = pior_fora['Nome dos Time']
#     pontos_pior_fora = pior_fora['PontosFora']

#     analise_desempenho = f"""
# Melhor Time em Casa: {nome_melhor_casa} com {pontos_melhor_casa} pontos
# Melhor Time Fora: {nome_melhor_fora} com {pontos_melhor_fora} pontos
# Pior Time em Casa: {nome_pior_casa} com {pontos_pior_casa} pontos
# Pior Time Fora: {nome_pior_fora} com {pontos_pior_fora} pontos
# """
#     return analise_desempenho

    # # Cálculo do total de gols como mandante incluindo UF
    # gols_mandante = df.groupby(['TimeMandante', 'UF_M'], as_index=False).agg(
    #     Gols_M=('Gols_M', 'sum')
    # )

    # # Cálculo do total de gols como visitante incluindo UF
    # gols_visitante = df.groupby(['TimeVisitante', 'UF_V'], as_index=False).agg(
    #     Gols_V=('Gols_V', 'sum')
    # )

    # # Calcula a média de gols como mandante
    # media_gols_mandante = gols_mandante['Gols_M'].mean()

    # # Calcula a média de gols como visitante
    # media_gols_visitante = gols_visitante['Gols_V'].mean()

    # # Calcula média total
    # media_total_gols = (gols_mandante['Gols_M'].sum() + gols_visitante['Gols_V'].sum()) / (len(gols_mandante) + len(gols_visitante))

    # # Encontra menor e maior total de gols como mandante
    # menor_gols_mandante = gols_mandante.loc[gols_mandante['Gols_M'].idxmin()]
    # maior_gols_mandante = gols_mandante.loc[gols_mandante['Gols_M'].idxmax()]

    # # Encontra menor e maior total de gols como visitante
    # menor_gols_visitante = gols_visitante.loc[gols_visitante['Gols_V'].idxmin()]
    # maior_gols_visitante = gols_visitante.loc[gols_visitante['Gols_V'].idxmax()]

    # # Formatar a análise em uma string
    # analise_aproveitamento = f"""
    # Menor aproveitamento como mandante: {menor_gols_mandante['TimeMandante']} ({menor_gols_mandante['UF_M']}) com {menor_gols_mandante['Gols_M']} gols
    # Maior aproveitamento como mandante: {maior_gols_mandante['TimeMandante']} ({maior_gols_mandante['UF_M']}) com {maior_gols_mandante['Gols_M']} gols
    # Média de gols como mandante: {media_gols_mandante:.2f} gols

    # Menor aproveitamento como visitante: {menor_gols_visitante['TimeVisitante']} ({menor_gols_visitante['UF_V']}) com {menor_gols_visitante['Gols_V']} gols
    # Maior aproveitamento como visitante: {maior_gols_visitante['TimeVisitante']} ({maior_gols_visitante['UF_V']}) com {maior_gols_visitante['Gols_V']} gols
    # Média de gols como visitante: {media_gols_visitante:.2f} gols

    # Média total de gols: {media_total_gols:.2f} gols
    # """

