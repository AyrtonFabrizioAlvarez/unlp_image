import PySimpleGUI as sg

# CONSTANTES
from UNLPimage.common.const import WINDOW_SIZE, THEME, FONT_BODY, FONT_TITLE
from UNLPimage.common.path import PATH_BACK_ICO, PATH_IMAGE_AVATAR

# FUNCIONES PROPIAS, PARA UNIFICAR Y NO REPETIR CODIGO EDIT USA
# VARIAS FUNCIONES DE NEW_PROFILE_FUNCTIONS (NEW_FUNCTIONS)
import UNLPimage.src.edit_profile.edit_profile_functions as edit_functions
import UNLPimage.src.new_profile.new_profile_functions as new_functions


def edit_profile_window():
    """Esta funcion retorna el alayout de la ventana edit_profile"""
    sg.set_options(font=FONT_BODY)
    sg.theme(THEME)
    components_left = [
        [sg.Text("Editar Perfil", font=FONT_TITLE)],
        [sg.Text("Nick o Alias", font=FONT_BODY, pad=((10, 10), (10, 10)))],
        [
            sg.Input(
                key="-NICK-",
                font=FONT_BODY,
                size=(35, 2),
                readonly=True,
                pad=((10, 10), (8, 8)),
            )
        ],
        [sg.Text("Nombre", font=FONT_BODY, pad=((10, 10), (10, 10)))],
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
                key="-EXIT-",
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
                key="SELECCIONAR AVATAR EDIT",
                pad=((140, 0), (45, 0)),
                initial_folder=PATH_IMAGE_AVATAR,
            ),
        ],
        [
            sg.Push(),
            sg.Button(
                "Guardar", key="GUARDAR EDIT", border_width=0,
                pad=((350, 0), (40, 0))
            ),
        ],
    ]
    layout = [
        [
            sg.Column(components_left),
            sg.Column(components_right),
        ]
    ]
    return sg.Window(
        "UNLPimage - Editar Perfil",
        layout,
        size=WINDOW_SIZE,
        finalize=True,
        enable_close_attempted_event=True,
    )


def run(active_user):
    """Esta funcion contiene la logica de la ventana edit_profile"""
    window = edit_profile_window()
    edit_functions.get_active_user_data(window, active_user.lower())
    initial_user = new_functions.get_user(window["-NICK-"].get())

    while True:
        event, values = window.read()
        match event:
            case "-EXIT-":
                # NO SE CAMBIA NADA DEL ARCHIVO Y RETORNO EL USUARIO INICIAL
                window.Hide()
                return initial_user
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
            case "GUARDAR EDIT":
                # EDITO EL USUARIO INGRESADO
                user, ok = edit_functions.edit_user(window, values,
                                                    initial_user)
                if ok:
                    window.Hide()
                    if initial_user.values() != user.values():
                        # SI SE REALIZARON MODIFICACIONES DEVUELVO ESE
                        # USUARIO MODIFICADO
                        return user
                    else:
                        # SI NO SE REALIZARON MODIFICACIONES DEVUELVO EL
                        # USUARIO ORIGINAL
                        return initial_user
                else:
                    sg.popup("Verifique los datos ingresados")
            case "-AVATAR URL-":
                # ACTUALIZO AVATAR
                img_path = window["-AVATAR URL-"].get()
                path = new_functions.user_img(window, img_path)
                window["AVATAR"].update(source=path, subsample=4)
    window.close()
