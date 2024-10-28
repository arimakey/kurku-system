import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GdkPixbuf
from utils.methods import apply_css, on_image_button_clicked

def select_place(on_previous_button_clicked):
         # Crear un Box vertical PRINCIPAL
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        main_box.set_margin_top(10)    # Margen superior
        main_box.set_margin_bottom(10)  # Margen inferior
        main_box.set_margin_start(10)   # Margen izquierdo
        main_box.set_margin_end(10)     # Margen derecho
        # self.set_child(main_box)

        # Crear un Box horizontal para el buscador
        search_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        search_box.set_margin_bottom(20)  # Margen inferior
        #search_box.set_valign(Gtk.Align.FILL)  # Alinear verticalmente para llenar

        # Crear un Box horizontal para el LOS RESULTADOS DE LA BUSQUEDA
        result_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        result_box.set_hexpand(True)
        result_box.set_vexpand(True)
        
        # Crear un Box Horizontal para los botones
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        button_box.set_valign(Gtk.Align.FILL)  # Alinear verticalmente para llenar

        # Agregar a main_box
        main_box.append(search_box)
        main_box.append(result_box)
        main_box.append(button_box)

    # BUSCADOR

         # Crear una CAJA DE ENTRADA DE TEXTO
        entry = Gtk.Entry()
        entry.set_placeholder_text("Nombre")  # Texto de sugerencia
        search_box.append(entry)
        entry.set_css_classes(["buscador"])  # Agregar una clase CSS
        entry.set_hexpand(True)

        # Crear un BOTON DE BUSQUEDA
        search_button=  Gtk.Button()
        search_button.set_css_classes(["buscador_boton"])  # Agregar una clase CSS 
        # Crear un contenedor horizontal para el ícono y el texto
        search_content= Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        search_content.set_margin_start(10)     # Margen derecho
        search_content.set_margin_end(10)     # Margen derecho
        # Crear el ícono
        icon_search = Gtk.Image.new_from_icon_name("folder-saved-search")
        # Crear una etiqueta con el texto
        label_search= Gtk.Label(label="Buscar")
        # Agregar el ícono y la etiqueta al contenedor
        search_content.append(icon_search)
        search_content.append(label_search)
        # Agregar el contenedor al botón
        search_button.set_child(search_content)

        search_box.append(search_button)
      
    # RESULTADOS E IMAGEN
        
        class Imagen:
                def __init__(self, nombre, ruta):
                    self.nombre = nombre
                    self.ruta = ruta
        # Crear una lista de objetos Imagen
        imagenes = [
            Imagen("Imagen 1", "https://earthengine.googleapis.com/v1/projects/prueba-imagen-satelital/thumbnails/467042e606a40d44549bfcbf5cd19e6c-483cfd6fcb1261c900f6b93dd69497a7:getPixels"),
            Imagen("Imagen 2", "images/seleccione.jpg"),
            Imagen("Imagen 3", "images/seleccione.jpg"),
            Imagen("Imagen 4", "images/seleccione.jpg"),
            Imagen("Imagen 5", "images/seleccione.jpg"),
            Imagen("Imagen 1", "images/seleccione.jpg"),
            Imagen("Imagen 2", "images/seleccione.jpg"),
            Imagen("Imagen 3", "images/seleccione.jpg"),
            Imagen("Imagen 4", "images/seleccione.jpg"),
            Imagen("Imagen 5", "images/seleccione.jpg")
        ]
        def mostrar_nombres():

            texto = entry.get_text()
            print(f"Buscando nombres que contengan: {texto}")
            # Inicializar child al primer hijo de result
            child = result_box.get_first_child()
            
            # Limpiar el área de resultados
            child = result_box.get_first_child()
            while child is not None:
                result_box.remove(child)
                child = result_box.get_first_child()
                
             # RESULTADOS
            #Crear un contenedor de resultados
            result = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
            # result.set_size_request(300, -1)
            result.set_css_classes(["box_result"])  # Agregar una clase CSS

             # Titulo
            text_result= Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            text_result.set_halign(Gtk.Align.CENTER)  # Alinear el contenido al centro

            label_result = Gtk.Label(label="Resultados")
            label_result.set_margin_top(10)  # Margen superior
            label_result.set_margin_bottom(0)  # Margen inferior
            label_result.set_css_classes(["label_result"])

            text_result.append(label_result)
            result.append(text_result)

            scrolled_result = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)

            # Crear un contenedor con barra de desplazamiento
            scrolled_window = Gtk.ScrolledWindow()
            scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)  # Desplazamiento solo vertical
            scrolled_window.set_min_content_height(320)  # Altura mínima visible
            # scrolled_window.set_hexpand(True)
            # scrolled_window.set_vexpand(False)
           
            scrolled_window.set_child(scrolled_result)
            # Agregar el contenedor de resultados al scrolled_window
            result.append(scrolled_window)

            result_box.append(result)

            # IMAGEN
            # Crear un contenedor para la imagen con tamaño fijo
            image_box = Gtk.Box()
            image_box.set_css_classes(["imagen_resultado"])  # Agregar una clase CSS
            image_box.set_size_request(250, 250)
            image_box.set_hexpand(True)
            image_box.set_vexpand(True)
            result_box.append(image_box)

            # Agregar cada nombre como un label en el área de resultados
            for imagen in imagenes:
                # Crear un botón para cada imagen
                button = Gtk.Button()
                button.set_margin_start(10)  # Margen izquierdo
                button.set_margin_end(10)    # Margen derecho
                button.set_css_classes(["lista_resultados"])  # Agregar una clase CSS
                button.set_hexpand(True)
                # Conectar el evento "clicked" al método para mostrar la imagen
                # Usar lambda para pasar argumentos adicionales
                button.connect("clicked", lambda btn, ruta=imagen.ruta: on_image_button_clicked(btn, image_box, ruta))  # Pasar el contenedor de imagen y la imagen actual
                # Crear una etiqueta con el nombre de la imagen
                label = Gtk.Label(label=imagen.nombre)
                label.set_margin_top(6)  # Margen superior
                label.set_margin_bottom(6)  # Margen inferior
                button.set_child(label)
                scrolled_result.append(button)
            #Mostrar imagen por defecto //Seleccione un opcion
            
            # Cargar la nueva imagen correspondiente
            pixbuf = GdkPixbuf.Pixbuf.new_from_file("images/seleccione.jpg")
            image_widget = Gtk.Image.new_from_pixbuf(pixbuf)
            image_widget.set_css_classes(["imagen_resultado"])

            image_widget.set_hexpand(True)

            # Agregar la nueva imagen al image_box
            image_box.append(image_widget)
            image_box.show()

          # Conectar el botón de búsqueda para mostrar los nombres
        search_button.connect("clicked", lambda btn: mostrar_nombres())
    
     # CONTENIDO PARA ANTERIOR Y SIGUIENTE
        back_button=  Gtk.Button()
        back_button.connect("clicked", on_previous_button_clicked)
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

        next_button=  Gtk.Button()
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
        back_button.set_css_classes(["button"])
        next_button.set_css_classes(["button"])

        button_box.append(back_button)

        spacer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        spacer.set_hexpand(True)  # Permitir que se expanda horizontalmente
        button_box.append(spacer)

        # Hacer que el segundo botón se alinee a la derecha
        button_box.append(next_button)
        button_box.set_margin_top(15)

        apply_css()
    
        return main_box

            
        

        
