import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

def create_next_and_previous(change_screen, to_previous, to_next):
    """
    Crea un contenedor con botones de navegación 'Anterior' y 'Siguiente'.
    """
    button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    button_box.set_valign(Gtk.Align.FILL)

    # Botón 'Anterior'
    back_button = Gtk.Button()
    back_button.connect("clicked", lambda x: change_screen(to_previous))

    # Crear un contenedor horizontal para el ícono y el texto del botón 'Anterior'
    back_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
    back_box.set_margin_start(10)  # Margen izquierdo
    back_box.set_margin_end(10)  # Margen derecho
    icon_back = Gtk.Image.new_from_icon_name("go-previous")
    label_back = Gtk.Label(label="Anterior")
    back_box.append(icon_back)
    back_box.append(label_back)
    back_button.set_child(back_box)
    back_button.set_css_classes(["button-primary"])  # Actualización del nombre de clase CSS

    # Botón 'Siguiente'
    next_button = Gtk.Button()
    next_button.connect("clicked", lambda x: change_screen(to_next))

    # Crear un contenedor horizontal para el ícono y el texto del botón 'Siguiente'
    next_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
    next_box.set_margin_start(10)  # Margen izquierdo
    next_box.set_margin_end(10)  # Margen derecho
    icon_next = Gtk.Image.new_from_icon_name("go-next")
    label_next = Gtk.Label(label="Siguiente")
    next_box.append(label_next)
    next_box.append(icon_next)
    next_button.set_child(next_box)
    next_button.set_css_classes(["button-primary"])  # Actualización del nombre de clase CSS

    # Agregar los botones al contenedor principal
    button_box.append(back_button)

    spacer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
    spacer.set_hexpand(True)  # Permitir que se expanda horizontalmente
    button_box.append(spacer)

    button_box.append(next_button)
    button_box.set_margin_top(15)

    return button_box
