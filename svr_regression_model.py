from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd
import matplotlib.pyplot as plt
import joblib


def svr_regression(ruta):
    data = pd.read_csv(ruta)

    # Convertir la fecha en formato ordinal para manejar la temporalidad
    data['fecha'] = pd.to_datetime(data['fecha'].apply(lambda x: x.split('_')[0])).map(pd.Timestamp.toordinal)
    X = data[['fecha']]  # Usamos solo la fecha como característica
    y = data['vegetation_percentage']

    # Dividir los datos en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Crear y entrenar el modelo de SVR
    model = SVR(kernel='rbf')  # Usamos el kernel radial (rbf) para mayor flexibilidad
    model.fit(X_train, y_train)

    # Realizar las predicciones
    y_pred = model.predict(X_test)

    # Evaluar el modelo
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f'MSE: {mse:.2f}')
    print(f'R^2: {r2:.2f}')

    # Guardar el modelo entrenado en la carpeta 'proyecto_trujillo'
    joblib.dump(model, 'data/proyecto_trujillo/regresion_svr_model.pkl')

    # Guardar los resultados en un archivo CSV
    resultados = pd.DataFrame({
        'fecha': X_test['fecha'],  # Fecha de la predicción
        'vegetation_percentage_real': y_test,  # Porcentaje real de vegetación
        'vegetation_percentage_predicho': y_pred  # Porcentaje de vegetación predicho
    })

    resultados.to_csv('data/proyecto_trujillo/model_results.csv', index=False)

    return resultados

