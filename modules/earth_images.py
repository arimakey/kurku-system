import ee

ee.Authenticate()
ee.Initialize(project='prueba-imagen-satelital')

longitud = -70.9410125
latitud = -12.3041344

# Crea un punto de interés (POI)
poi = ee.Geometry.Point([longitud, latitud])

# Define una región de interés (ROI)
roi = ee.Geometry.Rectangle([longitud - 0.015, latitud - 0.015, longitud + 0.015, latitud + 0.015])

# Filtra la colección para obtener imágenes recientes del ROI
imagenes = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED") \
    .filterBounds(roi) \
    .filterDate('2017-03-28', '2024-09-28') \
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 5))  # Filtrar por nubes

imagen = imagenes.median()

# Visualizar la imagen con las bandas RGB de Sentinel-2
imagenrgb = imagen.visualize(**{
    'min': 0,
    'max': 2000,
    'bands': ['B4', 'B3', 'B2']
})

url = imagenrgb.getThumbURL({
    'region': roi,
    'dimensions': 800,
    'format': 'jpg'
})

# Imprimir la URL de la imagen
print(url)

