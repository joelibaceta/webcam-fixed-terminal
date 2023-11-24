from PIL import Image

import numpy as np

import os
import pyautogui
import Quartz
import time
import cv2

TERMINAL_COLUMN_WIDTH_CONSTANT = 9.028871391076116
TERMINAL_ROW_HEIGHT_CONSTANT = 17.142857142857142


def get_screen_size() -> tuple[int, int]:
    """
    Obtiene el tamaño de la pantalla.

    Returns:
        tuple: Ancho y alto de la pantalla.
    """
    return pyautogui.size()


def get_frame_size(cap: cv2.VideoCapture) -> tuple[int, int]:
    """
    Obtiene el tamaño del frame capturado por la webcam.

    Args:
        cap (cv2.VideoCapture): Objeto de captura de video.

    Returns:
        tuple: Ancho y alto del frame.
    """
    return int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(
        cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    )


def get_terminal_size(window_number) -> tuple[int, int, int, int, int, int]:
    """
    Obtiene el tamaño de la ventana de la terminal.

    Args:
        window_number (int): Número de la ventana de la terminal.

    Returns:
        tuple: Coordenadas x, y, ancho, alto, columnas y filas de la terminal.
    """
    window_list = Quartz.CGWindowListCopyWindowInfo(
        Quartz.kCGWindowListOptionOnScreenOnly, Quartz.kCGNullWindowID
    )
    for window_info in window_list:
        if (
            window_info["kCGWindowNumber"] == window_number
        ):  # Busca la ventana de la terminal
            terminal_window = window_info
            break

    x = int(terminal_window["kCGWindowBounds"]["X"])
    y = int(terminal_window["kCGWindowBounds"]["Y"])

    terminal_columns, terminal_rows = os.get_terminal_size()

    width = int(terminal_columns * TERMINAL_COLUMN_WIDTH_CONSTANT)
    height = int(terminal_rows * TERMINAL_ROW_HEIGHT_CONSTANT)

    return x, y, width, height, terminal_columns, terminal_rows


def resize_frame(frame, frame_width, frame_height) -> np.ndarray:
    """
    Redimensiona el frame para que se ajuste a la pantalla.

    Args:
        frame (np.ndarray): Frame capturado por la webcam.
        frame_width (int): Ancho del frame.
        frame_height (int): Alto del frame.

    Returns:
        np.ndarray: Frame redimensionado.
    """
    screen_width, screen_height = get_screen_size()

    if frame_height > screen_height:
        adjusted_width = int(screen_height / frame_height * frame_width)
        adjusted_height = screen_height
    else:
        adjusted_width = int(screen_width)
        adjusted_height = int(screen_width / frame_width * frame_height)

    return cv2.resize(frame, (adjusted_width, adjusted_height))


def prepare_image(frame: np.ndarray) -> Image.Image:
    """
    Prepara la imagen para la conversión a ASCII Art.

    Args:
        frame (np.ndarray): Frame capturado por la webcam.

    Returns:
        Image.Image: Imagen preparada para la conversión a ASCII Art.
    """
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    normalized_frame = cv2.normalize(gray_frame, None, 0, 255, cv2.NORM_MINMAX)
    return Image.fromarray(normalized_frame.astype(np.uint8))


def lazy_print(ascii_art: str):
    """
    Imprime el ASCII Art en la terminal con un pequeño retraso entre líneas.

    Args:
        ascii_art (str): ASCII Art a imprimir.
    """
    lines = ascii_art.split("\n")
    for line in lines:
        print(line, end="\r\n")
    time.sleep(0.1)
