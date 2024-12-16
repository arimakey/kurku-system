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
        image = project_elem.find("image").text
        model = project_elem.find("model").text
        longitude = project_elem.find("longitude").text
        latitude = project_elem.find("latitude").text
        analysis_route = project_elem.find("analysis_route").text

        # Crear un diccionario con los datos del proyecto
        project = {
            "name": name,
            "description": description,
            "location": location,
            "state": state,
            "image": image,
            "model": model,
            "longitude": longitude,
            "latitude": latitude,
            "analysis_route": analysis_route
        }
        projects.append(project)

    return projects
