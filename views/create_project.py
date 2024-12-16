import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gio
import os

def create_project(change_screen, locations, parent_window):
    main_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
    main_container.get_style_context().add_class("background-custom")

    # Crear header
    header_section = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
    header_section.set_halign(Gtk.Align.FILL)
    header_section.set_hexpand(True)

    # Crear FlowBox para las tarjetas
    projects = Gtk.FlowBox()
    projects.set_row_spacing(8)
    projects.set_column_spacing(8)
    projects.set_valign(Gtk.Align.START)
    projects.set_selection_mode(Gtk.SelectionMode.NONE)

    # ScrolledWindow para las tarjetas
    projects_section = Gtk.ScrolledWindow()
    projects_section.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
    projects_section.set_hexpand(True)
    projects_section.set_vexpand(True)
    projects_section.set_child(projects)

    main_container.append(header_section)
    main_container.append(projects_section)

    # Crear barra de búsqueda y botones
    search_bar = create_search_bar(projects, locations, change_screen, parent_window)
    add_button = create_add_button(change_screen)
    file_button = create_file_button()

    header_section.append(search_bar)
    header_section.append(add_button)
    header_section.append(file_button)

    # Cargar proyectos en las tarjetas
    load_projects(projects, locations, change_screen, parent_window)

    return main_container

def create_search_bar(projects, locations, change_screen, parent_window):
    """
    Crea una barra de búsqueda con un placeholder y un icono de lupa,
    y filtra las tarjetas en tiempo real.
    """
    search_bar = Gtk.Entry()
    search_bar.set_placeholder_text("Buscar...")
    search_bar.set_hexpand(True)
    search_bar.set_icon_from_icon_name(Gtk.EntryIconPosition.PRIMARY, "system-search-symbolic")
    search_bar.get_style_context().add_class("search-bar")

    # Conectar el evento "changed" para filtrar las tarjetas
    def on_search_changed(entry):
        search_text = entry.get_text().lower()
        filtered_locations = [
            loc for loc in locations if search_text in loc["name"].lower()  # Acceso a la clave 'name'
        ]
        load_projects(projects, filtered_locations, change_screen, parent_window)

    search_bar.connect("changed", on_search_changed)

    return search_bar

def load_projects(projects, locations, change_screen, parent_window):
    projects.remove_all()
    for location in locations:
        card = LocationCard(location, change_screen, parent_window)
        projects.append(card)

def create_add_button(change_screen):
    add_button = Gtk.Button()
    add_button.set_hexpand(False)
    add_button.connect("clicked", lambda x: change_screen("select_models"))

    # Agregar icono de añadir
    icon_image = Gtk.Image.new_from_icon_name("list-add-symbolic")  # Guardar la imagen
    add_button.set_child(icon_image)         # Añadir la imagen como hijo
    add_button.get_style_context().add_class("button-primary")
    return add_button

def create_file_button():
    file_button = Gtk.Button()
    file_button.set_hexpand(False)

    # Icono de carpeta
    icon_image = Gtk.Image.new_from_icon_name("folder-symbolic")
    file_button.set_child(icon_image)
    file_button.connect("clicked", on_file_button_clicked)
    file_button.get_style_context().add_class("button-primary")
    return file_button

def on_file_button_clicked(button):
    """
    Muestra un diálogo de selección de archivo.
    """
    dialog = Gtk.FileChooserNative(
        title="Select a File",
        action=Gtk.FileChooserAction.OPEN
    )

    dialog.set_modal(True)
    dialog.set_accept_label("Open")
    dialog.connect("response", on_file_dialog_response)
    dialog.show()

def on_file_dialog_response(dialog, response):
    if response == Gtk.ResponseType.ACCEPT:
        selected_file_path = dialog.get_file().get_path()
        print("Archivo seleccionado: ", selected_file_path)
    else:
        print("No se seleccionó ningún archivo")
    dialog.destroy()



class LocationCard(Gtk.Box):
    def __init__(self, location, change_screen, parent_window):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        self.location = location
        self.change_screen = change_screen
        self.get_style_context().add_class("active-card" if location["state"] else "inactive-card")

        # Configurar tamaño mínimo para la tarjeta
        self.set_size_request(100, 400)  # Ancho mínimo de 300px, altura mínima de 200px
        self.set_hexpand(True)  # Permite expansión cuando haya espacio adicional
        self.set_vexpand(False)  # Evita que la tarjeta se expanda verticalmente más de lo necesario

        # Contenedor principal para la tarjeta
        container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        container.get_style_context().add_class("project-container")
        container.set_hexpand(True)
        container.set_vexpand(True)  # Contenedor principal también respeta la altura mínima

        # Overlay para superponer círculo sobre imagen
        overlay = Gtk.Overlay()
        overlay.set_hexpand(True)
        overlay.set_vexpand(True)

        # Imagen principal
        image_file = Gio.File.new_for_path(location["image"])
        image = Gtk.Picture.new_for_file(image_file)
        
        # Establecer la imagen para que sea cuadrada y se adapte dinámicamente
        image.set_content_fit(Gtk.ContentFit.COVER)  # Mantener la imagen en proporción
        overlay.set_child(image)

        # Ajustar la imagen para que sea cuadrada, asegurando que se expanda adecuadamente
        image.set_hexpand(True)
        image.set_vexpand(True)
        
        # Esto garantiza que la imagen mantenga una forma cuadrada al expandirse.
        overlay.set_size_request(200, 200)  # Esto asegura que la imagen mantenga proporción cuadrada
        
        # Círculo de estado
        self.status_circle = Gtk.DrawingArea()
        self.status_circle.set_size_request(20, 20)
        self.status_circle.set_draw_func(self.on_draw_circle)
        overlay.add_overlay(self.status_circle)
        self.status_circle.set_halign(Gtk.Align.END)
        self.status_circle.set_valign(Gtk.Align.END)
        self.status_circle.set_margin_end(10)
        self.status_circle.set_margin_bottom(10)

        container.append(overlay)

        # Contenedor de datos (nombre y coordenadas)
        container_data = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        name_label = Gtk.Label(label=location["name"])
        name_label.get_style_context().add_class("name-label")
        name_label.set_halign(Gtk.Align.START)

        coordinates_label = Gtk.Label(label=location.get("coordinates", "No disponible"))
        coordinates_label.get_style_context().add_class("coordinate-label")
        coordinates_label.set_halign(Gtk.Align.END)
        coordinates_label.set_hexpand(True)

        container_data.append(name_label)
        container_data.append(coordinates_label)
        container.append(container_data)

        self.append(container)

        # Gesto para el clic
        click_gesture = Gtk.GestureClick()
        click_gesture.connect("released", self.on_card_clicked)
        self.add_controller(click_gesture)

    def on_draw_circle(self, widget, cr, width, height):
        # Color del círculo dependiendo del estado
        if self.location["state"]:
            cr.set_source_rgba(0, 1, 0, 1)  # Verde si está activo
        else:
            cr.set_source_rgba(1, 0, 0, 1)  # Rojo si no está activo

        # Dibujar círculo centrado
        cr.arc(width / 2, height / 2, 10, 0, 2 * 3.1416)  # Radio de 10
        cr.fill()

    def on_card_clicked(self, gesture, n_press, x, y):
        location_data = {
            "name": self.location["name"],
            "image": self.location["image"],
            "description": self.location.get("description", "No disponible"),
            "coordinates": self.location.get("coordinates", "No disponible"),
            "state": self.location["state"]
        }
        self.change_screen("show_location", location_data)