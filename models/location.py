class Location:
    def __init__(self, name, image, coordinates, state, description=None):
        self.name = name
        self.image = image
        self.coordinates = coordinates
        self.state = state
        self.description = description or "Descripción no disponible"
