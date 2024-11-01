import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GdkPixbuf
from utils.methods import on_image_button_clicked
from modules import earth_images, suggestions
from components.btn_direction import create_next_and_previous

def select_place(change_screen):
    # Crear un Box vertical PRINCIPAL
    main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

    # Crear un Box horizontal para el buscador
    search_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    search_box.set_margin_bottom(20)  # Margen inferior
    #search_box.set_valign(Gtk.Align.FILL)  # Alinear verticalmente para llenar

    # Crear un Box horizontal para el LOS RESULTADOS DE LA BUSQUEDA
    result_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    result_box.set_hexpand(True)
    result_box.set_vexpand(True)
    
    # Crear un Box Horizontal para los botones
    button_box = create_next_and_previous(change_screen, "project_options", "project_options")

    # Agregar a main_box
    main_box.append(search_box)
    main_box.append(result_box)
    main_box.append(button_box)

# BUSCADOR

        # Crear una CAJA DE ENTRADA DE TEXTO
    entry = Gtk.Entry()
    entry.set_placeholder_text("Nombre")  # Texto de sugerencia
    search_box.append(entry)
    entry.set_css_classes(["search-bar"])  # Agregar una clase CSS
    entry.set_hexpand(True)

    # Crear un BOTON DE BUSQUEDA
    search_button=  Gtk.Button()
    search_button.set_css_classes(["btn_primary"])  # Agregar una clase CSS 
    # Crear un contenedor horizontal para el ícono y el texto
    search_content= Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
    search_content.set_margin_start(10)     # Margen derecho
    search_content.set_margin_end(10)     # Margen derecho
    # Crear el ícono
    icon_search = Gtk.Image.new_from_icon_name("folder-saved-search")
    # Crear una etiqueta con el texto
    label_search= Gtk.Label(label="Buscar")
    # Agregar el ícono y la etiqueta al contenedor
    search_content.append(icon_search)
    search_content.append(label_search)
    # Agregar el contenedor al botón
    search_button.set_child(search_content)
    search_box.append(search_button)
        
    class Imagen:
        def __init__(self, nombre, ruta):
            self.nombre = nombre
            self.ruta = ruta
    # Crear una lista de objetos Imagen
    places = []
    
    def mostrar_nombres():
        texto = entry.get_text()
        places = suggestions.get_suggested_places(texto)
        
        # Inicializar child al primer hijo de result
        child = result_box.get_first_child()
        
        # Limpiar el área de resultados
        child = result_box.get_first_child()
        while child is not None:
            result_box.remove(child)
            child = result_box.get_first_child()
        
        # RESULTADOS
        #Crear un contenedor de resultados
        result = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        # result.set_size_request(300, -1)
        result.set_css_classes(["box_result"])  # Agregar una clase CSS

            # Titulo
        text_result= Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        text_result.set_halign(Gtk.Align.CENTER)  # Alinear el contenido al centro

        label_result = Gtk.Label(label="Resultados")
        label_result.set_margin_top(10)  # Margen superior
        label_result.set_margin_bottom(0)  # Margen inferior
        label_result.set_css_classes(["label_result"])

        text_result.append(label_result)
        result.append(text_result)

        scrolled_result = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)

        # Crear un contenedor con barra de desplazamiento
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)  # Desplazamiento solo vertical
        scrolled_window.set_min_content_height(320)  # Altura mínima visible
        # scrolled_window.set_hexpand(True)
        # scrolled_window.set_vexpand(False)
        
        scrolled_window.set_child(scrolled_result)
        # Agregar el contenedor de resultados al scrolled_window
        result.append(scrolled_window)

        result_box.append(result)

        # IMAGEN
        # Crear un contenedor para la imagen con tamaño fijo
        image_box = Gtk.Box()
        image_box.set_css_classes(["imagen_resultado"])  # Agregar una clase CSS
        image_box.set_size_request(250, 250)
        image_box.set_hexpand(True)
        image_box.set_vexpand(True)
        result_box.append(image_box)

        for index, place in enumerate(places):
            # Crear un botón para cada imagen
            button = Gtk.Button()
            button.set_margin_start(10)
            button.set_margin_end(10)
            button.set_css_classes(["lista_resultados"])  # Agregar una clase CSS
            button.set_hexpand(True)
            
            button.connect("clicked", lambda btn, selected=index: on_image_button_clicked(image_box, selected, places))  # Pasar el contenedor de imagen y la imagen actual
            
            label = Gtk.Label(label=place)
            label.set_margin_top(6)
            label.set_margin_bottom(6)
            button.set_child(label)
            scrolled_result.append(button)
            
        # Cargar la nueva imagen correspondiente
        pixbuf = GdkPixbuf.Pixbuf.new_from_file("images/seleccione.jpg")
        image_widget = Gtk.Image.new_from_pixbuf(pixbuf)
        image_widget.set_css_classes(["imagen_resultado"])

        image_widget.set_hexpand(True)

        # Agregar la nueva imagen al image_box
        image_box.append(image_widget)
        image_box.show()

    search_button.connect("clicked", lambda x: mostrar_nombres())

    return main_box


