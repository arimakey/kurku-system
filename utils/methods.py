import os
import threading
import requests
import tempfile
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GLib, Gdk, GdkPixbuf

# Crear la carpeta 'temp' si no existe
temp_dir = "temp"
os.makedirs(temp_dir, exist_ok=True)
def mostrar_imagen(image_box, ruta_imagen):
    """
    Carga una imagen desde una URL o archivo local de forma asincrónica y la muestra en image_box.
    Muestra un mensaje de "Cargando..." con un spinner mientras la imagen se carga.
    """

    def load_image():
        image_widget = None

        if ruta_imagen == "loading":
            # Crear spinner y texto de carga visibles
            spinner = Gtk.Spinner()
            spinner.set_name("custom-spinner")  # Nombre CSS personalizado
            spinner.start()

            loading_label = Gtk.Label(label="Cargando...")
            loading_label.set_name("loading-text")
            loading_label.set_halign(Gtk.Align.CENTER)
            loading_label.set_valign(Gtk.Align.CENTER)

            # Caja central para el spinner y el texto
            loading_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
            loading_box.set_halign(Gtk.Align.CENTER)
            loading_box.set_valign(Gtk.Align.CENTER)
            loading_box.append(spinner)
            loading_box.append(loading_label)

            # Caja de fondo para centrar el contenido
            background_box = Gtk.Box()
            background_box.set_name("loading-background")
            background_box.set_hexpand(True)
            background_box.set_vexpand(True)
            background_box.set_halign(Gtk.Align.CENTER)
            background_box.set_valign(Gtk.Align.CENTER)
            background_box.append(loading_box)

            # Actualizar la caja de la interfaz para mostrar el contenido de carga centrado
            GLib.idle_add(update_image_box, image_box, background_box)
            return

        try:
            # Ruta del archivo temporal para la imagen
            temp_image_path = os.path.join(temp_dir, "imagen_temporal.jpg")

            # Si ya existe una imagen temporal, eliminarla
            if os.path.exists(temp_image_path):
                os.remove(temp_image_path)

            # Si la ruta es una URL, descargar la imagen
            if ruta_imagen.startswith("http"):
                response = requests.get(ruta_imagen)
                response.raise_for_status()  # Lanza un error si hay un problema en la descarga

                # Guardar la imagen temporalmente en la carpeta 'temp'
                with open(temp_image_path, 'wb') as tmp_file:
                    tmp_file.write(response.content)
                
                # Cargar la imagen desde la carpeta temporal
                pixbuf = GdkPixbuf.Pixbuf.new_from_file(temp_image_path)

            else:
                # Si es un archivo local, cargarlo directamente
                pixbuf = GdkPixbuf.Pixbuf.new_from_file(ruta_imagen)

            # Crear un Gtk.Image desde el Pixbuf cargado
            image_widget = Gtk.Image.new_from_pixbuf(pixbuf)
            image_widget.set_hexpand(True)
            image_widget.set_css_classes(["image-result"])

            # Actualizar el image_box con la imagen
            GLib.idle_add(update_image_box, image_box, image_widget)

        except Exception as e:
            print(f"Error al cargar la imagen: {e}")
            GLib.idle_add(update_image_box, image_box, Gtk.Label(label="Error al cargar la imagen"))

    threading.Thread(target=load_image, daemon=True).start()


def update_image_box(image_box, new_widget):
    """
    Actualiza el contenedor image_box con el nuevo widget (imagen o mensaje de carga/error).
    """
    # Eliminar cualquier widget existente en el image_box
    child = image_box.get_first_child()
    while child:
        image_box.remove(child)
        child = image_box.get_first_child()

    # Agregar el nuevo widget (ya sea la imagen o el mensaje de "Cargando..." o error)
    image_box.append(new_widget)
    image_box.show()


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
