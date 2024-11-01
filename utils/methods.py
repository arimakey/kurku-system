import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gio, Gdk,GdkPixbuf
from modules import suggestions, earth_images
import requests
import tempfile

def apply_css():
        # Cargar el archivo CSS
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path("styles/styles.css")  # Cargar el archivo styles.css

        # Obtener el contexto de estilo para la aplicación y aplicar los estilos
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),  # Obtener el display por defecto
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_USER
        )

def on_button_clicked_satellite(self, button_selected, other_button, name_button):
        # Mostrar el botón seleccionado en la consola
        if name_button == "Satelite 1":
            print(name_button)
            button_selected.get_style_context().add_class("selected")
            other_button.get_style_context().remove_class("selected")

        elif name_button == "Satelite 2":
            print(name_button)
            button_selected.get_style_context().add_class("selected")
            other_button.get_style_context().remove_class("selected")

def on_button_clicked_model(self, button_selected, other_button1, other_button2, name_button):
        # Mostrar el botón seleccionado en la consola
        if name_button == "Modelo 1":
            print(name_button)
            button_selected.get_style_context().add_class("selected")
            other_button1.get_style_context().remove_class("selected")
            other_button2.get_style_context().remove_class("selected")

        elif name_button == "Modelo 2":
            print(name_button)
            button_selected.get_style_context().add_class("selected")
            other_button1.get_style_context().remove_class("selected")
            other_button2.get_style_context().remove_class("selected")

        elif name_button == "Modelo 3":
            print(name_button)
            button_selected.get_style_context().add_class("selected")
            other_button1.get_style_context().remove_class("selected")
            other_button2.get_style_context().remove_class("selected")


def on_image_button_clicked(image_box, selected, places):
    x, y = suggestions.select_suggested_places(places, selected)
    print(x, y)
    image_url = earth_images.get_image(x, y)
    mostrar_imagen(image_box, image_url)
    
def mostrar_imagen(image_box, ruta_imagen):
    """
    Muestra la imagen en el contenedor `image_box`, reemplazando cualquier imagen anterior.
    """
    # Eliminar cualquier imagen previa del image_box
    child = image_box.get_first_child()
    while child:
        image_box.remove(child)
        child = image_box.get_first_child()  # Actualizar al nuevo primer hijo después de la eliminación

    image_widget = None  # Inicializa `image_widget` por defecto

    # Cargar la imagen desde una URL remota o desde una ruta local
   
    if ruta_imagen.startswith("http"):
            # Descargar la imagen desde una URL remota
            response = requests.get(ruta_imagen)
            response.raise_for_status()  # Lanza un error si la descarga falla

            # Guardar la imagen en un archivo temporal
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                tmp_file.write(response.content)
                tmp_file_path = tmp_file.name

            # Cargar la imagen desde el archivo temporal
            pixbuf = GdkPixbuf.Pixbuf.new_from_file(tmp_file_path)
            image_widget = Gtk.Image.new_from_pixbuf(pixbuf)
            image_widget.set_hexpand(True)
            image_widget.set_css_classes(["imagen_resultado"])
    else:
            
            # Cargar la imagen desde una ruta local
            pixbuf = GdkPixbuf.Pixbuf.new_from_file(ruta_imagen)

        # Crear el widget de la imagen y configurar
            image_widget = Gtk.Image.new_from_pixbuf(pixbuf)
            image_widget.set_hexpand(True)
            image_widget.set_css_classes(["imagen_resultado"])

   

    # Agregar el widget de la imagen al `image_box`
    if image_widget:
        image_box.append(image_widget)
        image_box.show()

    return image_widget