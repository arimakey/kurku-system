import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GdkPixbuf
from modules import earth_images, suggestions
from components.btn_direction import create_next_and_previous
from utils.methods import mostrar_imagen
import threading

def select_place(change_screen):
    # Crear un Box vertical PRINCIPAL
    main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

    # Crear un Box horizontal para el buscador
    search_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    search_box.set_margin_bottom(20)  # Margen inferior

    # Crear un Box horizontal para los resultados de la búsqueda
    result_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    result_box.set_hexpand(True)
    result_box.set_vexpand(True)
    
    # Crear un Box Horizontal para los botones
    button_box = create_next_and_previous(change_screen, "select_models", "select_models")

    # Agregar a main_box
    main_box.append(search_box)
    main_box.append(result_box)
    main_box.append(button_box)

    # BUSCADOR
    entry = Gtk.Entry()
    entry.set_placeholder_text("Nombre")  # Texto de sugerencia
    search_box.append(entry)
    entry.set_css_classes(["search-bar"])  # Clase CSS actualizada
    entry.set_hexpand(True)

    # Crear un BOTÓN DE BÚSQUEDA
    search_button = Gtk.Button()
    search_button.set_css_classes(["button-primary"])  # Clase CSS actualizada
    search_content = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
    search_content.set_margin_start(10)
    search_content.set_margin_end(10)
    icon_search = Gtk.Image.new_from_icon_name("folder-saved-search")
    label_search = Gtk.Label(label="Buscar")
    search_content.append(icon_search)
    search_content.append(label_search)
    search_button.set_child(search_content)
    search_box.append(search_button)

    # Clase para manejar imágenes
    class Imagen:
        def __init__(self, nombre, ruta):
            self.nombre = nombre
            self.ruta = ruta

    # Crear una lista de objetos Imagen
    places = []

    def mostrar_nombres():
        texto = entry.get_text()
        places = suggestions.get_suggested_places(texto)
        
        # Limpiar el área de resultados
        child = result_box.get_first_child()
        while child is not None:
            result_box.remove(child)
            child = result_box.get_first_child()
        
        # RESULTADOS
        result = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        result.set_css_classes(["result-box"])

        text_result = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        text_result.set_halign(Gtk.Align.CENTER)
        label_result = Gtk.Label(label="Resultados")
        label_result.set_margin_top(10)
        label_result.set_margin_bottom(0)
        label_result.set_css_classes(["result-label"])

        text_result.append(label_result)
        result.append(text_result)

        scrolled_result = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        
        scrolled_result.set_vexpand(True)

        # Barra de desplazamiento
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.set_min_content_height(320)
        scrolled_window.set_child(scrolled_result)

        result.append(scrolled_window)
        result_box.append(result)

        # Imagen de resultados
        image_box = Gtk.Box()
        image_box.set_css_classes(["image-result"])
        image_box.set_size_request(250, 250)
        image_box.set_hexpand(True)
        image_box.set_vexpand(True)
        result_box.append(image_box)

        for index, place in enumerate(places):
            button = Gtk.Button()
            button.set_margin_start(10)
            button.set_margin_end(10)
            button.set_css_classes(["search-result-item"])
            button.set_hexpand(True)
            button.connect("clicked", lambda btn, selected=index: on_image_button_clicked_async(image_box, selected, places))
            
            label = Gtk.Label(label=place)
            label.set_margin_top(6)
            label.set_margin_bottom(6)
            button.set_child(label)
            scrolled_result.append(button)

        # Imagen inicial con manejo de errores
        try:
            pixbuf = GdkPixbuf.Pixbuf.new_from_file("images/seleccione.jpg")
            image_widget = Gtk.Image.new_from_pixbuf(pixbuf)
            image_widget.set_css_classes(["image-result"])
            image_widget.set_hexpand(True)
            image_box.append(image_widget)
        except Exception as e:
            print(f"Error al cargar la imagen: {e}")
            error_label = Gtk.Label(label="Imagen no encontrada")
            image_box.append(error_label)

        # Mostrar el contenido
        result_box.show()

    # Conectar el botón de búsqueda
    search_button.connect("clicked", lambda x: mostrar_nombres())

    return main_box

def on_image_button_clicked_async(image_box, selected, places):
    """
    Ejecuta la carga de imágenes de forma asincrónica para evitar bloquear la interfaz.
    """
    def fetch_image():
        try:
            # Obtener coordenadas en un hilo separado
            x, y = suggestions.select_suggested_places(places, selected)
            image_url = earth_images.get_image(x, y)
            mostrar_imagen(image_box, image_url)  # Usar la función mostrar_imagen para cargar y mostrar
        except Exception as e:
            print(f"Error al obtener la imagen: {e}")

    # Crear un hilo para ejecutar la tarea de red
    threading.Thread(target=fetch_image, daemon=True).start()
