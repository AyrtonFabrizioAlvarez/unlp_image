import json
import PySimpleGUI as sg
import UNLPimage.src.functions.files_functions as skov
from UNLPimage.common.path import PATH_DATA_JSON
import os
import PIL.Image
import PIL.ImageTk
import PIL.ImageOps
import PIL.ImageDraw


def create_patterns_collage():
    """Funcion que crea el archivo "patterns_collage.json" con los patrones
    de diseño implementados en la creacion de collage, almacenandolo en la
    ruta "grupo19/UNLPimage/data/json_files"
    """
    pattern_collage = [
        {
            "name": "-box-2h-.png",
            "number_images": "2",
            "fit_0": "400,200",
            "fit_1": "400,200",
            "axes_0": "0,0",
            "axes_1": "0,200",
        },
        {
            "name": "-box-2v-.png",
            "number_images": "2",
            "fit_0": "200,400",
            "fit_1": "200,400",
            "axes_0": "0,0",
            "axes_1": "200,0",
        },
        {
            "name": "-box-2d-.png",
            "number_images": "2",
            "fit_0": "400,100",
            "fit_1": "400,300",
            "axes_0": "0,0",
            "axes_1": "0,100",
        },
        {
            "name": "-box-3-.png",
            "number_images": "3",
            "fit_0": "400,200",
            "fit_1": "200,200",
            "fit_2": "200,200",
            "axes_0": "0,0",
            "axes_1": "0,200",
            "axes_2": "200,200",
        },
        {
            "name": "-box-3i-.png",
            "number_images": "3",
            "fit_0": "200,200",
            "fit_1": "200,200",
            "fit_2": "400,200",
            "axes_0": "0,0",
            "axes_1": "200,0",
            "axes_2": "0,200",
        },
        {
            "name": "-box-3h-.png",
            "number_images": "3",
            "fit_0": "400,133",
            "fit_1": "400,133",
            "fit_2": "400,133",
            "axes_0": "0,0",
            "axes_1": "0,133",
            "axes_2": "0,266",
        },
        {
            "name": "-box-4-.png",
            "number_images": "4",
            "fit_0": "200,200",
            "fit_1": "200,200",
            "fit_2": "200,200",
            "fit_3": "200,200",
            "axes_0": "0,0",
            "axes_1": "0,200",
            "axes_2": "200,0",
            "axes_3": "200,200",
        },
        {
            "name": "-box-6-.png",
            "number_images": "6",
            "fit_0": "200,133",
            "fit_1": "200,133",
            "fit_2": "200,133",
            "fit_3": "200,133",
            "fit_4": "200,133",
            "fit_5": "200,133",
            "axes_0": "0,0",
            "axes_1": "200,0",
            "axes_2": "0,133",
            "axes_3": "200,133",
            "axes_4": "0,266",
            "axes_5": "200,266",
        },
    ]
    route = os.path.join(PATH_DATA_JSON, "patterns_collage.json")
    try:
        with open(route, "w") as file:
            json.dump(pattern_collage, file)
    except MemoryError:
        sg.popup(
            """ERROR: excepcion MemoryError, no se pudo crear el
           archivo json de Patrones de diseno del collage"""
        )
    except PermissionError:
        sg.popup(
            """ERROR: excepcion PermissionError, no se pudo crear el
            archivo json de Patrones de diseno del collage"""
        )


def layout_collage(pattern):
    """Funcion que recibe el nombre de la patron de diseño
    que usaremos para implementar el collage, en caso de no poder abrir
    el archivo (en skov.open_json("patterns_collage.json")) por que no
    existe, lo crea y vuelve a invocar la funcion para leerlo

    Args:
        pattern (_string_): Es el nombre de la imagen de patron seleccionada
        en la ventana "Seleccionar Patron"

    Returns:
        _dict_: devuelve el diccionario con la info del patron de diseño
        de la imagen collage
    """
    try:
        list_dict = list(skov.open_json_dict("patterns_collage.json"))
        filtered_dict = next(
            filter(lambda item: item.get("name") == pattern, list_dict), None
        )
        return filtered_dict
    except FileNotFoundError:
        create_patterns_collage()
        return layout_collage(pattern)


