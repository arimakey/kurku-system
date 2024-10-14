from modules import earth_images, project, suggestions


if __name__ == "__main__":
    location = input("Ingresa un lugar a buscar: ")
    get_suggestions = suggestions.get_suggested_places(location)

    index = int(input("Selecciona uno: "))
    latitude, longitude = suggestions.select_suggested_places(get_suggestions, index)

    url_image = earth_images.get_image(longitude, latitude)

    print(url_image)