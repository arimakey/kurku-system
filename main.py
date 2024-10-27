from screens.select_place import select_place # Importar la clase de la nueva ventana
class Methods:
    def __init__(self, main_window):
        self.main_window = main_window  # Mantener referencia a la ventana principal

    def on_next_button_clicked(self, button, main_window):
    # Crear una nueva ventana
        new_window = select_place()

        # Mostrar la nueva ventana
        new_window.present()

        # Cerrar la ventana principal (actual)
        # if main_window:
        #     main_window.close()