def open_csv():
    """Abre el archivo csv "metadata.csv" para filtrar los nombres de
    las imagenes previamente etiquetadas.

    Returns:
        _list_: Lista que contiene los nombres de las imagenes previamente
        etiquetadas
    """
    try:
        data_csv = skov.open_csv("metadata.csv")
        list_relative_path = [element["relative_path"] for element in data_csv]
        list_names_images = [os.path.basename(path) for path in list_relative_path]
        return list_names_images
    except FileNotFoundError:
        skov.try_open_csv(
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
        return open_csv()


def string_to_tupple(modification_string):
    """funcion que convierte un string a una tupla de numeros
    usados para coordenadas o modificacion de las imagenes

    Args:
        modification_string (_string_): recibe un string con formato par de
        numeros ej: "0,0"

    Returns:
        _tuple_: tupla de numeros usados para modificar o pegar imagenes
    """
    return tuple(map(int, modification_string.split(",")))


def new_pil_image(window):
    """_Funcion que genera una nueva ventana pillow vacia,
    donde posicionaremos nuestras imagenes del collage, actualiza
    la ventana sg.Image  en el layout(components_left) _

    Args:
        window (_PySimpleGUI.PySimpleGUI.Window_): Layout de collage.py

    Returns:
        _PIL.Image.Image_: retorna una imagen modificable usada en collage
    """
    IMAGE_SIZE = 400, 400
    new_image = PIL.Image.new("RGB", IMAGE_SIZE, color="black")
    collage = PIL.ImageTk.PhotoImage(new_image)
    window["-COLLAGE-"].update(data=collage)
    return new_image


def draw_title_on_image(collage, title):
    """Funcion que dibuja sobre la image un texto recibido como
    parametro ingesado por el usuario.

    Args:
        collage (_PIL.Image.Image_): recibe una imagen editable la
        cual sera usada para pegar sobre ella un texto.
        title (_string_): Titulo de la imagen, ingresado en sg.Imput

    Returns:
        _PIL.Image.Image_: devuelve una imagen modificada con texto embebido
    """
    collage_copy = collage.copy()
    draw = PIL.ImageDraw.Draw(collage_copy)
    draw.text((10, 382), title, fill="white")
    return collage_copy


def show_image(window, values, dict_pattern, images_path):
    """Funcion que modifica una imagen principal pegando fotos sobre ellas,
    estas fotos se reciben de metadata.csv, en la cual filtramos el nombre
    de ellas.

    Args:
        window (_PySimpleGUI.PySimpleGUI.Window_): Layout de collage.py
        values (_dict_): diccionario que contiene eventos y valores del
        la ventana.
        dict_pattern (_dict_): diccionario que contiene la info sobre cantidad
        de imagenes a mostrar, los formatos de cada imagen para modificar sus
        medidas y las coordenadas donde seran pegadas las imagenes
        images_path (_string_): Es la ruta relativa que uniremos al nombre
        de las imagenes para poder generar una ruta para cargar la imagen.

    Returns:
        collage  _PIL.Image.Image_ : imagen modificable
        names_list _list_: lista de nombres de imagenes usadas en el collage
        title: Titulo ingresado en el evento sg.Imput
    """
    collage = new_pil_image(window)
    title = values["-TITLE-"].strip()
    names_list = []
    for i in range(int(dict_pattern["number_images"])):
        if values[f"-IMAGE-{i}-"] != "":
            route_image = os.path.join(images_path, values[f"-IMAGE-{i}-"])
            try:
                image = PIL.Image.open(route_image)
                dimension_fit = string_to_tupple(dict_pattern[f"fit_{i}"])
                image = PIL.ImageOps.fit(image, dimension_fit)
                cardinal_paste = string_to_tupple(dict_pattern[f"axes_{i}"])
                collage.paste(image, cardinal_paste)
                names_list.append(values[f"-IMAGE-{i}-"])
            except FileNotFoundError:
                sg.popup_error("Imagen no encontrada")
    if title != "":
        collage = draw_title_on_image(collage, title)
    collage_copy = collage.copy()
    collage_copy = PIL.ImageTk.PhotoImage(collage_copy)
    window["-COLLAGE-"].update(data=collage_copy)
    return collage, names_list, title
