import os
import shutil
import uuid
import asyncio
from gi.repository import GLib, Gtk
from modules import earth_images  # Asegúrate de que la función 'descargar_imagenes' esté en este módulo

# Función asincrónica para manejar la carga del proyecto
async def loading_project_async(project, save_data, save_xml, change_screen):
    # Contenedor principal
    main_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
    main_container.set_margin_top(30)
    main_container.set_margin_bottom(30)
    main_container.set_margin_start(50)
    main_container.set_margin_end(50)
    main_container.get_style_context().add_class("loading-container")

    # Título
    title_label = Gtk.Label(label="Cargando Proyecto")
    title_label.get_style_context().add_class("title-label")
    title_label.set_halign(Gtk.Align.CENTER)
    main_container.append(title_label)

    # Barra de progreso
    progress_bar = Gtk.ProgressBar()
    progress_bar.set_show_text(True)
    main_container.append(progress_bar)

    # Mensaje de estado
    message_label = Gtk.Label(label="Iniciando carga del proyecto...")
    message_label.set_halign(Gtk.Align.CENTER)
    message_label.set_valign(Gtk.Align.CENTER)
    main_container.append(message_label)

    # Función para actualizar el progreso
    def update_progress(progress, message):
        progress_bar.set_fraction(progress)  # Actualiza el progreso de la barra (0.0 a 1.0)
        message_label.set_label(message)  # Actualiza el mensaje

        # Si el progreso ha llegado al 100%, iniciar el siguiente paso
        if progress >= 1.0:
            GLib.timeout_add(500, lambda: change_screen("create_project"))  # Cambiar pantalla después de 500ms

    # Función asincrónica para guardar el proyecto en una carpeta específica
    async def save_project_folder_async(project_data):
        # Crear una carpeta con el nombre del proyecto y un ID único
        project_name = project_data["name"]
        project_id = str(uuid.uuid4())  # Generar un ID único para el proyecto
        project_folder = os.path.join("projects", f"{project_name}_{project_id}")

        # Crear la carpeta si no existe
        if not os.path.exists(project_folder):
            os.makedirs(project_folder)

        # Guardar los datos del proyecto
        save_data('analysis_route', project_folder)  # Usamos la función `save_data` para guardar los datos en el archivo

        # Mover la imagen temporal a la carpeta del proyecto como 'preview.jpg'
        temp_image_path = "/temp/tmp_img.jpg"  # Ruta temporal de la imagen
        if os.path.exists(temp_image_path):
            preview_image_path = os.path.join(project_folder, "preview.jpg")
            shutil.move(temp_image_path, preview_image_path)  # Mover la imagen a la nueva carpeta
            print(f"Imagen movida a: {preview_image_path}")

        # Descargar las imágenes satelitales para el proyecto
        longitud = project_data["longitude"]
        latitud = project_data["latitude"]
        await earth_images.descargar_imagenes(longitud, latitud, project_folder)  # Llamamos al método de earth_images

    # Función para comenzar la carga real del proyecto
    async def begin_loading():
        progress = 0.0
        messages = ["Iniciando carga...", "Creando carpeta de proyecto...", "Guardando datos...", "Descargando imágenes...", "Finalizando..."]

        def update_simulation():
            nonlocal progress
            if progress < 1.0:
                progress += 0.2  # Incrementar el progreso en 0.2 para ajustarse a los 5 pasos

                message_index = int(progress / 0.2)

                # Evitar que el índice exceda el tamaño de la lista 'messages'
                message_index = min(message_index, len(messages) - 1)

                update_progress(progress, messages[message_index])

                if message_index == 1:  # Cuando se crea la carpeta, llamamos a la función real
                    asyncio.create_task(save_project_folder_async(project))  # Llamar la función asincrónica

                return True  # Mantener la simulación activa
            else:
                update_progress(1.0, "Proyecto cargado con éxito.")  # Último mensaje
                return False  # Detener la simulación

        # Iniciar la simulación de carga
        GLib.timeout_add(1000, update_simulation)

    # Inicia el proceso asincrónico de carga
    await begin_loading()

    return main_container


# Función principal que maneja el bucle de eventos
def loading_project(project, save_data, save_xml, change_screen):
    loop = asyncio.get_event_loop()

    # Ejecuta el bucle de eventos GTK y asyncio de manera conjunta
    def run_async():
        loop.run_until_complete(loading_project_async(project, save_data, save_xml, change_screen))

    # Ejecutamos el proceso asincrónico
    GLib.idle_add(run_async)

    return Gtk.Window()  # Retorna una ventana vacía mientras el proceso carga
