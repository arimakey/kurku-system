import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

def show_location(change_screen, location_data):
    # Contenedor principal
    main_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
    main_container.set_margin_top(20)
    main_container.set_margin_bottom(20)
    main_container.set_margin_start(20)
    main_container.set_margin_end(20)
    main_container.get_style_context().add_class("location-container")

    # Título
    title_label = Gtk.Label(label="Detalles de la Ubicación")
    title_label.get_style_context().add_class("title-label")
    title_label.set_halign(Gtk.Align.CENTER)
    main_container.append(title_label)

    # Imagen centrada
    image_container = Gtk.Box()
    image_container.set_halign(Gtk.Align.CENTER)
    image_container.set_vexpand(False)

    image = Gtk.Picture.new_for_filename(location_data["image"])
    image.set_content_fit(Gtk.ContentFit.CONTAIN)
    image.set_size_request(300, 300)
    image_container.append(image)
    main_container.append(image_container)

    # Grid para la información de la ubicación
    info_grid = Gtk.Grid()
    info_grid.set_column_spacing(10)
    info_grid.set_row_spacing(10)
    info_grid.set_halign(Gtk.Align.CENTER)
    info_grid.get_style_context().add_class("info-grid")

    # Etiquetas de información
    name_label = Gtk.Label(label="Nombre:")
    name_label.get_style_context().add_class("info-title")
    name_value = Gtk.Label(label=location_data['name'])
    name_value.get_style_context().add_class("info-value")
    name_value.set_halign(Gtk.Align.START)

    description_label = Gtk.Label(label="Descripción:")
    description_label.get_style_context().add_class("info-title")
    description_value = Gtk.Label(label=location_data.get('description', 'No disponible'))
    description_value.get_style_context().add_class("info-value")
    description_value.set_halign(Gtk.Align.START)

    coordinates_label = Gtk.Label(label="Coordenadas:")
    coordinates_label.get_style_context().add_class("info-title")
    coordinates_value = Gtk.Label(label=location_data.get('coordinates', 'No disponible'))
    coordinates_value.get_style_context().add_class("info-value")
    coordinates_value.set_halign(Gtk.Align.START)

    # Añadir elementos al grid
    info_grid.attach(name_label, 0, 0, 1, 1)
    info_grid.attach(name_value, 1, 0, 1, 1)
    info_grid.attach(description_label, 0, 1, 1, 1)
    info_grid.attach(description_value, 1, 1, 1, 1)
    info_grid.attach(coordinates_label, 0, 2, 1, 1)
    info_grid.attach(coordinates_value, 1, 2, 1, 1)

    main_container.append(info_grid)

    # Botón de regreso
    back_button = Gtk.Button(label="Volver")
    back_button.get_style_context().add_class("back-button")
    back_button.set_halign(Gtk.Align.CENTER)
    back_button.connect("clicked", lambda button: change_screen("create_project"))

    main_container.append(back_button)

    return main_container