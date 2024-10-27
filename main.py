import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

# Importar las pantallas desde los archivos
from screens.models import models
from screens.select_place import select_place
from utils.methods import apply_css

class MainWindow(Gtk.Window):
    def __init__(self, app):
        super().__init__(application=app)
        self.set_title("Kurku")
        self.set_default_size(800, 600)

        # Crear una barra de herramientas (HeaderBar)
        header = Gtk.HeaderBar()
        header.set_title_widget(Gtk.Label(label="Kurku"))  # Establecer el título en la barra
        header.set_show_title_buttons(True)  # Mostrar botones de cerrar, minimizar, maximizar
        self.set_titlebar(header)

        # Aplicar estilo personalizado
        apply_css()

        # Crear un Box vertical PRINCIPAL
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        main_box.set_margin_top(30)    # Margen superior
        main_box.set_margin_bottom(30)  # Margen inferior
        main_box.set_margin_start(50)   # Margen izquierdo
        main_box.set_margin_end(50)     # Margen derecho
        self.set_child(main_box) # Agregar el Box a la ventana

        # Crear el Stack
        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.stack.set_transition_duration(250)

        # Agregar el Stack al main_box sin el StackSwitcher
        main_box.append(self.stack)

        # Crear y agregar las pantallas
        self.create_and_add_screens()

    def create_and_add_screens(self):
        # Crear las pantallas importadas y agregar al Stack
        screen1 = models(self.on_next_button_clicked)
        screen2 = select_place(self.on_previous_button_clicked)
        
        # Agregar pantallas al Stack con nombres para referencia, pero sin mostrar los títulos
        self.stack.add_named(screen1, "screen1")
        self.stack.add_named(screen2, "screen2")

    def on_next_button_clicked(self, button):
        # Cambia a la siguiente pantalla (Pantalla 2)
        self.stack.set_visible_child_name("screen2")

    def on_previous_button_clicked(self, button):
        # Cambia a la pantalla anterior (Pantalla 1)
        self.stack.set_visible_child_name("screen1")


class MainApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="com.models")
        
    def do_activate(self):
        # Crear la ventana principal y mostrarla
        win = MainWindow(self)
        win.present()

# Crear y ejecutar la aplicación
app = MainApp()
app.run(None)
