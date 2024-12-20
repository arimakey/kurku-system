import gi
gi.require_version("Gtk", "4.0")
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, GLib
from utils.xml_loader import load_projects_from_xml  # Cargar los proyectos
from views.create_project import create_project
from views.select_models import select_models
from views.select_place import select_place
from utils.methods import apply_css
from views.show_location import show_location  # Importar la vista para mostrar la ubicación
from views.select_name import create_add_location_view
import xml.etree.ElementTree as ET
import tempfile
import os
from views.loading_project import loading_project

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app)
        self.set_title("Kurku")
        self.set_default_size(800, 600)

        temp_dir = tempfile.mkdtemp()

        # Inicializar datos del proyecto
        self.project_data = {
            'name': '',
            'description': '',
            'location': '',
            'state': 'active',
            'model': '',
            'longitude': 0.0,
            'latitude': 0.0,
            'analysis_route': '',
            'height': 600,
            'width': 800
        }

        # Cargar los proyectos desde el archivo XML
        self.projects = load_projects_from_xml("projects.xml")

        # Crear una barra de herramientas (HeaderBar)
        header = Gtk.HeaderBar()
        header.set_title_widget(Gtk.Label(label="Kurku"))
        header.set_show_title_buttons(True)
        self.set_titlebar(header)

        # Aplicar CSS
        apply_css()

        # Crear una caja principal (Box)
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        main_box.set_margin_top(30)
        main_box.set_margin_bottom(30)
        main_box.set_margin_start(50)
        main_box.set_margin_end(50)
        self.set_child(main_box)

        # Crear un stack para las pantallas
        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.stack.set_transition_duration(250)
        main_box.append(self.stack)

        # Agregar las pantallas
        self.create_and_add_screens()

    def create_and_add_screens(self):
        # Crear las pantallas
        create_project_screen = create_project(self.change_screen, self.projects, self)
        select_models_screen = select_models(self.change_screen, self.save_project_data)
        select_place_screen = select_place(self.change_screen, self.save_project_data)
        add_location_screen = create_add_location_view(self.change_screen, self.save_project_data)

        # Añadir pantallas al stack
        self.stack.add_named(create_project_screen, "create_project")
        self.stack.add_named(select_models_screen, "select_models")
        self.stack.add_named(select_place_screen, "select_place")
        self.stack.add_named(add_location_screen, "add_location_screen")

    def change_screen(self, screen_name, location_data=None):
        if screen_name == "loading_project":
            loading_screen = loading_project(self.project_data, self.save_project_data, self.save_project_to_xml, self.change_screen)
            self.stack.add_named(loading_screen, "loading_project_screen")
            self.stack.set_visible_child_name("loading_project_screen")
        elif screen_name == "create_project":
            create_project_screen = create_project(self.change_screen, self.projects, self)
            self.stack.add_named(create_project_screen, "create_project_screen")
            self.stack.set_visible_child_name("create_project_screen")
        elif screen_name == "show_location" and location_data:
            show_location_screen = show_location(self.change_screen, location_data)
            self.stack.add_named(show_location_screen, "show_location_screen")
            self.stack.set_visible_child_name("show_location_screen")
        else:
            self.stack.set_visible_child_name(screen_name)

    def save_project_data(self, field, value):
        print(field, value)
        # Guardar los datos del proyecto
        if field in self.project_data:
            self.project_data[field] = value


    def save_project_to_xml(self):
        # Verificar si el archivo XML ya existe
        if os.path.exists("projects.xml"):
            # Cargar el archivo XML existente
            tree = ET.parse("projects.xml")
            root = tree.getroot()
        else:
            # Crear el elemento raíz si no existe el archivo
            root = ET.Element("projects")
            tree = ET.ElementTree(root)

        # Crear un nuevo elemento de proyecto
        project_element = ET.Element("project")

        for key, value in self.project_data.items():
            child = ET.SubElement(project_element, key)
            child.text = str(value)

        # Agregar el nuevo proyecto al árbol existente
        root.append(project_element)

        # Guardar el archivo XML actualizado
        tree.write("projects.xml", encoding="utf-8", xml_declaration=True)


class MainApp(Adw.Application):
    def __init__(self):
        super().__init__(application_id="com.kurku")

    def do_activate(self):
        # Inicializar la ventana principal
        win = MainWindow(self)
        win.present()

# Crear y ejecutar la aplicación
app = MainApp()
app.run(None)
