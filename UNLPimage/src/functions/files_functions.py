import PySimpleGUI as sg
import UNLPimage.src.classes.log as fran
from UNLPimage.common.path import (
    PATH_DATA_CSV,
    PATH_DATA_JSON,
    PATH_JSON,
    PATH_DEFAULT_COLLAGE,
    PATH_DEFAULT_IMAGES,
    PATH_DEFAULT_MEMES,
    PATH_CSV,
)
import os
import json
import csv


def open_csv(csv_name) -> list:
    """Funcion que abre un archivo csv que recibe como parametro
    el nombre, en caso de querer abrirlo y no encontrarlo levanta
    el error para ser tratado desde la funcion que lo
    invoca.

    Args:
        csv_name (_string_): Nombre del archivo csv que queremos abrir

    Returns:
        list: retorna un iterable con la info del csv.
    """
    route = PATH_DATA_CSV
    route_file = os.path.join(route, csv_name)
    try:
        with open(route_file, "r", encoding="utf8") as file:
            csv_reader = list(csv.DictReader(file, delimiter=","))
        return csv_reader
    except FileNotFoundError:
        raise


def open_csv_list(csv_name) -> list:
    """Funcion que abre un archivo csv que recibe como parametro
    el nombre, en caso de querer abrirlo y no encontrarlo levanta
    el error para ser tratado desde la funcion que lo
    invoca.

    Args:
        csv_name (_string_): Nombre del archivo csv que queremos abrir

    Returns:
        list: retorna un iterable con la info del csv.
    """
    route = PATH_DATA_CSV
    route_file = os.path.join(route, csv_name)
    try:
        with open(route_file, "r", encoding="utf8") as file:
            csv_reader = list(csv.reader(file, delimiter=","))
        return csv_reader
    except FileNotFoundError:
        raise


def open_json_dict(json_name: str) -> dict | list[dict]:
    """Esta funcion recibe un nombre del json a abrir y retorna sus contenidos
    tal y como lo encuentra.

    Args:
        json_name (str): nombre del json.

    Returns:
        dict | list[dict]: diccionario con sus contenidos o lista de
        diccionarios.

    Raises:
        FileNotFoundError: Si el archivo no esta entonces va a levantar la
        excepcion de que el archivo no esta.

    """
    route = PATH_DATA_JSON
    route_file = os.path.join(route, json_name)
    data = []
    try:
        with open(route_file, "r", encoding="utf8") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        raise


def get_user(nick: str) -> dict:
    """Esta funcion recibe un string que representa la clave 'nick'
    y si lo encuentra retorna un diccionario que representa al usuario
    """
    ruta = PATH_DATA_JSON
    rutaArchivo = os.path.join(ruta, "usuarios.json")

    with open(rutaArchivo, "r", encoding="utf8") as archivo:
        data = list(json.load(archivo))

    user = list(filter((lambda x: x["nick"] == nick), data))

    return user[0]


def open_record() -> dict:
    """Esta funcion intenta abrir el json con las rutas a los directorios
    de imagenes, collage y memes, si no puede abrirlo intenta crearlo,
    de no poder crearlo lo informa.

    Returns:
        dict: diccionario con las rutas del archivo.
    """

    def default_paths():
        """Esta función simplemente esta para no tener que repetir el
        codigo para crear los caminos por default.

        Returns:
            dict: un diccionario con el usuario actual, y los caminos default
            relativos.
        """
        data = {
            "-NICK-": f"{fran.Log.nick}",
            "-IMAGEPATH-": os.path.relpath(PATH_DEFAULT_IMAGES).replace('\\', '/'),
            "-COLLAGEPATH-": os.path.relpath(PATH_DEFAULT_COLLAGE).replace('\\', '/'),
            "-MEMEPATH-": os.path.relpath(PATH_DEFAULT_MEMES).replace('\\', '/'),
        }
        return data

    try:
        data = open_json_dict(PATH_JSON)
    except FileNotFoundError:
        dict_paths = default_paths()
        try:
            with open(PATH_JSON, "w", encoding="utf-8") as file:
                file.write(json.dumps([dict_paths], indent=4))
        except MemoryError:
            sg.popup(
                "ERROR: excepcion MemoryError, no se pudo crear el archivo json de rutas"
            )
        except PermissionError:
            sg.popup(
                "ERROR: excepcion PermissionError, no se pudo crear el archivo json de rutas"
            )
    else:
        dict_paths = list(filter(lambda x: x["-NICK-"] == fran.Log.nick, data))
        if len(dict_paths) == 0:
            dict_paths = default_paths()
            data.append(dict_paths)
            with open(PATH_JSON, "w+", encoding="utf-8") as file:
                file.write(json.dumps(data, indent=4))
        else:
            dict_paths = dict_paths[0]
    return dict_paths


def try_open_csv(header: list[str], file_name="metadata.csv"):
    """Esta funcion intenta abrir el csv, si no existe creamos el archivo y
    le escribimos la cabecera con las
    las columnas que necesitamos.

    Args:
        header (list[str]): lista con lo que va a ir en la cabecera.
        file_name (str, optional): el nombre del archivo a abrir. Defaults to "metadata.csv".
    """
    try:
        tags = open(os.path.join(PATH_CSV, file_name), "r", encoding="utf-8")
        tags.close()
    except FileNotFoundError:
        try:
            with open(os.path.join(PATH_CSV, file_name), "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(header)
        except MemoryError:
            sg.popup(f"ERROR: excepcion MemoryError, no se pudo crear el {file_name}")
        except PermissionError:
            sg.popup(
                f"ERROR: excepcion PermissionError, no se pudo crear el {file_name}"
            )


def election(copy, title, path):
    """funcion que graba una imagen en la carpeta previamente seleccionada
    en configuracion.

    Args:
        copy (_PIL.Image.Image_): imagen pillow que se grabara en memoria.
        title (_str_): Titulo con el que se almacenara la imagen.
        save_path (_str_): ruta relativa donde se almacenara la imagen
    """
    layout = [
        [sg.Text("Formato de la imagen?")],
        [
            sg.Button(".jpg", key="-JPG-", pad=((40, 10), (10, 10))),
            sg.Button(".png", key="-PNG-", pad=((10, 10), (10, 10))),
        ],
    ]
    extension = ""
    window = sg.Window("", layout)
    event, _ = window.read()
    while True:
        match event:
            case "-JPG-":
                extension = ".jpg"
                break
            case "-PNG-":
                extension = ".png"
                break
            case _:
                break
    window.close()
    if (event == "-JPG-") or (event == "-PNG-"):
        save_image(copy, title, path, extension)
    return extension


def save_image(copy, title, path, extension):
    """Funcion que Guarda una imagen en formato png o jpg.

    Args:
        copy (_img_): esla imagen que deseamos guardar
        title (_str_): es el titulo de la imagen
        path (_str_): ruta relativa usada para guardar la imagen
        format (_str_): str que indica un formato ".jpg" ".png"
    """
    if title == "":
        title = "default"
    route = os.path.join(path, title + extension)
    if extension == ".png":
        copy.convert(mode="RGBA").save(route)
    else:
        copy.convert(mode="RGB").save(route)
