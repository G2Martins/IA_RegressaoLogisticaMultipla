import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import accuracy_score
import scipy.sparse as sp

# Carregar os dados
data = pd.read_csv('s11.csv')

# Função para extrair o tempo de jogo em minutos
def convert_game_length_to_minutes(game_length):
    try:
        minutes, seconds = game_length.split('m')
        return int(minutes.strip()) + int(seconds.replace('s', '').strip()) / 60
    except:
        return 0  # Caso o formato do tempo seja inesperado

# Aplicar a função de conversão ao tempo de jogo
data['game_length_minutes'] = data['game_length'].apply(convert_game_length_to_minutes)

# Selecionar as colunas dos campeões e o resultado
X = data[['team_1__001', 'team_1__002', 'team_1__003', 'team_1__004', 'team_1__005',
          'team_2__001', 'team_2__002', 'team_2__003', 'team_2__004', 'team_2__005', 'game_length_minutes']]
y = data['result'].apply(lambda x: 1 if x == 'Victory' else 0)

# One-hot encoding para representar os campeões numericamente
encoder = OneHotEncoder(handle_unknown='ignore')
X_encoded = encoder.fit_transform(X[['team_1__001', 'team_1__002', 'team_1__003', 'team_1__004', 'team_1__005',
                                     'team_2__001', 'team_2__002', 'team_2__003', 'team_2__004', 'team_2__005']])

# Incluir o tempo de jogo no conjunto de features
X_encoded = sp.hstack([X_encoded, X[['game_length_minutes']].values])

# Dividir os dados em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.3, random_state=42)

# Ajuste de pesos para balancear as classes
model = LogisticRegression(max_iter=5000, C=1, class_weight='balanced')
model.fit(X_train, y_train)

# Avaliar a acurácia do modelo
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Acurácia do modelo: {accuracy * 100:.2f}%")

# Função para prever e exibir as probabilidades
def predict_winner_with_graph(team1_champs, team2_champs, game_time_minutes):
    input_data = pd.DataFrame([[team1_champs[0], team1_champs[1], team1_champs[2], team1_champs[3], team1_champs[4],
                                team2_champs[0], team2_champs[1], team2_champs[2], team2_champs[3], team2_champs[4], game_time_minutes]],
                              columns=['team_1__001', 'team_1__002', 'team_1__003', 'team_1__004', 'team_1__005',
                                       'team_2__001', 'team_2__002', 'team_2__003', 'team_2__004', 'team_2__005', 'game_length_minutes'])

    # Aplicar o mesmo one-hot encoding
    input_encoded = encoder.transform(input_data[['team_1__001', 'team_1__002', 'team_1__003', 'team_1__004', 'team_1__005',
                                                  'team_2__001', 'team_2__002', 'team_2__003', 'team_2__004', 'team_2__005']])
    input_encoded = sp.hstack([input_encoded, input_data[['game_length_minutes']].values])

    # Prever a probabilidade
    prediction_prob = model.predict_proba(input_encoded)[0]
    prob_team_1 = prediction_prob[1]  # Probabilidade do Time 1 ganhar
    prob_team_2 = prediction_prob[0]  # Probabilidade do Time 2 ganhar

    # Exibir o gráfico com os times e as probabilidades
    fig, ax = plt.subplots(figsize=(8, 5))

    team1_text = "\n".join([f"Team 1 Champ {i+1}: {champ}" for i, champ in enumerate(team1_champs)])
    team2_text = "\n".join([f"Team 2 Champ {i+1}: {champ}" for i, champ in enumerate(team2_champs)])

    textstr = f"{team1_text}\n\n{team2_text}\n\nProbabilidade de Vitória:\nTime 1: {prob_team_1:.2f}\nTime 2: {prob_team_2:.2f}"

    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=12, verticalalignment='top', bbox=props)

    plt.title('Composição dos Times e Probabilidade de Vitória')
    plt.axis('off')  # Remover eixos
    plt.show()

    # Exibir a previsão com base na maior probabilidade
    if prob_team_1 > prob_team_2:
        print("Previsão: Time 1 vencerá!")
    else:
        print("Previsão: Time 2 vencerá!")

# Teste com times e probabilidade
team1_champs = ['Elise', 'Darius', 'Yasuo', 'Blitzcrank', 'Ashe']
team2_champs = ['Cassiopeia', "Draven", 'Aatrox', 'Aurelion Sol', 'Ahri']
game_time_minutes = 30  # Tempo de jogo em minutos

# Prever o resultado da partida entre os dois times com gráfico
predict_winner_with_graph(team1_champs, team2_champs, game_time_minutes)