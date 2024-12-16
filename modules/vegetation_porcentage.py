import ee
from earth_images import obtener_urls_imagenes

# Autenticación e inicialización
ee.Authenticate()
ee.Initialize(project='prueba-imagen-satelital')

def porcentaje_vegetacion(longitud, latitud, fecha_inicio, fecha_fin):
    roi = ee.Geometry.Rectangle([longitud-0.03, latitud-0.03, longitud+0.03, latitud+0.03])
    
    imagenes = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED") \
        .filterBounds(roi) \
        .filterDate(fecha_inicio, fecha_fin) \
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 0.1))

    # Validar si hay imágenes disponibles
    num_imagenes = imagenes.size().getInfo()
    if num_imagenes == 0:
        print("No se encontraron imágenes disponibles para los filtros dados.")
        return []
    
    lista_imagenes = imagenes.toList(num_imagenes).getInfo()
    resultados = []

    for imagen_info in lista_imagenes:
        id_imagen = imagen_info['id']
        fecha_milisegundos = imagen_info['properties']['system:time_start']
        fecha_imagen = ee.Date(fecha_milisegundos).format('YYYY-MM-dd').getInfo()

        imagen = ee.Image(id_imagen)
        ndvi = imagen.normalizedDifference(['B8', 'B4']).rename('NDVI')
        vegetacion = ndvi.gt(0.2)

        pixeles_totales = vegetacion.reduceRegion(
            reducer=ee.Reducer.count(),
            geometry=roi,
            scale=10,
            maxPixels=1e8
        ).get('NDVI')

        pixeles_vegetacion = vegetacion.reduceRegion(
            reducer=ee.Reducer.sum(),
            geometry=roi,
            scale=10,
            maxPixels=1e8
        ).get('NDVI')

        pixeles_totales = pixeles_totales.getInfo() if pixeles_totales else 0
        pixeles_vegetacion = pixeles_vegetacion.getInfo() if pixeles_vegetacion else 0

        porcentaje_vegetacion = (pixeles_vegetacion / pixeles_totales) * 100 if pixeles_totales > 0 else 0
        resultados.append({'fecha': fecha_imagen, 'porcentaje_vegetacion': porcentaje_vegetacion})

    return resultados



# Ejemplo de uso
longitud = -70.8082
latitud = -32.9578

fecha_inicio ='2010-01-01'
fecha_fin ='2023-12-31'
print(obtener_urls_imagenes(longitud, latitud,fecha_inicio,fecha_fin))

# Uso de la función
resultados = porcentaje_vegetacion(longitud, latitud,fecha_inicio,fecha_fin)
for resultado in resultados:
    print(f"Fecha: {resultado['fecha']}, Porcentaje de vegetación: {resultado['porcentaje_vegetacion']:.2f}%")
