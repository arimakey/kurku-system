import requests
import geopy
from geopy.geocoders import Nominatim

# LocationIQ API key
API_KEY = 'pk.ce50a5663503058cf13001062b0db6a7'

def get_suggested_places(query):
    # Endpoint
    url = f'https://us1.locationiq.com/v1/autocomplete.php'

    # Request parameters
    params = {
        'key': API_KEY,
        'q': query,
        'format': 'json',
        'limit': 20
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Check for HTTP errors
        places = response.json()

        # Lista de sugerencias
        suggestions = [place['display_name'] for place in places]

        print(f"Suggestions for '{query}':")
        for idx, place in enumerate(suggestions):
            print(f"{idx}. {place}")

        return suggestions

    except requests.exceptions.HTTPError as err:
        print(f"HTTP request error: {err}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Selecciona lugar
    input_query = input("Ingrese un lugar: ")
    
    suggestions = get_suggested_places(input_query)
    # Crear una instancia del geolocalizador con un user_agent personalizado
    geolocator = Nominatim(user_agent="pachamama_project")

    if suggestions:
        try:
            index = int(input(f"Selecciona un lugar (0-{len(suggestions) - 1}): "))
            if 0 <= index < len(suggestions):
                location = geolocator.geocode(suggestions[index])
                if location:
                    print(f"Coordenadas de {suggestions[index]}:")
                    print(f"{location.latitude},{location.longitude}")
                else:
                    print("No se encontraron coordenadas para el lugar ingresado.")
            else:
                print("Fuera de rango")
        except ValueError:
            print("Ingresa un número válido")
