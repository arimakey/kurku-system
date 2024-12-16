import xml.etree.ElementTree as ET
from models.location import Location

def load_projects_from_xml(file_path):
    """
    Carga los proyectos desde un archivo XML y retorna una lista de diccionarios.
    """
    tree = ET.parse(file_path)
    root = tree.getroot()

    projects = []

    # Iterar sobre los elementos <project> en el XML
    for project_elem in root.findall("project"):
        name = project_elem.find("name").text
        description = project_elem.find("description").text
        location = project_elem.find("location").text
        state = project_elem.find("state").text.lower() == "active"  # Convertir 'active' a booleano
        
        # No es necesario buscar la etiqueta <image> en el XML
        # Ruta fija de la imagen de vista previa
        image = "/data/{}/preview.jpg".format(name.replace(" ", "_").lower())  # Ruta fija con el nombre del proyecto

        height = project_elem.find("height").text if project_elem.find("height") is not None else None
        width = project_elem.find("width").text if project_elem.find("width") is not None else None

        model = project_elem.find("model").text
        longitude = float(project_elem.find("longitude").text) if project_elem.find("longitude") is not None else None
        latitude = float(project_elem.find("latitude").text) if project_elem.find("latitude") is not None else None
        analysis_route = project_elem.find("analysis_route").text

        # Crear un diccionario con los datos del proyecto
        project = {
            "name": name,
            "description": description,
            "location": location,
            "state": state,
            "image": image,  # Ruta de la imagen de vista previa
            "height": height,
            "width": width,
            "model": model,
            "longitude": longitude,
            "latitude": latitude,
            "analysis_route": analysis_route
        }
        projects.append(project)

    return projects
