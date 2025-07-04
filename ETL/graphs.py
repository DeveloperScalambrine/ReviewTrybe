import pandas as pd
import matplotlib.pyplot as plt
import os

from sklearn.linear_model import LinearRegression
import numpy as np

path_excel = "File/Tables.xlsx" 


if not os.path.exists(path_excel):
    raise FileNotFoundError(f"Arquivo não encontrado: {path_excel}")

df_classificacao = pd.read_excel(path_excel, sheet_name="Classificação")

# Remove espaços extras nos nomes das colunas
df_classificacao.columns = df_classificacao.columns.str.strip()

# Ordena os times por Pontos e seleciona os 5 primeiros
top5 = df_classificacao.sort_values(by="Pontos", ascending=False).head(5)

# Cria o gráfico
plt.figure(figsize=(10, 6))
plt.bar(top5["Nome dos Times"], top5["Pontos"], color="royalblue")
plt.title("Top 5 Times - Pontuação")
plt.xlabel("Times")
plt.ylabel("Pontos")
plt.xticks(rotation=45)
plt.tight_layout()

# Salva o gráfico
# plt.savefig("img/top5_pontos_classificacao.png", dpi=300)
# print("✅ Gráfico salvo em 'graphs/top5_pontos_classificacao.png'")

#     # Gerando Grafico

# # if 'ROD_NUM' not in df.columns:
# #     df['ROD_NUM'] = df['ROD'].str.extract(r'(\d+)').astype(int)

# # # Filtra jogos com São Paulo SP como mandante ou visitante
# # sp_mandante = df_filter_2rod[df_filter_2rod['GolMandante'].str.contains(r'^São Paulo SP', regex=True)].copy()
# # sp_visitante = df_filter_2rod[df_filter_2rod['GolVisitante'].str.contains(r'^São Paulo SP', regex=True)].copy()

# # # Extrai gols e rodada
# # sp_mandante['GOLS'] = sp_mandante['GolMandante'].str.extract(r' - (\d+)$').astype(int)
# # sp_mandante['TIME'] = 'São Paulo SP'
# # sp_mandante['TIPO'] = 'Mandante'

# # sp_visitante['GOLS'] = sp_visitante['GolVisitante'].str.extract(r' - (\d+)$').astype(int)
# # sp_visitante['TIME'] = 'São Paulo SP'
# # sp_visitante['TIPO'] = 'Visitante'

# # # Junta os dois dataframes
# # sp_total = pd.concat([sp_mandante, sp_visitante])

# # # Agrupa por rodada e soma os gols
# # gols_por_rodada = sp_total.groupby('ROD_NUM')['GOLS'].sum()

# # # Identifica a rodada com mais e menos gols
# # rodada_max = gols_por_rodada.idxmax()
# # rodada_min = gols_por_rodada.idxmin()

# # # --- 📊 Gráfico ---
# # plt.figure(figsize=(10, 6))
# # bars = plt.bar(gols_por_rodada.index, gols_por_rodada.values, color='skyblue')

# # # Destaca as rodadas com mais e menos gols
# # bars[gols_por_rodada.index.get_loc(rodada_max)].set_color('green')
# # bars[gols_por_rodada.index.get_loc(rodada_min)].set_color('red')

# # # Rótulos
# # plt.title('Gols do São Paulo SP até a decima Rodada')
# # plt.xlabel('Rodada')
# # plt.ylabel('Gols Marcados')
# # plt.xticks(gols_por_rodada.index)

# # # Anotações
# # plt.text(rodada_max, gols_por_rodada[rodada_max] + 0.2, f'Máx: {gols_por_rodada[rodada_max]}', ha='center', color='green')
# # plt.text(rodada_min, gols_por_rodada[rodada_min] + 0.2, f'Mín: {gols_por_rodada[rodada_min]}', ha='center', color='red')

# # os.makedirs('img', exist_ok=True)

# # plt.tight_layout()
# # plt.savefig('img/grafico_sao_paulo_sp.png', dpi=300)
# # print("✅ Gráfico salvo como 'grafico_sao_paulo_sp.png'")


def better_team(df):
    # Etapa de preparação
    df['ROD_NUM'] = df['ROD'].str.extract(r'(\d+)').astype(int)
    df = df[df['ROD_NUM'] <= 14].copy()
    df['Gols_M'] = df['Gols_M'].astype(int)
    df['Gols_V'] = df['Gols_V'].astype(int)

    # Nome dos times
    df['Mandante'] = df['TimeMandante'].str.strip() + ' ' + df['UF_M']
    df['Visitante'] = df['TimeVisitante'].str.strip() + ' ' + df['UF_V']

    # Mandantes
    mandante = df[['Mandante', 'Gols_M', 'Gols_V']].copy()
    mandante.columns = ['Time', 'GolsFeitos', 'GolsSofridos']
    mandante['Vitoria'] = (mandante['GolsFeitos'] > mandante['GolsSofridos']).astype(int)
    mandante['Empate'] = (mandante['GolsFeitos'] == mandante['GolsSofridos']).astype(int)
    mandante['PartidasMandante'] = 1
    mandante['PartidasVisitante'] = 0

    # Visitantes
    visitante = df[['Visitante', 'Gols_V', 'Gols_M']].copy()
    visitante.columns = ['Time', 'GolsFeitos', 'GolsSofridos']
    visitante['Vitoria'] = (visitante['GolsFeitos'] > visitante['GolsSofridos']).astype(int)
    visitante['Empate'] = (visitante['GolsFeitos'] == visitante['GolsSofridos']).astype(int)
    visitante['PartidasMandante'] = 0
    visitante['PartidasVisitante'] = 1

    # Junta tudo
    df_total = pd.concat([mandante, visitante])

    # Agrupa
    resumo = df_total.groupby('Time').agg({
        'GolsFeitos': 'sum',
        'PartidasMandante': 'sum',
        'PartidasVisitante': 'sum',
        'Vitoria': 'sum',
        'Empate': 'sum'
    }).reset_index()

    # Pontuação total
    resumo['Pontos'] = (resumo['Vitoria'] * 3) + (resumo['Empate'] * 1)

    # Ordena
    top5 = resumo.sort_values(by='Pontos', ascending=False).head(5)

    # Conversão para inteiros
    cols_int = ['GolsFeitos', 'PartidasMandante', 'PartidasVisitante', 'Vitoria', 'Empate', 'Pontos']
    top5[cols_int] = top5[cols_int].astype(int)

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

def pred_Winner(df_original, top5):
    summary = top5_filtered(df_original, top5)

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

def plot_previsao(table):
    plt.figure(figsize=(10, 6))
    bars = plt.bar(table['Time'], table['PontosPrevistos'], color='dodgerblue')

    for bar in bars:
        altura = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, altura + 0.5, f'{altura:.0f}', 
                 ha='center', va='bottom', fontsize=9)
    plt.title('🏆 Previsão de Pontuação Final - Brasileirão 2024')
    plt.xlabel('Time')
    plt.ylabel('Pontos Previstos')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('img/previsao_pontuacao.png', dpi=300)