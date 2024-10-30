import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gdk, Pango

selected_file_path = None

def create_project(change_screen):
    #Creacion de containers
    container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    container_1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
    container_2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

    #Añadir clases a container
    container.get_style_context().add_class("container")
    container_2.get_style_context().add_class("container2")

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
    container_wrapper = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    container_wrapper.set_vexpand(True)

    #Bucle para colocar los cards
    container_card = None 
    for i,location in enumerate(locations):
        if i % 3 == 0: 
            container_card = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
            container_card.set_margin_start(10)
            container_card.set_margin_end(10)
            container_card.set_margin_bottom(10)
            container_card.set_margin_top(10)
            container_wrapper.append(container_card)
        card = LocationCard(location)
        container_card.append(card)

    #Agregar scrollbar al contenedor wrapper
    scrolled_window = Gtk.ScrolledWindow()
    scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC) 
    scrolled_window.set_child(container_wrapper)
    
    #Configuracion de containers
    container_2.set_hexpand(True)
    container_2.set_vexpand(True)
    container_2.set_margin_start(10)
    container_2.set_margin_end(10)
    container_2.set_margin_bottom(30)
    container_1.set_halign(Gtk.Align.FILL)
    container_1.set_hexpand(True)
    
    #Agregar containers
    container.append(container_1)
    container_2.append(scrolled_window)
    container.append(container_2)
    container_1.append(create_search_bar())
    container_1.append(create_add_button(change_screen))
    container_1.append(create_file_button())

    return container

def create_file_button():
    file_button=Gtk.Button()
    file_button.set_margin_top(30)
    file_button.set_margin_start(10)
    file_button.set_margin_end(80)
    file_button.set_margin_bottom(30)
    file_button.set_hexpand(False)

    icon_image = Gtk.Image.new_from_icon_name("folder-symbolic")  #guardar la imagen
    file_button.set_child(icon_image)         #añadir la imagen como hijo
    file_button.connect("clicked", on_file_button_clicked)
    file_button.get_style_context().add_class("custom-btn")
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
    add_button.set_margin_top(30)
    add_button.set_margin_start(10)
    add_button.set_margin_bottom(30)
    add_button.set_hexpand(False)
    add_button.connect("clicked", lambda x: change_screen("project_options"))

    # Agregar icono de añadir
    icon_image = Gtk.Image.new_from_icon_name("list-add-symbolic")  #guardar la imagen
    add_button.set_child(icon_image)         #añadir la imagen como hijo
    add_button.get_style_context().add_class("custom-btn")
    return add_button
   
def create_toolbar():
    toolbar = Gtk.HeaderBar()
    toolbar.set_show_title_buttons(True)
    return toolbar

def apply_css():
    css_provider = Gtk.CssProvider()
    css_provider.load_from_path("styles.css")

    Gtk.StyleContext.add_provider_for_display(
        Gdk.Display.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )

def create_search_bar():
    search_bar = Gtk.Entry() #Crea la entrada
    search_bar.set_placeholder_text("Search...")
    search_bar.set_margin_top(30)
    search_bar.set_margin_start(80)
    search_bar.set_margin_bottom(30)
    search_bar.set_hexpand(True)
    # Agregar icono de lupa
    search_bar.set_icon_from_icon_name(Gtk.EntryIconPosition.PRIMARY, "system-search-symbolic")
    search_bar.get_style_context().add_class("custom-search-bar")
    return search_bar

class NewProjectWindow(Gtk.Window):

    def __init__(self):
        super().__init__(title = "Proyecto")
        self.set_default_size(350,120)

        self.connect("realize", self.center_window)

        self.create_name_bar = self.create_name_bar()
        container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        container_1 = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)

        container_1.append(self.create_name_bar)
        container_1.append(self.create_button())
        container_1.get_style_context().add_class("bg-custom")
        container.append(container_1)
        self.apply_css()

        self.set_child(container)

    def center_window(self, *args):
        self.maximize()
        self.unmaximize()

    def create_name_bar(self):
        name_bar = Gtk.Entry() #Crea la entrada
        name_bar.set_placeholder_text("Nombre...")
        name_bar.set_margin_top(30)
        name_bar.set_margin_start(20)
        name_bar.set_margin_bottom(50)
        name_bar.set_hexpand(True)
        name_bar.set_size_request(230,40)
        return name_bar

    def create_button(self):
        create_button=Gtk.Button(label = "Crear")
        create_button.set_margin_top(30)
        create_button.set_margin_start(10)
        create_button.set_margin_end(20)
        create_button.set_margin_bottom(50)
        create_button.set_hexpand(False)

        create_button.connect("clicked", self.open_save_dialog)
        create_button.get_style_context().add_class("custom-btn2")
        return create_button

    def open_save_dialog(self, button):
        file_name = self.create_name_bar.get_text().strip()  #Obtener texto ingresado

        if not file_name:
            print("Ingrese un nombre para el archivo.")
            return

        if not file_name.endswith(".xml"):  #Agregar extension si no está presente
            file_name += ".xml"

        dialog = Gtk.FileChooserNative(     #Abrir el apartado para guardar
            title = "Guardar como",
            action = Gtk.FileChooserAction.SAVE
        )
        dialog.set_modal(True)
        dialog.set_current_name(file_name)      #Mostrar nombre sugerido para el archivo

        dialog.connect("response", self.on_save_dialog_response)
        dialog.show()

    def on_save_dialog_response(self, dialog, response):
        if response == Gtk.ResponseType.ACCEPT:
            file_path = dialog.get_file().get_path()
            try:
                with open(file_path, "w") as file:
                    file.write("Este es un archivo de texto creado desde la aplicación.")
                print(f"Archivo guardado en: {file_path}")
            except Exception as e:
                print(f"Error al guardar el archivo: {e}")
        else:
            print("Guardado cancelado por el usuario.")
        # Cerrar el diálogo
        dialog.destroy()

    def apply_css(self):
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path("styles.css")
        # Aplicar el CSS solo al contenedor especificado
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )

class Location:
    def __init__ (self, name, state, coordinates, image):
        self.name = name
        self.state = state
        self.coordinates = coordinates
        self.image = image

class LocationCard(Gtk.Box):
    def __init__(self, location):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        self.apply_css()
        self.set_vexpand(False)
        self.set_hexpand(False)
        self.set_margin_start(20)

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

    def apply_css(self):
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path("styles.css")

        # Aplicar el CSS solo al contenedor especificado
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )