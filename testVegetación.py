from modules.earth_images import calcular_porcentaje_vegetacion_y_url

longitud = -80.2004555
latitud = -5.0948108
fecha_inicio = '2024-01-01'
fecha_fin = '2024-12-31'

porcentaje, url_imagen = calcular_porcentaje_vegetacion_y_url(longitud, latitud, fecha_inicio, fecha_fin)
print(f"El porcentaje de vegetación es: {porcentaje}%")
print(f"URL de la imagen NDVI: {url_imagen}")
