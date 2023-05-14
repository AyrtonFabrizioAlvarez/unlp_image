import PySimpleGUI as sg
from UNLPimage.common.const import WINDOW_FULL_SIZE, FONT_BODY, THEME
from UNLPimage.common.path import PATH_BACK_ICO


def collage():
    """ "Genera el layout de pestaña collage"""
    layout = [
        [
            sg.Text(
                "ACA VA LA EDICION DE IMAGENES DE COLLAGE",
                font=FONT_BODY,
                pad=((0, 0), (150, 0)),
            )
        ],
        [
            sg.Push(),
            sg.Image(
                source=PATH_BACK_ICO,
                subsample=2,
                enable_events=True,
                key="-RETURN-",
                pad=((0, 0), (450, 0)),
            ),
        ],
    ]
    return sg.Window(
        "UNLPimage - Editar Collage",
        layout,
        element_justification="c",
        size=WINDOW_FULL_SIZE,
        finalize=True,
        enable_close_attempted_event=True,
    )


def run():  # en caso de uso de parametros pasarlo al run
    sg.theme(THEME)
    collage_window = collage()

    while True:
        event, values = collage_window.read()
        if event == sg.WIN_CLOSE_ATTEMPTED_EVENT:
            confirm = sg.popup_yes_no("¿Está seguro que desea salir?")
            if confirm == "Yes":
                exit()
        if event == "-RETURN-":
            break
    collage_window.close()
