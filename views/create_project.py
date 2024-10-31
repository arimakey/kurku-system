import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gdk, Pango

selected_file_path = None

def create_project(change_screen):
    #Creacion de containers
    
    main_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
    header_section = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
    projects_section = Gtk.ScrolledWindow()

    #Añadir clases a container
    
    #Variables
    locations = [
        Location("Trujillo", True, "35° 41' 22'' N ", r".\images\prueba.png"),
        Location("Amazonas", True, "36° 41' 22'' N", r".\images\prueba.png"),
        Location("Ucayali", False, "37° 41' 22'' N", r".\images\prueba.png"),
        Location("Trujillo", True, "35° 41' 22'' N ", r".\images\prueba.png"),
        Location("Amazonas", False, "36° 41' 22'' N", r".\images\prueba.png"),
        Location("Amazonas", True, "36° 41' 22'' N", r".\images\prueba.png"),
        Location("Ucayali", False, "37° 41' 22'' N", r".\images\prueba.png"),
        Location("Trujillo", True, "35° 41' 22'' N ", r".\images\prueba.png"),
    ]
    
    #Crear contenedor adicional
    container_wrapper = Gtk.FlowBox()
    container_wrapper.set_row_spacing(8)
    container_wrapper.set_column_spacing(8)
    container_wrapper.set_valign(Gtk.Align.START)
    container_wrapper.set_max_children_per_line(0)
    container_wrapper.set_selection_mode(Gtk.SelectionMode.NONE)

    container_wrapper.get_style_context().add_class("projects_container")

    #Bucle para colocar los cards
    for i,location in enumerate(locations):
        card = LocationCard(location)
        container_wrapper.append(card)

    #Agregar scrollbar al contenedor wrapper
    projects_section.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC) 
    projects_section.set_child(container_wrapper)
    
    #Configuracion de containers
    projects_section.set_hexpand(True)
    projects_section.set_vexpand(True)
    header_section.set_halign(Gtk.Align.FILL)
    header_section.set_hexpand(True)
        
    #Agregar containers
    main_container.append(header_section)
    main_container.append(projects_section)
    
    header_section.append(create_search_bar())
    header_section.append(create_add_button(change_screen))
    header_section.append(create_file_button())

    return main_container

def load_projects():
    return

def create_file_button():
    file_button=Gtk.Button()
    file_button.set_hexpand(False)

    icon_image = Gtk.Image.new_from_icon_name("folder-symbolic")
    file_button.set_child(icon_image)
    file_button.connect("clicked", on_file_button_clicked)
    file_button.get_style_context().add_class("btn_primary")
    return file_button

def on_file_button_clicked(button):
    dialog = Gtk.FileChooserNative(
        title="Select a File",
        action = Gtk.FileChooserAction.OPEN
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
        print("No se selecciono ningun archivo")
    dialog.destroy()
    
def create_add_button(change_screen):
    add_button=Gtk.Button()
    add_button.set_hexpand(False)
    add_button.connect("clicked", lambda x: change_screen("project_options"))

    # Agregar icono de añadir
    icon_image = Gtk.Image.new_from_icon_name("list-add-symbolic")  #guardar la imagen
    add_button.set_child(icon_image)         #añadir la imagen como hijo
    add_button.get_style_context().add_class("btn_primary")
    return add_button

def create_search_bar():
    search_bar = Gtk.Entry() #Crea la entrada
    search_bar.set_placeholder_text("Search...")
    search_bar.set_hexpand(True)
    # Agregar icono de lupa
    search_bar.set_icon_from_icon_name(Gtk.EntryIconPosition.PRIMARY, "system-search-symbolic")
    search_bar.get_style_context().add_class("search-bar")
    return search_bar

class Location:
    def __init__ (self, name, state, coordinates, image):
        self.name = name
        self.state = state
        self.coordinates = coordinates
        self.image = image

class LocationCard(Gtk.Box):
    def __init__(self, location):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        self.set_vexpand(False)
        self.set_hexpand(False)

        container = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing= 20)
        container_img = Gtk.Fixed()
        container_data= Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)

        image = Gtk.Image.new_from_file(location.image)
        image.set_size_request(200,200)
        container_img.set_size_request (200,200)
        container_img.put(image, 3, 3)

        self.status_icon = Gtk.Image()
        if location.state:
            self.get_style_context().add_class("active-card")
            self.status_icon.set_from_file("./images/btn_verde.png")
        else:
            self.get_style_context().add_class("inactive-card")
            self.status_icon.set_from_file("./images/btn_rojo.png")

        self.status_icon.set_size_request(20,20)
        container_img.put(self.status_icon,180,180)

        container.append(container_img)

        name_label = Gtk.Label(label = location.name)
        name_label.get_style_context().add_class("custom-name-lb")
        container_data.append(name_label)

        coordinates_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        coordinates_label = Gtk.Label(label=location.coordinates)
        coordinates_label.get_style_context().add_class("custom-coor-lb")
        coordinates_box.append(coordinates_label)
        coordinates_box.set_halign(Gtk.Align.END)  # Alinear a la derecha
        coordinates_box.set_hexpand(True)
        container_data.append(coordinates_box)
        container_data.get_style_context().add_class("container_data")

        container.append (container_data)

        self.append(container)