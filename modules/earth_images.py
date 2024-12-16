import ee
import os
import requests
from modules import suggestions

ee.Authenticate()
ee.Initialize(project='prueba-imagen-satelital')

def descargar_imagenes(longitud, latitud, fecha_inicio, fecha_fin, directorio='data/proyecto_trujillo'):
    try:
        # Inicializar la API de Earth Engine
        ee.Initialize()
        
        # Definir el área de interés (ROI)
        roi = ee.Geometry.Rectangle([longitud-0.03, latitud-0.03, longitud+0.03, latitud+0.03])

        # Obtener la colección de imágenes
        imagenes = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED") \
                    .filterBounds(roi) \
                    .filterDate(fecha_inicio, fecha_fin) \
                    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 1))

        # Convertir la lista de imágenes en una lista de Python
        lista_imagenes = imagenes.toList(imagenes.size()).getInfo()

        # Verificar y crear el directorio principal si no existe
        if not os.path.exists(directorio):
            os.makedirs(directorio)

        # Crear la subcarpeta 'images' para almacenar las imágenes NDVI
        images_directory = os.path.join(directorio, 'images')
        if not os.path.exists(images_directory):
            os.makedirs(images_directory)

        # Crear el archivo CSV fuera de la carpeta 'images'
        csv_path = os.path.join(directorio, 'vegetation_data.csv')
        with open(csv_path, 'w') as file:
            file.write('fecha,vegetation_percentage\n')  # Escribir encabezados

        # Procesar cada imagen y guardarla
        for imagen_info in lista_imagenes:
            id_imagen = imagen_info['id']
            imagen = ee.Image(id_imagen)

            # Calcular el NDVI
            ndvi = imagen.normalizedDifference(['B8', 'B4']).rename('NDVI')
            ndvi_image = ndvi.visualize(min=0, max=1, palette=['white', 'green'])
            ndvi_url = ndvi_image.getDownloadURL({
                'region': roi,
                'scale': 10,
                'format': 'jpg'
            })

            # Calcular el porcentaje de vegetación
            vegetacion_mask = ndvi.gt(0.4)
            porcentaje_vegetacion = vegetacion_mask.reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=roi,
                scale=10
            ).get('NDVI').getInfo() * 100  # Convertir a porcentaje

            # Descargar la imagen NDVI
            ndvi_response = requests.get(ndvi_url)
            fecha = id_imagen.split('/')[-1]  # Extraer la fecha del ID
            ndvi_filename = os.path.join(images_directory, f'{fecha}_NDVI.jpg')

            with open(ndvi_filename, 'wb') as f:
                f.write(ndvi_response.content)

            # Guardar la información de vegetación en el archivo CSV
            with open(csv_path, 'a') as file:
                file.write(f"{fecha},{porcentaje_vegetacion}\n")

        print("Descarga y procesamiento completado.")

    except ee.EEException as e:
        print("Error al interactuar con Google Earth Engine:", e)
    except requests.exceptions.RequestException as e:
        print("Error al descargar la imagen:", e)
    except Exception as e:
        print("Ocurrió un error inesperado:", e)

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

def url_imagen_vegetacion_coloreada(longitud, latitud, fecha_inicio='2024-01-01', fecha_fin='2024-12-31'):

    # Define la región de interés (ROI) como un rectángulo alrededor de las coordenadas dadas
    roi = ee.Geometry.Rectangle([longitud - 0.03, latitud - 0.03, longitud + 0.03, latitud + 0.03])

    # Filtra la colección de imágenes Sentinel-2 por la ROI, fechas y porcentaje de nubes
    imagenes = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED") \
        .filterBounds(roi) \
        .filterDate(fecha_inicio, fecha_fin) \
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10))

    # Utiliza la mediana de las imágenes para reducir el ruido y los efectos de las nubes
    imagen = imagenes.median()

    # Calcula el NDVI usando las bandas del infrarrojo cercano (NIR) y rojo (Red)
    ndvi = imagen.normalizedDifference(['B8', 'B4']).rename('NDVI')

    # Crear una máscara de vegetación donde el NDVI sea mayor que un umbral
    vegetacion_mask = ndvi.gt(0.4)

    # Aplicar la máscara de vegetación con color verde
    imagen_coloreada = imagen.visualize(min=0, max=3000, bands=['B4', 'B3', 'B2']).blend(
        ee.Image(1).visualize(palette=['green']).mask(vegetacion_mask)
    )

    # Genera y devuelve la URL de la imagen visualizada
    url = imagen_coloreada.getThumbURL({
        'region': roi,
        'dimensions': 800,
        'format': 'jpg'
    })

    return url

def calcular_porcentaje_vegetacion_y_url(longitud, latitud, fecha_inicio, fecha_fin):
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