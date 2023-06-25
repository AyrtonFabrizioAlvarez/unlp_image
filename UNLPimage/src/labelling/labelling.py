import os

import PySimpleGUI as sg

from UNLPimage.common.const import WINDOW_FULL_SIZE, FONT_BODY
from UNLPimage.common.const import THEME, FONT_TITLE
from UNLPimage.common.path import PATH_BACK_ICO
from UNLPimage.src.labelling.labelling_functions import (
    show_image,
    update_csv,
)
from UNLPimage.src.functions.files_functions import try_open_csv, open_record


def run(current_user: str):
    """Conseguimos el camino a la carpeta de imagenes, y filtramos
    de todos los archivos encontrados dentro para solo dejar
    los nombres de los archivos imagenes en un lista, que luego
    mostramos en el listbox.

    Args:
        current_user (str): Un string con el alias del usuario actual 
        que entro al etiquetado.
    """    
    sg.set_options(font=FONT_BODY)
    sg.theme(THEME)
    try_open_csv(
        [
            "current_user",
            "relative_path",
            "resolution",
            "format",
            "last_update",
            "tags",
            "size_mb",
            "description",
        ]
    )

    images_directories = open_record()["-IMAGEPATH-"]
    valid_extensions = [".jpg", ".jpeg", ".png", ".gif"]
    img_names = [
        file
        for file in os.listdir(images_directories)
        if (os.path.splitext(file)[1] in valid_extensions)
    ]

    elements_row_1 = [
        [
            sg.Text("Etiquetar imagenes", font=FONT_TITLE),
            sg.P(),
            sg.Image(
                source=PATH_BACK_ICO, subsample=2, key="-BACK-", enable_events=True
            ),
        ],
        [
            sg.Text("Dirección donde estan los archivos:"),
            sg.Input(images_directories, disabled=True),
        ],
    ]
    elements_column_1 = [
        [
            sg.Listbox(
                values=img_names, size=(40, 25), key="-FILELIST-", enable_events=True
            )
        ],
    ]
    elements_column_2 = [
        [sg.Image(key="-IMAGE-", size=(400, 400))],
        [sg.T(key="-IMGNAME-"), sg.T(key="-IMGSIZE-"), sg.T(key="-IMGMB-")],
        [sg.P(), sg.Text("Modificar tags (separe por comas):"), sg.I(key="-LABELS-")],
        [sg.P(), sg.Text("Modificar descripccion:"), sg.I(key="-DESCRIPTION-")],
        [sg.B("Guardar cambios", key="-SAVE-")],
    ]

    layout = [
        elements_row_1,
        [
            sg.Column(elements_column_1, element_justification="left", pad=(100, 10)),
            sg.P(),
            sg.Column(elements_column_2, element_justification="right", pad=(100, 10)),
        ],
    ]

    window = sg.Window(
        "Configuration",
        layout,
        size=(1300, 700),
        element_justification="c",
        finalize=True,
        enable_close_attempted_event=True,
    )
    while True:
        event, values = window.read()
        match event:
            case "-EXIT-" | sg.WIN_CLOSE_ATTEMPTED_EVENT:
                confirm = sg.popup_yes_no("¿Está seguro que desea salir?")
                if confirm == "Yes":
                    exit()
            case "-BACK-":
                break
            case "-FILELIST-":
                try:
                    show_image(values["-FILELIST-"][0], images_directories, window)
                except IndexError:
                    sg.popup_error(
                        "No hay ninguna imagen en este directorio para mostrar."
                    )
            case "-SAVE-":
                if (len(values["-DESCRIPTION-"]) < 255) and (
                    len(values["-LABELS-"]) < 30
                ):
                    confirm = sg.popup_yes_no("¿Confirma guardar los datos?")
                    if confirm == "Yes":
                        update_csv(values, images_directories, current_user)
                else:
                    if len(values["-DESCRIPTION-"]) > 255:
                        sg.popup_error("Descripción con más de 255 caracteres")
                    if len(values["-LABELS-"]) > 30:
                        sg.popup_error("Tags con más de 30 caracteres")
    window.close()
