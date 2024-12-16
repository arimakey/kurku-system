import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import joblib

def random_forest(ruta,destino):

    data = pd.read_csv(ruta)

    # Convertir la fecha en formato ordinal para manejar la temporalidad
    data['fecha'] = pd.to_datetime(data['fecha'].apply(lambda x: x.split('_')[0])).map(pd.Timestamp.toordinal)
    X = data[['fecha']]  # Usamos solo la fecha como característica
    y = data['vegetation_percentage']

    # Dividir los datos en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Crear y entrenar el modelo Random Forest
    model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
    model.fit(X_train, y_train)

    # Realizar las predicciones
    y_pred = model.predict(X_test)

    # Evaluar el modelo
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    # Guardar el modelo entrenado
    joblib.dump(model, 'data/proyecto_trujillo/random_forest_model.pkl')

    # Crear el DataFrame con los resultados
    resultados = pd.DataFrame({
        'fecha': X_test['fecha'],
        'vegetation_percentage_real': y_test,
        'vegetation_percentage_predicho': y_pred 
    })
    resultados.to_csv(destino, index=False)

    return resultados


