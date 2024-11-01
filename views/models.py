import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gdk, Gio
from utils.methods import apply_css, on_button_clicked_satellite, on_button_clicked_model
from components.btn_direction import create_next_and_previous

def models(change_screen):
    main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
    # window.set_child(main_box) Agregar el Box a la ventana

    # Crear un Box horizontal
    select_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    select_box.set_valign(Gtk.Align.FILL)  # Alinear verticalmente para llenar

    button_box = create_next_and_previous(change_screen, "main_screen", "select_place")

    # Agregar a main_box
    main_box.append(select_box)
    main_box.append(button_box)

    # Crear un Box Vertical para SATELITE
    satellite_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    satellite_box.set_hexpand(True)  # Permitir que se expanda horizontalmente
    satellite_box.set_margin_end(10)   # Margen izquierdo
    satellite_box.set_size_request(200, -1)

    # Crear un Box Vertical para MODELO
    model_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    model_box.set_hexpand(True)  # Permitir que se expanda horizontalmente
    model_box.set_margin_start(10)     # Margen derecho
    model_box.set_size_request(300,-1)

    select_box.append(satellite_box)
    select_box.append(model_box)

# CONTENIDO PARA SATELITE
    # Titulo
    text_satellite = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    text_satellite.set_halign(Gtk.Align.CENTER)  # Alinear el contenido al centro

    label_satellite = Gtk.Label(label="Satelite")
    label_satellite.set_css_classes(["tittle-label"])

    text_satellite.append(label_satellite)
    satellite_box.append(text_satellite)

    # Botones
    button_satellite = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    button_satellite.set_valign(Gtk.Align.FILL)  # Alinear verticalmente para llenar
    satellite_box.append(button_satellite)


    square_satellite = create_option("Landstad", "Satelite", "icons/Rectangle 87.svg")
    triangle_satellite = create_option("Landstad", "Satelite", "icons/Polygon 1.svg")

    # Agregar clases
    square_satellite.set_css_classes(["btn_item"])
    square_satellite.get_style_context().add_class("selected")  # Seleccionado por defecto
    # Imprimir en consola que el primer botón está seleccionado por defecto
    on_button_clicked_satellite(None, square_satellite, triangle_satellite, 'Satelite 1')  # Llamada inicial
    
    triangle_satellite.set_css_classes(["btn_item"])

    # Conectar señales de clic a los botones
    square_satellite.connect("clicked", on_button_clicked_satellite, square_satellite, triangle_satellite, 'Satelite 1')
    triangle_satellite.connect("clicked", on_button_clicked_satellite, triangle_satellite, square_satellite,'Satelite 2')

    button_satellite.append(square_satellite)
    button_satellite.append(triangle_satellite)

# CONTENIDO PARA MODELO
    # Titulo
    text_model = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    text_model.set_halign(Gtk.Align.CENTER)  # Alinear el contenido al centro

    label_model = Gtk.Label(label="Modelo")
    label_model.set_css_classes(["tittle-label"])

    text_model.append(label_model)
    model_box.append(text_model)

    # Botones
    button_model = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    model_box.append(button_model)
        
    star_model = create_option("Srt 1", "Model", "icons/Star 1.svg")
    diamond_model = create_option("SRT '1","Modelo","icons/Rectangle 93.svg")
    circle_model = create_option("SRT'2", "Modelo", "icons/Ellipse 9.svg")

    circle_model.get_style_context().add_class("selected")  # Seleccionado por defecto

    # Conectar señales de clic a los botones
    circle_model.connect("clicked", on_button_clicked_model, circle_model, star_model,diamond_model, 'Modelo 1')
    star_model.connect("clicked", on_button_clicked_model, star_model, diamond_model, circle_model, 'Modelo 2')
    diamond_model.connect("clicked", on_button_clicked_model, diamond_model, circle_model,star_model,'Modelo 3')

    button_model.append(circle_model)
    button_model.append(star_model)
    button_model.append(diamond_model)
    
    return main_box

def create_section():
    return

def create_option(name_button, type_button, icon):
    option_button = Gtk.Button()
    option_button.set_hexpand(True)
    option_button.set_vexpand(True)
    
    label_1 = Gtk.Label(label=name_button)
    label_2 = Gtk.Label(label=type_button)
    label_2.set_css_classes(["tittle-label"])
    
    file_svg = Gio.File.new_for_path(icon)
    svg=Gdk.Texture.new_from_file(file_svg)

    image = Gtk.Image.new_from_paintable(svg)
    image.set_pixel_size(50)

    content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
    content.set_halign(Gtk.Align.CENTER)
    content.set_valign(Gtk.Align.CENTER)
    content.append(image)
    label_1.set_css_classes(["tittle-label_"])
    content.append(label_1)
    content.append(label_2)
    option_button.set_child(content) 
    option_button.set_css_classes(["btn_item"])
    
    return option_button