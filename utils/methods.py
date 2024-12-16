import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gio, Gdk,GdkPixbuf, GLib
from modules import suggestions, earth_images
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

import threading
import requests
import tempfile
from gi.repository import Gtk, GdkPixbuf, GLib


def mostrar_imagen(image_box, ruta_imagen):
    """
    Carga una imagen desde una URL o archivo local de forma asincrónica y la muestra en image_box.
    """

    def load_image():
        """
        Carga la imagen en un hilo separado.
        """
        image_widget = None
        try:
            # Si la ruta es una URL, descargar la imagen
            if ruta_imagen.startswith("http"):
                response = requests.get(ruta_imagen)
                response.raise_for_status()  # Lanza un error si hay un problema en la descarga
                with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                    tmp_file.write(response.content)
                    tmp_file_path = tmp_file.name
                pixbuf = GdkPixbuf.Pixbuf.new_from_file(tmp_file_path)
            else:
                # Si es un archivo local, cargarlo directamente
                pixbuf = GdkPixbuf.Pixbuf.new_from_file(ruta_imagen)

            # Crear un Gtk.Image desde el Pixbuf cargado
            image_widget = Gtk.Image.new_from_pixbuf(pixbuf)
            image_widget.set_hexpand(True)
            image_widget.set_css_classes(["image-result"])

        except Exception as e:
            print(f"Error al cargar la imagen: {e}")

        # Usar GLib.idle_add para actualizar la interfaz desde el hilo principal
        if image_widget:
            GLib.idle_add(update_image_box, image_box, image_widget)

    # Lanzar la carga de la imagen en un hilo separado
    threading.Thread(target=load_image, daemon=True).start()


def update_image_box(image_box, image_widget):
    """
    Actualiza el contenedor image_box con el nuevo Gtk.Image.
    """
    # Eliminar cualquier widget existente en el image_box
    child = image_box.get_first_child()
    while child:
        image_box.remove(child)
        child = image_box.get_first_child()

    # Agregar el nuevo widget con la imagen
    image_box.append(image_widget)
    image_box.show_all()
