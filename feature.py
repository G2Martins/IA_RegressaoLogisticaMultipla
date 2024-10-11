# Importância das features
# Vamos pegar os coeficientes do modelo para as features
importances = np.abs(model.coef_[0])

# Como temos muitas features devido ao one-hot encoding, vamos focar no tempo de jogo (última feature)
# Nomear as features como campeões + tempo de jogo
feature_names = list(encoder.get_feature_names_out(input_features=X.columns[:-1])) + ['game_length_minutes']

# Criar um dataframe para as importâncias
feature_importance_df = pd.DataFrame({
    'feature': feature_names,
    'importance': importances
})

# Ordenar as importâncias e pegar as top 10 features
top_features = feature_importance_df.nlargest(10, 'importance')

# Gráfico 3: Importância das Features
plt.figure(figsize=(10, 6))
sns.barplot(data=top_features, x='importance', y='feature')
plt.title('Top 10 Features Mais Importantes no Modelo')
plt.xlabel('Importância')
plt.ylabel('Feature')
plt.show()
