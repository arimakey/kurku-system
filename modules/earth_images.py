import ee
from modules import suggestions

ee.Authenticate()
ee.Initialize(project='prueba-imagen-satelital')

def obtener_urls_imagenes(longitud=-70.4967607, latitud=-12.0545491, fecha_inicio='2024-01-01', fecha_fin='2024-12-31'):
    """
    Genera URLs de imágenes satelitales en RGB según las coordenadas y el rango de fechas.
    """
    roi = ee.Geometry.Rectangle([longitud-0.03, latitud-0.03, longitud+0.03, latitud+0.03])

    imagenes = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED") \
        .filterBounds(roi) \
        .filterDate(fecha_inicio, fecha_fin) \
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 30))

    lista_imagenes = imagenes.toList(imagenes.size()).getInfo()
    
    urls_imagenes = []
    
    for imagen_info in lista_imagenes:
        id_imagen = imagen_info['id']
        imagen = ee.Image(id_imagen)
        
        imagenrgb = imagen.visualize(**{
            'min': 0,
            'max': 2800,
            'bands': ['B4', 'B3', 'B2']
        })
        
        try:
            url = imagenrgb.getThumbURL({
                'region': roi,
                'scale': 7,
                'format': 'jpg'
            })
            urls_imagenes.append(url)
        except Exception as e:
            print(f"Error generando URL para la imagen {id_imagen}: {e}")
    
    return urls_imagenes

def get_image(longitud, latitud):
    """
    Genera la URL de una imagen satelital RGB para las coordenadas específicas.
    """
    ee.Authenticate()
    ee.Initialize(project='prueba-imagen-satelital')

    # Define una región de interés (ROI)
    roi = ee.Geometry.Rectangle([longitud - 0.015, latitud - 0.015, longitud + 0.015, latitud + 0.015])

    # Filtra la colección para obtener imágenes recientes del ROI
    imagenes = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED") \
        .filterBounds(roi) \
        .filterDate('2017-03-28', '2024-09-28') \
        .filterMetadata('CLOUDY_PIXEL_PERCENTAGE', 'less_than', 10)

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

    return url

def get_spectral_signature(longitud, latitud, fecha_inicio='2024-01-01', fecha_fin='2024-12-31'):
    """
    Calcula la firma espectral promedio de una región específica según las coordenadas.
    """
    # Definir la región de interés (ROI)
    roi = ee.Geometry.Rectangle([longitud - 0.015, latitud - 0.015, longitud + 0.015, latitud + 0.015])

    # Filtrar la colección de imágenes por ROI, fechas y porcentaje de nubes
    imagenes = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED") \
        .filterBounds(roi) \
        .filterDate(fecha_inicio, fecha_fin) \
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10)) \
        .median()  # Promedia las imágenes en el rango de fechas

    # Seleccionar bandas espectrales relevantes
    bandas = ['B2', 'B3', 'B4', 'B8', 'B11', 'B12']  # Azul, Verde, Rojo, NIR, SWIR1, SWIR2
    imagen = imagenes.select(bandas)

    # Reducir las bandas sobre la región de interés (media por banda)
    firma_espectral = imagen.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=roi,
        scale=10,
        bestEffort=True
    ).getInfo()

    if not firma_espectral:
        raise ValueError("No se pudo calcular la firma espectral. Verifica las coordenadas o el rango de fechas.")

    return firma_espectral

def calcular_porcentaje_vegetacion_y_url(longitud, latitud, fecha_inicio, fecha_fin):
    # Inicializar la API de Google Earth Engine
    ee.Initialize()

    # Definir la región de interés
    roi = ee.Geometry.Rectangle([longitud - 0.04, latitud - 0.04, longitud + 0.04, latitud + 0.04])
    
    # Cargar colección de imágenes Sentinel-2 y filtrar
    imagenes = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED") \
        .filterBounds(roi) \
        .filterDate(fecha_inicio, fecha_fin) \
        .filterMetadata('CLOUDY_PIXEL_PERCENTAGE', 'less_than', 10)
    
    # Crear una imagen compuesta usando la mediana
    imagen = imagenes.median()
    
    # Aplicar falso color compuesto para mejorar la identificación de la vegetación
    false_color = imagen.select(['B8', 'B11', 'B4'])

    # NDVI para el cálculo de cobertura vegetal utilizando la imagen en falso color
    ndvi = false_color.normalizedDifference(['B8', 'B4']).rename('NDVI')
    
    # Umbral para identificar vegetación densa
    vegetacion = ndvi.gt(0.3)

    # Calcular el área total de la ROI y el área de vegetación densa
    area_total = roi.area()
    area_vegetacion = vegetacion.multiply(ee.Image.pixelArea()).reduceRegion(
        reducer=ee.Reducer.sum(),
        geometry=roi,
        scale=10
    ).get('NDVI')
    
    # Porcentaje de área cubierta por vegetación
    porcentaje_vegetacion = ee.Number(area_vegetacion).divide(area_total).multiply(100).getInfo()
    
    # Parámetros para visualización en falso color (mejorada)
    false_color_params = {
        'bands': ['B8', 'B11', 'B4'],
        'min': 0,
        'max': 3000,
        'gamma': 1.4
    }

    # Generar URL de la imagen en falso color para mejor visualización
    url = false_color.visualize(**false_color_params).getThumbURL({
        'region': roi,
        'dimensions': 800,
        'format': 'jpg'
    })
    
    return porcentaje_vegetacion, url


def get_place_info_with_image_and_signature(query):
    """
    Obtiene información del lugar con su imagen satelital y firma espectral.
    """
    places_with_coordinates = suggestions.get_places_with_coordinates(query)
    place_info = []

    for place in places_with_coordinates:
        name = place['name']
        latitud, longitud = place['coordinates']
        image_url = get_image(longitud, latitud)
        spectral_signature = get_spectral_signature(longitud, latitud)
        place_info.append({
            'name': name,
            'coordinates': (latitud, longitud),
            'image_url': image_url,
            'spectral_signature': spectral_signature
        })

    return place_info