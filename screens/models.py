import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gdk, Gio
from utils.methods import apply_css, on_button_clicked_satellite, on_button_clicked_model

    # Crear un Box vertical PRINCIPAL
def models(on_next_button_clicked):
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        main_box.set_margin_top(10)    # Margen superior
        main_box.set_margin_bottom(10)  # Margen inferior
        main_box.set_margin_start(10)   # Margen izquierdo
        main_box.set_margin_end(10)     # Margen derecho
        # window.set_child(main_box) Agregar el Box a la ventana

        # Crear un Box horizontal
        select_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        select_box.set_valign(Gtk.Align.FILL)  # Alinear verticalmente para llenar

        # Crear un Box Horizontal para los botones
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        button_box.set_valign(Gtk.Align.FILL)  # Alinear verticalmente para llenar

        # Agregar a main_box
        main_box.append(select_box)
        main_box.append(button_box)

        # Crear un Box Vertical para SATELITE
        satellite_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        satellite_box.set_hexpand(False)  # Permitir que se expanda horizontalmente
        satellite_box.set_margin_end(10)   # Margen izquierdo
        satellite_box.set_size_request(300, -1)

        # Crear un Box Vertical para MODELO
        model_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        model_box.set_hexpand(True)  # Permitir que se expanda horizontalmente
        model_box.set_margin_start(10)     # Margen derecho

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

        # BOTON SATELITE CUADRADO
        square_satellite = Gtk.Button()
         # Cargar el archivo SVG como textura
        route_svg_square= "icons/Rectangle 87.svg"
        file_svg_square = Gio.File.new_for_path(route_svg_square)
        svg_square=Gdk.Texture.new_from_file(file_svg_square)
        # Crear una imagen con la textura SVG
        image_square = Gtk.Image.new_from_paintable(svg_square)
        image_square.set_pixel_size(50)
        # Bloque de contenido para el boton SQUARE
        content_square = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        content_square.set_halign(Gtk.Align.CENTER)
        content_square.set_valign(Gtk.Align.CENTER)
        content_square.append(image_square)
        label_square1 = Gtk.Label(label="Landstad")
        label_square2=Gtk.Label(label="Satelite")
        label_square2.set_css_classes(["tittle-label"])
        label_square1.set_css_classes(["tittle-label_"])
        content_square.append(label_square1)
        content_square.append(label_square2)
        square_satellite.set_child(content_square)  # Agregar el contenido al botón

        # BOTON SATELITE TRIANGULO
        triangle_satellite = Gtk.Button()
         # Cargar el archivo SVG como textura
        route_svg_triangle= "icons/Polygon 1.svg"
        file_svg_triangle = Gio.File.new_for_path(route_svg_triangle)
        svg_triangle=Gdk.Texture.new_from_file(file_svg_triangle)
        # Crear una imagen con la textura SVG
        image_triangle = Gtk.Image.new_from_paintable(svg_triangle)
        image_triangle.set_pixel_size(50)
        # Bloque de contenido para el boton SQUARE
        content_triangle = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        content_triangle.set_halign(Gtk.Align.CENTER)
        content_triangle.set_valign(Gtk.Align.CENTER)
        content_triangle.append(image_triangle)
        label_triangle1 = Gtk.Label(label="Landstad")
        label_triangle2=Gtk.Label(label="Satelite")
        label_triangle2.set_css_classes(["tittle-label"])
        label_triangle1.set_css_classes(["tittle-label_"])
        content_triangle.append(label_triangle1)
        content_triangle.append(label_triangle2)
        triangle_satellite.set_child(content_triangle)  # Agregar el contenido al botón

        # Hacer que ocupe todo el espacio disponible
        square_satellite.set_hexpand(True)
        triangle_satellite.set_hexpand(True)
        square_satellite.set_vexpand(True)
        triangle_satellite.set_vexpand(True)

        # Agregar clases
        square_satellite.set_css_classes(["button"])
        square_satellite.get_style_context().add_class("selected")  # Seleccionado por defecto
        # Imprimir en consola que el primer botón está seleccionado por defecto
        on_button_clicked_satellite(None, square_satellite, triangle_satellite, 'Satelite 1')  # Llamada inicial
        
        triangle_satellite.set_css_classes(["button"])

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
         #button_model.set_valign(Gtk.Align.FILL)  # Alinear verticalmente para llenar
        model_box.append(button_model)

        # BOTON MODELO CIRCULO
        circle_model = Gtk.Button()
         # Cargar el archivo SVG como textura
        route_svg_circle= "icons/Ellipse 9.svg"
        file_svg_circle = Gio.File.new_for_path(route_svg_circle)
        svg_circle=Gdk.Texture.new_from_file(file_svg_circle)
        # Crear una imagen con la textura SVG
        image_circle = Gtk.Image.new_from_paintable(svg_circle)
        image_circle.set_pixel_size(50)
        # Bloque de contenido para el boton CICRCLE
        content_circle = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        content_circle.set_halign(Gtk.Align.CENTER)
        content_circle.set_valign(Gtk.Align.CENTER)
        content_circle.append(image_circle)
        label_circle1 = Gtk.Label(label="SRT '2")
        label_circle2 = Gtk.Label(label="Modelo")
        label_circle2.set_css_classes(["tittle-label"])
        label_circle1.set_css_classes(["tittle-label_"])
        content_circle.append(label_circle1)
        content_circle.append(label_circle2)
        circle_model.set_child(content_circle)  # Agregar el contenido al botón

        # BOTON MODELO STAR
        star_model = Gtk.Button()
         # Cargar el archivo SVG como textura
        route_svg_star= "icons/Star 1.svg"
        file_svg_star = Gio.File.new_for_path(route_svg_star)
        svg_star=Gdk.Texture.new_from_file(file_svg_star)
        # Crear una imagen con la textura SVG
        image_star = Gtk.Image.new_from_paintable(svg_star)
        image_star.set_pixel_size(50)
        # Bloque de contenido para el boton STAR
        content_star = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        content_star.set_halign(Gtk.Align.CENTER)
        content_star.set_valign(Gtk.Align.CENTER)
        content_star.append(image_star)
        label_star1 = Gtk.Label(label="SRT '1")
        label_star2 = Gtk.Label(label="Modelo")
        label_star2.set_css_classes(["tittle-label"])
        label_star1.set_css_classes(["tittle-label_"])
        content_star.append(label_star1)
        content_star.append(label_star2)
        star_model.set_child(content_star)  # Agregar el contenido al botón

        # BOTON MODELO DIAMOND
        diamond_model = Gtk.Button()
         # Cargar el archivo SVG como textura
        route_svg_diamond= "icons/Rectangle 93.svg"
        file_svg_diamond = Gio.File.new_for_path(route_svg_diamond)
        svg_diamond=Gdk.Texture.new_from_file(file_svg_diamond)
        # Crear una imagen con la textura SVG
        image_diamond = Gtk.Image.new_from_paintable(svg_diamond)
        image_diamond.set_pixel_size(50)
        # Bloque de contenido para el boton DIAMOND
        content_diamond = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        content_diamond.set_halign(Gtk.Align.CENTER)
        content_diamond.set_valign(Gtk.Align.CENTER)
        content_diamond.append(image_diamond)
        label_diamond1 = Gtk.Label(label="SRT '1")
        label_diamond2 = Gtk.Label(label="Modelo")
        label_diamond2.set_css_classes(["tittle-label"])
        label_diamond1.set_css_classes(["tittle-label_"])
        content_diamond.append(label_diamond1)
        content_diamond.append(label_diamond2)
        diamond_model.set_child(content_diamond)  # Agregar el contenido al botón

        # Hacer que ocupe todo el espacio disponible
        circle_model.set_hexpand(True)
        star_model.set_hexpand(True)
        diamond_model.set_hexpand(True)
        circle_model.set_vexpand(True)
        star_model.set_vexpand(True)
        diamond_model.set_vexpand(True)

        # Agregar clases
        circle_model.set_css_classes(["button"])
        circle_model.get_style_context().add_class("selected")  # Seleccionado por defecto
        on_button_clicked_model(None,circle_model, star_model,diamond_model, 'Modelo 1')


        star_model.set_css_classes(["button"])
        diamond_model.set_css_classes(["button"])

        # Conectar señales de clic a los botones
        circle_model.connect("clicked", on_button_clicked_model, circle_model, star_model,diamond_model, 'Modelo 1')
        star_model.connect("clicked", on_button_clicked_model, star_model, circle_model,diamond_model,'Modelo 2')
        diamond_model.connect("clicked", on_button_clicked_model, diamond_model, circle_model,star_model,'Modelo 3')

        button_model.append(circle_model)
        button_model.append(star_model)
        button_model.append(diamond_model)


    # CONTENIDO PARA ANTERIOR Y SIGUIENTE
        back_button=  Gtk.Button()
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
        # next_button.connect("clicked", Methods(self).on_next_button_clicked, window)
        next_button.connect("clicked", on_next_button_clicked)
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


        # Aplicar estilos personalizados desde un archivo CSS
        apply_css()

        return main_box
