import requests

def get_image(url, route):
    response = requests.get(url)
    if response.status_code == 200:
        with open(route, "wb") as file:
            file.write(response.content)
        print("Imagen descargada con éxito.")
    else:
        print(f"Error al descargar la imagen. Código de estado: {response.status_code}")