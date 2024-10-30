import requests
import geopy
from geopy.geocoders import Nominatim

# LocationIQ API keyS
API_KEY = 'pk.ce50a5663503058cf13001062b0db6a7'

def get_suggested_places(query):
    # Endpoint
    url = f'https://us1.locationiq.com/v1/autocomplete.php'

    # Request parameters
    params = {
        'key': API_KEY,
        'q': query,
        'format': 'json',
        'limit': 10
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status() 
        places = response.json()

        suggestions = [place['display_name'] for place in places]

        print(f"Suggestions for '{query}':")
        for idx, place in enumerate(suggestions):
            print(f"{idx}. {place}")

        return suggestions

    except requests.exceptions.HTTPError as err:
        print(f"HTTP request error: {err}")
    except Exception as e:
        print(f"An error occurred: {e}")

def select_suggested_places(suggestions, index):
    geolocator = Nominatim(user_agent="pachamama_project")
    if suggestions:
        try:
            if 0 <= index < len(suggestions):
                location = geolocator.geocode(suggestions[index])
                if location:
                    print(f"Coordenadas de {suggestions[index]}:")
                    return location.latitude, location.longitude
                else:
                    print("No se encontraron coordenadas para el lugar ingresado.")
            else:
                print("Fuera de rango")
        except ValueError:
            print("Ingresa un número válido")


def get_places_with_coordinates(query):
    suggestions = get_suggested_places(query)
    geolocator = Nominatim(user_agent="pachamama_project")
    
    places_with_coordinates = []

    if suggestions:
        for place in suggestions:
            location = geolocator.geocode(place)
            if location:
                places_with_coordinates.append({
                    'name': place,
                    'coordinates': (location.latitude, location.longitude)
                })
            else:
                print(f"No se encontraron coordenadas para {place}.")

    return places_with_coordinates