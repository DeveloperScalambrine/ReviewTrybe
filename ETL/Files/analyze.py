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
    os.path.join(INPUT_DIR, 'Tables.xlsx')
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

    df_rounds = all_tabs["Rodadas-2024"]
    df_classification = all_tabs["Classificação"]
    df_classification.columns = df_classification.columns.str.strip()
    top_five = df_classification.sort_values(by="Pontos", ascending=False).head(5)
    
    if graph_func:
       graph_func(top_five)

    return top_five
    
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
