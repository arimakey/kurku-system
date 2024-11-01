import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gdk, Gio

def create_next_and_previous(change_screen, to_previous, to_next):
    button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    button_box.set_valign(Gtk.Align.FILL)
    
    # CONTENIDO PARA ANTERIOR Y SIGUIENTE
    back_button = Gtk.Button()
    back_button.connect("clicked", lambda x: change_screen(to_previous))
    
    # Crear un contenedor horizontal para el ícono y el texto
    back_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
    back_box.set_margin_start(10)     # Margen derecho
    back_box.set_margin_end(10)     # Margen derecho
    # Crear el ícono
    icon_back = Gtk.Image.new_from_icon_name("go-previous")
    # Crear una etiqueta con el texto
    label_back = Gtk.Label(label="Anterior")
    # Agregar el ícono y la etiqueta al contenedor
    back_box.append(icon_back)
    back_box.append(label_back)
    # Agregar el contenedor al botón
    back_button.set_child(back_box)

    next_button = Gtk.Button()
    # next_button.connect("clicked", Methods(self).change_screen, window)
    next_button.connect("clicked", lambda x: change_screen(to_next))
    # Crear un contenedor horizontal para el ícono y el texto
    next_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
    next_box.set_margin_start(10)     # Margen derecho
    next_box.set_margin_end(10)     # Margen derecho
    # Crear el ícono
    icon_next = Gtk.Image.new_from_icon_name("go-next")
    # Crear una etiqueta con el texto
    label_next = Gtk.Label(label="Siguiente")
    # Agregar el ícono y la etiqueta al contenedor
    next_box.append(label_next)
    next_box.append(icon_next)
    # Agregar el contenedor al botón
    next_button.set_child(next_box)

        # Agregar clases
    back_button.set_css_classes(["btn_primary"])
    next_button.set_css_classes(["btn_primary"])

    button_box.append(back_button)

    spacer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
    spacer.set_hexpand(True)  # Permitir que se expanda horizontalmente

    button_box.append(spacer)
    # Hacer que el segundo botón se alinee a la derecha
    button_box.append(next_button)
    button_box.set_margin_top(15)
    
    return button_box
