import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

# Cargar los datos desde tu CSV
data = pd.read_csv('data/images/vegetation_data.csv')

# Supongamos que utilizamos una conversión simple de fecha a ordinal para manejar la temporalidad
data['fecha'] = pd.to_datetime(data['fecha'].apply(lambda x: x.split('_')[0])).map(pd.Timestamp.toordinal)
X = data[['fecha']]  # Usamos solo la fecha como característica por ahora
y = data['vegetation_percentage']

# Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Crear y entrenar el modelo Random Forest
model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

# Evaluar el modelo
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'MSE: {mse:.2f}')
print(f'R^2: {r2:.2f}')

# Opcional: Graficar los resultados
plt.scatter(X_test, y_test, color='black', label='Datos reales')
plt.scatter(X_test, y_pred, color='red', label='Predicciones')
plt.title('Comparación de Vegetación Real vs. Predicha')
plt.xlabel('Fecha (ordinal)')
plt.ylabel('Porcentaje de Vegetación')
plt.legend()
plt.show()
