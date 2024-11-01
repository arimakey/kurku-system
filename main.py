import gi
gi.require_version("Gtk", "4.0")
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw

# Importar las pantallas desde los archivos
from views.models import models
from views.select_place import select_place
from views.create_project import create_project
from utils.methods import apply_css
from data.locations import locations

class MainWindow(Gtk.ApplicationWindow):
    title = "Kurku"
    
    def __init__(self, app):
        super().__init__(application=app)
        self.set_title(self.title)
        self.set_default_size(800, 600)

        # Crear una barra de herramientas (HeaderBar)
        header = Gtk.HeaderBar()
        header.set_title_widget(Gtk.Label(label=self.title))
        header.set_show_title_buttons(True)
        self.set_titlebar(header)

        apply_css()

        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        main_box.set_margin_top(30)
        main_box.set_margin_bottom(30)
        main_box.set_margin_start(50)
        main_box.set_margin_end(50)
        self.set_child(main_box)

        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.stack.set_transition_duration(250)

        main_box.append(self.stack)

        self.create_and_add_screens()

    def create_and_add_screens(self):
        main_screen = create_project(self.change_screen, locations)
        options_screen = models(self.change_screen)
        place_screen = select_place(self.change_screen)
        
        self.stack.add_named(main_screen, "main_screen")
        self.stack.add_named(options_screen, "project_options")
        self.stack.add_named(place_screen, "select_place")

    def change_screen(self, screen):
        self.stack.set_visible_child_name(screen)
        
class MainApp(Adw.Application):
    def __init__(self):
        super().__init__(application_id="com.models")
        
    def do_activate(self):
        win = MainWindow(self)
        win.present()

# Crear y ejecutar la aplicación
app = MainApp()
app.run(None)
