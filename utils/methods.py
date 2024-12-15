import gi

from test import earth_images
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gio, Gdk,GdkPixbuf, GLib
from modules import suggestions
import requests
import tempfile
import threading

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


#Modificaciones de la funcion para hacerla en un hilo separado
    
def mostrar_imagen(image_box, ruta_imagen):

    def load_image(): 
        image_widget = None
        try: 
            if ruta_imagen.startswith("http"):
                response = requests.get(ruta_imagen)
                response.raise_for_status()  # Lanza un error si la descarga falla
                with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                    tmp_file.write(response.content)
                    tmp_file_path = tmp_file.name
                pixbuf = GdkPixbuf.Pixbuf.new_from_file(tmp_file_path)
            else: 
                pixbuf = GdkPixbuf.Pixbuf.new_from_file(ruta_imagen)

            image_widget = Gtk.Image.new_from_pixbuf(pixbuf)
            image_widget.set_hexpand(True)
            image_widget.set_css_classes(["imagen_resultado"])

        except Exception as e: 
             print(f"Error al cargar la imagen:", e)

        # Usar GLib.idle_add para actualizar la interfaz en el hilo principal
        if image_widget:
            GLib.idle_add(update_image_box, image_box, image_widget)
    
    # Lanzar el hilo
    threading.Thread(target=load_image, daemon=True).start()

def update_image_box(image_box, image_widget):
    child = image_box.get_first_child()
    while child:
        image_box.remove(child)
        child = image_box.get_first_child()

    # Añadir la nueva imagen y mostrarla
    image_box.append(image_widget)
    image_box.show()

