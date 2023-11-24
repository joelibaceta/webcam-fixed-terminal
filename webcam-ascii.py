from img2ascii import image_to_ascii_art
from colorama import init, Fore
from utils import (
    get_frame_size,
    get_terminal_size,
    resize_frame,
    prepare_image,
    lazy_print,
)

import sys
import cv2


class WebcamAscii:
    """
    Clase que convierte la entrada de una webcam en ASCII Art
    y la muestra en multiples ventanas de la terminal
    """

    # Inicializa colorama para imprimir colores en la terminal
    init(autoreset=True)

    def __init__(self, window_number):
        self.window_number = window_number

    def open_webcam(self):
        """
        Abre la conexión con la webcam y verifica si la conexión fue exitosa.

        Returns:
            Objeto cv2.VideoCapture si la conexión fue exitosa.
        """

        # Abre la conexión con la webcam
        cap = cv2.VideoCapture(0)
        # Verifica si la conexión fue exitosa
        exit() if not cap.isOpened() else print(
            Fore.GREEN + "Conexión exitosa con la cámara."
        )
        return cap

    def run(self):
        """
        Inicia la captura de la webcam y la muestra en la terminal.
        """

        cap = self.open_webcam()
        frame_width, frame_height = get_frame_size(cap)
        (
            terminal_x,
            terminal_y,
            terminal_width,
            terminal_height,
            terminal_columns,
            _,
        ) = get_terminal_size(window_number)

        while True:
            ret, frame = cap.read()

            if not ret:  # Verifica si la captura fue exitosa
                print(Fore.RED + "Error: No se puede leer el frame.")
                break

            resized_frame = resize_frame(frame, frame_width, frame_height)
            cutted_frame = resized_frame[
                terminal_y : terminal_y + terminal_height,
                terminal_x : terminal_x + terminal_width,
            ]
            pre_processed_image = prepare_image(cutted_frame)
            ascii_art = image_to_ascii_art(pre_processed_image, rows=terminal_columns)
            lazy_print(ascii_art)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()

    # Libera la cámara y cierra la ventana
    cv2.destroyAllWindows()


if __name__ == "__main__":
    window_number = int(sys.argv[1])  # Obtiene el número de la ventana de la terminal
    cam = WebcamAscii(window_number)
    cam.run()
