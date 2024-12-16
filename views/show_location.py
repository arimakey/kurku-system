import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

def show_location(change_screen, location_data):
    # Contenedor principal
    main_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
    main_container.set_margin_top(10)
    main_container.set_margin_bottom(10)
    main_container.set_margin_start(10)
    main_container.set_margin_end(10)
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
    image.set_size_request(200, 200)
    image_container.append(image)
    main_container.append(image_container)

    # Grid para la información de la ubicación
    info_grid = Gtk.Grid()
    info_grid.set_column_spacing(10)
    info_grid.set_row_spacing(10)
    info_grid.set_halign(Gtk.Align.CENTER)
    info_grid.get_style_context().add_class("info-grid")

    # Añadir elementos al grid de forma dinámica
    row = 0
    for key, value in location_data.items():
        if key == "longitude" or key == "latitude":  # Mostrar latitud y longitud
            label = Gtk.Label(label=f"{key.capitalize()}:")
            label.get_style_context().add_class("info-title")
            value_label = Gtk.Label(label=str(value))
            value_label.get_style_context().add_class("info-value")
            value_label.set_halign(Gtk.Align.START)

            # Añadir los widgets al grid
            info_grid.attach(label, 0, row, 1, 1)
            info_grid.attach(value_label, 1, row, 1, 1)
            row += 1
        elif key != "image" and key != "longitude" and key != "latitude":  # Excluir image, longitude y latitude
            label = Gtk.Label(label=f"{key.capitalize()}:")
            label.get_style_context().add_class("info-title")
            value_label = Gtk.Label(label=str(value))
            value_label.get_style_context().add_class("info-value")
            value_label.set_halign(Gtk.Align.START)

            # Añadir los widgets al grid
            info_grid.attach(label, 0, row, 1, 1)
            info_grid.attach(value_label, 1, row, 1, 1)
            row += 1

    # Mostrar la ruta del proyecto
    project_route_label = Gtk.Label(label=f"Ruta del proyecto: {location_data.get('analysis_route', 'No disponible')}")
    project_route_label.get_style_context().add_class("info-title")
    project_route_label.set_halign(Gtk.Align.START)
    main_container.append(project_route_label)

    # Añadir el grid al contenedor principal
    main_container.append(info_grid)

    # Botón de regreso
    back_button = Gtk.Button(label="Volver")
    back_button.get_style_context().add_class("back-button")
    back_button.set_halign(Gtk.Align.CENTER)
    back_button.connect("clicked", lambda button: change_screen("create_project"))

    main_container.append(back_button)

    return main_container
