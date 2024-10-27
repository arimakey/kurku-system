import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gio, Gdk,GdkPixbuf

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


def on_image_button_clicked(button, image_box, ruta_imagen):
    """
    Llama a la función para mostrar la imagen en el contenedor `image_box`.
    """
    mostrar_imagen(image_box, ruta_imagen)

def mostrar_imagen(image_box, ruta_imagen):
    """
    Muestra la imagen en el contenedor `image_box`, reemplazando cualquier imagen anterior.
    """
    # Eliminar cualquier imagen previa del image_box
    child = image_box.get_first_child()
    while child:
        image_box.remove(child)
        child = image_box.get_first_child()  # Actualizar al nuevo primer hijo después de la eliminación

    # Cargar la nueva imagen correspondiente
    pixbuf = GdkPixbuf.Pixbuf.new_from_file(ruta_imagen)
    image_widget = Gtk.Image.new_from_pixbuf(pixbuf)
    image_widget.set_hexpand(True)
    image_widget.set_css_classes(["imagen_resultado"])


    # Agregar la nueva imagen al image_box
    image_box.append(image_widget)
    image_box.show()

    return image_widget  # Devolver el widget para ser reutilizado
