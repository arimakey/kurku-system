from modules.earth_images import descargar_imagenes

def test_descargar_imagenes():
    # Establecer coordenadas, fechas y, opcionalmente, un directorio
    longitud = -70.0421171
    latitud = -12.6028533
    fecha_inicio = '2010-01-01'
    fecha_fin = '2024-12-31'
    directorio = 'data/images'  # Este es el directorio por defecto, se puede omitir

    # Llamar a la función
    descargar_imagenes(longitud, latitud, fecha_inicio, fecha_fin, directorio)

if __name__ == "__main__":
    test_descargar_imagenes()