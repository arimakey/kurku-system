import ee

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

urls = obtener_urls_imagenes()

for url in urls:
    print(url)
