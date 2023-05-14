import os
import PySimpleGUI as sg

# CONSTANTES
from UNLPimage.common.const import (
    WINDOW_SIZE,
    THEME,
    FONT_BODY,
    FONT_TITLE,
    AVATAR_DEFAULT,
)
from UNLPimage.common.path import PATH_IMAGE_AVATAR, PATH_BACK_ICO

# FUNCIONES PROPIAS
import UNLPimage.src.new_profile.new_profile_functions as new_functions
import UNLPimage.src.main.main as main_window


def new_profile_window():
    """Esta funcion retorna el alayout de la ventana new_profile"""
    sg.set_options(font=FONT_BODY)
    sg.theme(THEME)
    components_left = [
        [sg.Text("Nuevo Perfil", font=FONT_TITLE)],
        [sg.Text("Nick o Alias", font=FONT_BODY, pad=((10, 10), (10, 10)))],
        [
            sg.Input(
                key="-NICK-",
                font=FONT_BODY,
                size=(35, 2),
                enable_events=True,
                pad=((10, 10), (8, 8)),
            )
        ],
        [
            sg.Text("Nombre", font=FONT_BODY, pad=((10, 10), (10, 10))),
        ],
        [
            sg.Input(
                key="-NAME-",
                font=FONT_BODY,
                size=(35, 2),
                enable_events=True,
                pad=((10, 10), (8, 8)),
            )
        ],
        [sg.Text("Edad", font=FONT_BODY, pad=((10, 10), (10, 10)))],
        [
            sg.Input(
                key="-AGE-",
                font=FONT_BODY,
                size=(35, 2),
                enable_events=True,
                pad=((10, 10), (8, 8)),
            )
        ],
        [sg.Text("Genero Autopercibido", font=FONT_BODY, pad=((10, 10),
                                                              (8, 8)))],
        [
            sg.Combo(
                ("Masculino", "Femenino", "No Binario"),
                key="-GENDER-",
                font=FONT_BODY,
                auto_size_text=True,
                disabled=False,
                readonly=True,
                pad=((10, 10), (8, 8)),
            )
        ],
        [
            sg.Checkbox(
                "Otro",
                font=FONT_BODY,
                key="-CHECKBOX-",
                enable_events=True,
                pad=((10, 10), (8, 8)),
            )
        ],
        [
            sg.Input(
                "Complete el Genero",
                font=FONT_BODY,
                key="-GENDER INPUT-",
                size=(35, 2),
                visible=False,
                pad=((10, 10), (8, 8)),
            )
        ],
    ]
    components_right = [
        [
            sg.Image(
                source=PATH_BACK_ICO,
                subsample=2,
                key="IR MENU INICIO",
                enable_events=True,
                pad=((380, 0), (0, 0)),
            )
        ],
        [sg.Image(key="AVATAR", pad=((90, 0), (25, 0)))],
        [
            sg.Input(
                key="-AVATAR URL-", font=FONT_BODY, visible=False,
                enable_events=True
            ),
            sg.FileBrowse(
                "Seleccionar Avatar",
                key="SELECCIONAR AVATAR",
                pad=((140, 0), (45, 0)),
                initial_folder=PATH_IMAGE_AVATAR,
            ),
        ],
        [sg.Button("Guardar", key="-SAVE-", border_width=0, pad=((350, 0),
                                                                 (40, 0)))],
    ]
    layout = [
        [
            sg.Column(components_left),
            sg.Column(components_right),
        ]
    ]
    return sg.Window(
        "UNLPimage - Nuevo Perfil",
        layout,
        size=WINDOW_SIZE,
        finalize=True,
        enable_close_attempted_event=True,
    )


def run():
    """Esta funcion contiene la logica de la ventana new_profile"""
    window = new_profile_window()
    default_img = os.path.join(PATH_IMAGE_AVATAR, AVATAR_DEFAULT)
    new_functions.user_img(window, default_img)
    window["AVATAR"].update(source=default_img, subsample=4)
    window["-AVATAR URL-"].update(default_img)

    while True:
        event, values = window.read()

        match event:
            case "IR MENU INICIO":
                # NO SE GENERA EL USUARIO Y SE VUELVE A LA PANTALLA DE INICIO
                new_functions.delete_img_before_back(window)
                break
            case sg.WIN_CLOSE_ATTEMPTED_EVENT:
                # PIDO CONFIRMACION PARA CERRAR LA VENTANA
                confirm = sg.popup_yes_no("¿Está seguro que desea salir?")
                if confirm == "Yes":
                    exit()
            case "-NICK-":
                # VERIFICO ESTADO DE INPUTS PARA "LIMPIARLOS"
                new_functions.clear_inputs(window)
            case "-NAME-":
                # VERIFICO ESTADO DE INPUTS PARA "LIMPIARLOS"
                new_functions.clear_inputs(window)
            case "-AGE-":
                # VERIFICO ESTADO DE INPUTS PARA "LIMPIARLOS"
                new_functions.clear_inputs(window)
            case "-CHECKBOX-":
                # VERIFICO SI EL CHECKBOX ESTA PRESIONADO Y LO DEJO EN SU
                # VALOR INVERSO
                window["-GENDER INPUT-"].update(
                    visible=(not window["-GENDER INPUT-"].visible)
                )
                window["-GENDER-"].update(disabled=(
                    not window["-GENDER-"].Disabled))
            case "-SAVE-":
                # CARGO EL NUEVO USUARIO INGRESADO
                ok = new_functions.new_user(window, values)
                if ok:
                    # SI SE DA EL ALTA CORRECTAMENTE RETORNO EL NUEVO USUARIO
                    user = new_functions.get_user(
                        window["-NICK-"].get().lower().replace(" ", "")
                    )
                    window.Hide()
                    main_window.run(user)
                    break
                else:
                    sg.popup("Verifique los datos ingresados")
            case "-AVATAR URL-":
                # ACTUALIZO AVATAR
                img_path = window["-AVATAR URL-"].get()
                path = new_functions.user_img(window, img_path)
                window["AVATAR"].update(path, subsample=4)
    window.close()
