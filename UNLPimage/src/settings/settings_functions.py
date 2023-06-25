import json
import PySimpleGUI as sg
from UNLPimage.common.path import PATH_JSON
from UNLPimage.src.functions.files_functions import open_json_dict
from UNLPimage.src.classes.log import Log
import os


def save_config(values:dict):
    """ 
    Crea o sobreescribe el archivo json donde estarian los distintos
    directorios donde se guardan las imagenes, collages o memes,
    y guarda lo que esta en los distintos inputs en el mismo.
    Ya que la informacion anterior esta cargada en los inputs, no se pierde.
    Si no hay espacio en memoria genera un ventana que informa del error.

    Args:
        values (dict): Datos dados por el PySimpleGUI.
    """
    def modify_dict(dic: dict, values:dict):
        if dic["-NICK-"] == Log.nick:
            dic["-IMAGEPATH-"] = os.path.relpath(values["-IMAGEPATH-"]).replace('\\', '/')
            dic["-COLLAGEPATH-"] = os.path.relpath(values["-COLLAGEPATH-"]).replace('\\', '/')
            dic["-MEMEPATH-"] = os.path.relpath(values["-MEMEPATH-"]).replace('\\', '/')
        return dic

    try:
        data = open_json_dict(PATH_JSON)
    except Exception as e:
        sg.popup_error(f"ERROR: {e}")
    else:
        data = list(map(lambda x: modify_dict(x, values), data))
        try:
            with open(PATH_JSON, "w", encoding="utf8") as file:
                file.write(json.dumps(data, indent=4))
        except FileNotFoundError:
            sg.popup_error("ERROR: FileNotFound")


def reset(paths: dict, window: object):
    """Esta funcion resetea los inputs así si le erramos al elegir
    se pone como estuvo al entrar a la ventana.
    Args:
        paths (dict): Diccionario con los caminos a los repositorios
        window (object): Ventana actual de configuracion
    """
    window["-IMAGEPATH-"].update(paths.get("-IMAGEPATH-", ""))
    window["-COLLAGEPATH-"].update(paths.get("-COLLAGEPATH-", ""))
    window["-MEMEPATH-"].update(paths.get("-MEMEPATH-", ""))
