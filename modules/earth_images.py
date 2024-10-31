import ee
from modules import suggestions

ee.Authenticate()
ee.Initialize(project='prueba-imagen-satelital')

def obtener_urls_imagenes(longitud=-70.4967607, latitud=-12.0545491, fecha_inicio='2024-01-01', fecha_fin='2024-10-23'):
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
    ee.Authenticate()
    ee.Initialize(project='prueba-imagen-satelital')

    # Crea un punto de interés (POI)
    poi = ee.Geometry.Point([longitud, latitud])

    # Define una región de interés (ROI)
    roi = ee.Geometry.Rectangle([longitud - 0.015, latitud - 0.015, longitud + 0.015, latitud + 0.015])

    # Filtra la colección para obtener imágenes recientes del ROI
    imagenes = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED") \
        .filterBounds(roi) \
        .filterDate('2017-03-28', '2024-09-28') \
        .filterMetadata('CLOUDY_PIXEL_PERCENTAGE','less_than', 10)

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


def get_place_info_with_image(query):
    places_with_coordinates = suggestions.get_places_with_coordinates(query)
    place_info = []

    for place in places_with_coordinates:
        name = place['name']
        latitud, longitud = place['coordinates']
        image_url = get_image(longitud, latitud)
        place_info.append({
            'name': name,
            'coordinates': (latitud, longitud),
            'image_url': image_url
        })

    return place_info