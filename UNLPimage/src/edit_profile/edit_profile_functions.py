import os
import json

from UNLPimage.common.path import PATH_IMAGE_AVATAR, PATH_DATA_JSON
import UNLPimage.src.new_profile.new_profile_functions as new_functions
from UNLPimage.src.functions.files_functions import open_json_dict


# FUNCION PARA EDITAR UN USUARIO EN EL ARCHIVO JSON
def edit_json_user(user: dict) -> None:
    """Esta funcion busca y modifica el usuario a editar
    
    Args:
        user (dict): usuario a dar de alta
    """
    path = PATH_DATA_JSON
    path_file = os.path.join(path, "usuarios.json")
    data = open_json_dict("usuarios.json")
    new_data = list(map(lambda x: edit_dict(x, user),data))
    with open(path_file, "w", encoding="utf8") as file:
        file.write(json.dumps(new_data, indent=4))

def edit_dict(dicc:dict, user:dict) -> None:
    """Esta funcion recibe un diccionario con los datos del usuario buscado.
    Al encontrarlo modifica los datos del mismo (excepto el campo nick)
    
    Args:
        dicc (dict): usuario a leer
        user (dict): usuario a comparar (buscado)
    """
    if dicc["nick"] == user["nick"]:
        dicc["name"] = user["name"]
        dicc["age"] = user["age"]
        dicc["gender"] = user["gender"]
        dicc["avatar"] = user["avatar"]
    return dicc

# FUNCION PARA VALIDAR SI SE EDITARA O NO UN USUARIO EN EL ARCHIVO JSON
def edit_user(window: object, value: dict, initial_user: dict) -> tuple[(dict, bool)]:
    """Funcion que valida si un usuario puede ser editado en usuarios.json
    de ser posible lo edita, y retorna (user, True), caso contrario no lo edita 
    y retorna (user, False)

    Args:
        window (sg.Window): objeto window de PySimpleGUI
        value (dict): diccionario con valores de eventos
        initial_user (dict): usuario inicial (al ingresar a editar)
    """
    user = new_functions.read_inputs(window, value, initial_user)
    if new_functions.valid_user(user, window):
        edit_json_user(user)
        new_functions.create_user_img(window["-AVATAR URL-"].get(), user["nick"])
        return (user, True)
    else:
        return (user, False)


# FUNCION PARA SABER SI EL CAMPO GENERO PERTENECE A LAS OPCIONES PREDETERMINADAS
def chosen_gender(gender: str) -> bool:
    """Esta funcion recibe el genero que tiene un usuario en el archivo
    'usuarios.json' si es una de las opciones del elemento combo
    ["varon cis", "varon trans", "mujer cis", "mujer trans", "no binarie", "otre"]
    retornamos true, en cualquier otro caso retornamos false
    
    Args:
        gender (str): genero a verificar
    """
    gender_list = ["varon cis", "varon trans", "mujer cis", "mujer trans", "no binarie", "otre"]
    match (gender):
        case _ if gender in gender_list:
            ok = True
        case _:
            ok = False
    return ok


# FUNCION PARA LLENAR LOS INPUTS CON LOS DATOS DEL USUARIO RECIBIDO COMO PARAMETRO
def fill_inputs(window: object, user: dict) -> None:
    """Esta funcion recibe una ventana y un usuario y
    lo rellena en los input de la pantalla editar perfil

    Args:
        window (sg.Window): objeto window de PySimpleGUI
        user (dict): usuario para rellenar
    """    
    window["-NICK-"].update(user["nick"])
    window["-NAME-"].update(user["name"])
    window["-AGE-"].update(user["age"])
    if chosen_gender(user["gender"]):
        window["-GENDER-"].update(user["gender"])
    else:
        window["-CHECKBOX-"](value=True)
        window["-GENDER INPUT-"](visible=True)
        window["-GENDER INPUT-"].update(user["gender"])
        window["-GENDER-"].update(disabled=(not window["-GENDER-"].Disabled))
    path_avatar = os.path.join(PATH_IMAGE_AVATAR, user["avatar"])
    window["-AVATAR URL-"].update(path_avatar)
    window["AVATAR"].update(source=path_avatar, subsample=4)
