import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

def create_add_location_view(change_screen, save_project_data, save_project_to_xml):
    # Crear contenedor principal
    main_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
    main_container.get_style_context().add_class("background-custom")

    # Crear formulario para ingresar datos
    form_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
    
    # Campo para ingresar el nombre
    name_entry_label = Gtk.Label(label="Nombre:")
    name_entry_label.get_style_context().add_class("title-label")
    name_entry = Gtk.Entry()
    name_entry.set_placeholder_text("Ingrese el nombre")
    name_entry.get_style_context().add_class("input-field")

    # Campo para ingresar la descripción
    description_entry_label = Gtk.Label(label="Descripción:")
    description_entry_label.get_style_context().add_class("title-label")
    description_entry = Gtk.TextView()
    description_entry.get_style_context().add_class("input-field")
    description_scroll = Gtk.ScrolledWindow()
    description_scroll.set_child(description_entry)
    description_scroll.set_vexpand(True)

    # Agregar un placeholder manualmente usando una etiqueta de texto (ya que Gtk.TextView no soporta placeholder directamente)
    description_placeholder_label = Gtk.Label(label="Ingrese la descripción")
    description_placeholder_label.get_style_context().add_class("placeholder-label")
    description_placeholder_label.set_margin_start(10)
    description_placeholder_label.set_margin_top(10)
    description_placeholder_label.set_visible(True)

    # Menú desplegable para seleccionar el estado
    state_label = Gtk.Label(label="Estado:")
    state_label.get_style_context().add_class("title-label")
    state_combo = Gtk.ComboBoxText()
    state_combo.append("active", "Activo")
    state_combo.append("inactive", "Inactivo")
    state_combo.set_active(0)  # Predeterminado en "Activo"
    state_combo.get_style_context().add_class("input-field")

    # Agregar campos al formulario
    form_container.append(name_entry_label)
    form_container.append(name_entry)
    form_container.append(description_entry_label)
    form_container.append(description_scroll)
    form_container.append(state_label)
    form_container.append(state_combo)

    # Crear botones de acción
    save_button = Gtk.Button(label="Guardar")
    save_button.get_style_context().add_class("button-primary")
    save_button.connect("clicked", lambda x: save_location_data(
        name_entry.get_text(),
        description_entry.get_buffer().get_text(description_entry.get_buffer().get_start_iter(), description_entry.get_buffer().get_end_iter(), True),  # Obtener todo el texto del TextView
        state_combo.get_active_id(),
        change_screen,
        save_project_data,
        save_project_to_xml
    ))
    
    cancel_button = Gtk.Button(label="Cancelar")
    cancel_button.get_style_context().add_class("button-primary")
    cancel_button.connect("clicked", lambda x: change_screen("previous_screen"))  # Cambiar "previous_screen" por el nombre real de la pantalla anterior

    # Crear barra de botones
    buttons_container = Gtk.Box(spacing=10)
    buttons_container.append(save_button)
    buttons_container.append(cancel_button)

    # Agregar formulario y botones al contenedor principal
    main_container.append(form_container)
    main_container.append(buttons_container)

    return main_container

def save_location_data(name, description, state, change_screen, save_project_data, save_project_to_xml):
    """
    Función para guardar los datos ingresados y realizar una acción (como volver a la pantalla principal).
    Aquí solo mostramos los datos por simplicidad.
    """
    print(f"Nombre: {name}")
    print(f"Descripción: {description}")
    print(f"Estado: {state}")
    
    # Aquí puedes agregar la lógica para guardar los datos en una base de datos o realizar alguna acción.

    # Si usas save_project_data, podrías almacenar esos datos de alguna manera, por ejemplo:
    save_project_data("name", name)
    save_project_data("description", description)
    save_project_data("state", state)

    # Si tienes un método save_project_to_xml, puedes invocar también allí
    save_project_to_xml()

    # Volver a la pantalla principal (cambiar según tu lógica)
    change_screen("previous_screen")
