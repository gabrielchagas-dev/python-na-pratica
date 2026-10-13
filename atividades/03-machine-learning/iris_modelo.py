# %% Bibliotecas e carregamento do Iris
import json
import tensorflow as tf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix, classification_report

tf.keras.utils.set_random_seed(42)
tf.config.experimental.enable_op_determinism()
tf.config.threading.set_inter_op_parallelism_threads(1)
tf.config.threading.set_intra_op_parallelism_threads(1)
iris = load_iris()
X, y = iris.data, iris.target
df = pd.DataFrame(X, columns=iris.feature_names)
df['especie'] = [iris.target_names[i] for i in y]
print('DADOS IRIS:', X.shape, '| classes:', iris.target_names.tolist())
print(df.head().to_string(index=False))

# %% Divisão estratificada e padronização sem vazamento de dados
X_treino_total, X_teste, y_treino_total, y_teste = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y)
X_treino, X_validacao, y_treino, y_validacao = train_test_split(
    X_treino_total, y_treino_total, test_size=0.20, random_state=42,
    stratify=y_treino_total)
scaler = StandardScaler()
X_treino_pad = scaler.fit_transform(X_treino).astype('float32')
X_validacao_pad = scaler.transform(X_validacao).astype('float32')
X_teste_pad = scaler.transform(X_teste).astype('float32')
print(f'Treino: {len(X_treino)}; validação: {len(X_validacao)}; teste: {len(X_teste)}')

# %% Construção e treinamento da rede neural TensorFlow
modelo = tf.keras.Sequential([
    tf.keras.Input(shape=(4,)),
    tf.keras.layers.Dense(16, activation='relu'),
    tf.keras.layers.Dense(8, activation='relu'),
    tf.keras.layers.Dense(3, activation='softmax'),
])
modelo.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.01),
               loss='sparse_categorical_crossentropy', metrics=['accuracy'])
modelo.summary()
parada = tf.keras.callbacks.EarlyStopping(
    monitor='val_loss', patience=15, restore_best_weights=True)
historico = modelo.fit(
    X_treino_pad, y_treino, validation_data=(X_validacao_pad, y_validacao),
    epochs=150, batch_size=16, verbose=0, callbacks=[parada])
print('Épocas executadas:', len(historico.history['loss']))

# %% Avaliação única no conjunto de teste reservado
perda, acuracia = modelo.evaluate(X_teste_pad, y_teste, verbose=0)
probabilidades = modelo.predict(X_teste_pad, verbose=0)
predicoes = probabilidades.argmax(axis=1)
matriz = confusion_matrix(y_teste, predicoes)
print(f'Perda no teste: {perda:.4f}; acurácia: {acuracia:.2%}')
print('Matriz de confusão (linhas reais, colunas previstas):\n', matriz)
print(classification_report(y_teste, predicoes,
      target_names=iris.target_names, zero_division=0))
fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(historico.history['loss'], label='Treino')
ax.plot(historico.history['val_loss'], label='Validação')
ax.set(title='Evolução da perda no treinamento', xlabel='Época', ylabel='Perda')
ax.legend()
fig.tight_layout()
fig.savefig('treinamento_iris.png', dpi=180)
plt.show()

# %% Previsões de três novas entradas demonstrativas
novas_flores = np.array([[5.1, 3.5, 1.4, 0.2],
                        [6.0, 2.9, 4.5, 1.5],
                        [6.5, 3.0, 5.8, 2.2]])
probs = modelo.predict(scaler.transform(novas_flores).astype('float32'), verbose=0)
previsoes_novas = []
for medidas, p in zip(novas_flores, probs):
    especie = str(iris.target_names[int(p.argmax())])
    previsoes_novas.append(especie)
    print(f'Medidas {medidas.tolist()} -> {especie}; probabilidades {p.round(4).tolist()}')
assert len(y_teste) == 30 and matriz.sum() == 30
assert np.isfinite(probabilidades).all()
assert np.allclose(probabilidades.sum(axis=1), 1, atol=1e-5)
assert np.allclose(X_treino_pad.mean(axis=0), 0, atol=1e-5)
print('TESTES: divisão, padronização e probabilidades conferidas.')
modelo.save('modelo_iris.keras')
with open('resultados.json', 'w', encoding='utf-8') as arquivo:
    json.dump({'treino': len(y_treino), 'validacao': len(y_validacao), 'teste': len(y_teste),
               'epocas': len(historico.history['loss']), 'perda': float(perda),
               'acuracia': float(acuracia), 'matriz': matriz.tolist(),
               'previsoes': previsoes_novas}, arquivo, indent=2, ensure_ascii=False)
