import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gdk, Gio
from utils.methods import apply_css, on_button_clicked_satellite
from components.btn_direction import create_next_and_previous

def select_models(change_screen, save_project_data):
    main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

    select_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    select_box.set_valign(Gtk.Align.FILL)
    button_box = create_next_and_previous(change_screen, "create_project", "select_place")

    main_box.append(select_box)
    main_box.append(button_box)

    # SATÉLITES
    satellite_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    satellite_box.set_hexpand(True)
    satellite_box.set_margin_end(10)
    satellite_box.set_size_request(200, -1)

    # MODELOS
    model_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    model_box.set_hexpand(True)
    model_box.set_margin_start(10)
    model_box.set_size_request(300, -1)

    select_box.append(satellite_box)
    select_box.append(model_box)

    # CONTENIDO PARA SATÉLITE
    # Título
    text_satellite = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    text_satellite.set_halign(Gtk.Align.CENTER)

    label_satellite = Gtk.Label(label="Satélite")
    label_satellite.set_css_classes(["title-label"])

    text_satellite.append(label_satellite)
    satellite_box.append(text_satellite)

    # Botones
    button_satellite = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    button_satellite.set_valign(Gtk.Align.FILL)
    satellite_box.append(button_satellite)

    square_satellite = create_option("Landstad", "Satélite", "icons/Rectangle 87.svg")
    triangle_satellite = create_option("Landstad", "Satélite", "icons/Polygon 1.svg")

    # Agregar clases
    square_satellite.set_css_classes(["button-item"])
    square_satellite.get_style_context().add_class("selected")  # Seleccionado por defecto
    on_button_clicked_satellite(None, square_satellite, triangle_satellite, 'Satélite 1')

    triangle_satellite.set_css_classes(["button-item"])

    # Conectar señales de clic a los botones
    square_satellite.connect("clicked", on_button_clicked_satellite, square_satellite, triangle_satellite, 'Satélite 1')
    triangle_satellite.connect("clicked", on_button_clicked_satellite, triangle_satellite, square_satellite, 'Satélite 2')

    button_satellite.append(square_satellite)
    button_satellite.append(triangle_satellite)

    # CONTENIDO PARA MODELO
    # Título
    text_model = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    text_model.set_halign(Gtk.Align.CENTER)

    label_model = Gtk.Label(label="Modelo")
    label_model.set_css_classes(["title-label"])

    text_model.append(label_model)
    model_box.append(text_model)

    # Botones
    button_model = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    model_box.append(button_model)

    star_model = create_option("SRT 1", "Modelo", "icons/Star 1.svg")
    diamond_model = create_option("SRT' 1", "Modelo", "icons/Rectangle 93.svg")
    circle_model = create_option("SRT-2", "Modelo", "icons/Ellipse 9.svg")

    # Asignar la clase 'selected' al primer modelo (por defecto)
    circle_model.get_style_context().add_class("selected")

    # Llamar a `save_project_data` para guardar el modelo por defecto
    save_project_data('model', 'Modelo 1')

    # Conectar señales de clic a los botones
    circle_model.connect("clicked", on_button_clicked_model, circle_model, star_model, diamond_model, 'model', 'RandomForest', save_project_data)
    star_model.connect("clicked", on_button_clicked_model, star_model, diamond_model, circle_model, 'model', 'Modelo 2', save_project_data)
    diamond_model.connect("clicked", on_button_clicked_model, diamond_model, circle_model, star_model, 'model', 'Modelo 3', save_project_data)

    button_model.append(circle_model)
    button_model.append(star_model)
    button_model.append(diamond_model)

    return main_box

def create_option(name_button, type_button, icon):
    option_button = Gtk.Button()
    option_button.set_hexpand(True)
    option_button.set_vexpand(True)

    label_1 = Gtk.Label(label=name_button)
    label_2 = Gtk.Label(label=type_button)
    label_2.set_css_classes(["title-label-item"])

    # Cargar el archivo SVG para el icono
    file_svg = Gio.File.new_for_path(icon)
    svg = Gdk.Texture.new_from_file(file_svg)

    image = Gtk.Image.new_from_paintable(svg)
    image.set_pixel_size(50)

    # Crear un contenedor para el contenido
    content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
    content.set_halign(Gtk.Align.CENTER)
    content.set_valign(Gtk.Align.CENTER)
    content.append(image)
    label_1.set_css_classes(["subtitle-label"])
    content.append(label_1)
    content.append(label_2)

    # Asignar el contenido al botón
    option_button.set_child(content)
    option_button.set_css_classes(["button-item"])

    return option_button


def on_button_clicked_model(self, button_selected, other_button1, other_button2, field, name_button, save_project_data):
    # Mostrar el botón seleccionado en la consola
    print(f"{name_button} seleccionado")
    
    # Cambiar el estilo de los botones (marcar el seleccionado)
    button_selected.get_style_context().add_class("selected")
    other_button1.get_style_context().remove_class("selected")
    other_button2.get_style_context().remove_class("selected")

    # Guardar los datos del proyecto al seleccionar un modelo
    save_project_data(field, name_button)
