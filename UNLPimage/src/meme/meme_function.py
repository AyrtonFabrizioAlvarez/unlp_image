import PySimpleGUI as sg
from UNLPimage.common.const import FONT_BODY
from UNLPimage.common.const import FONT_TITLE
from UNLPimage.common.const import THEME
from UNLPimage.common.const import WINDOW_FULL_SIZE
from UNLPimage.common.path import PATH_BACK_ICO
from UNLPimage.common.path import PATH_DATA_JSON
from UNLPimage.common.path import PATH_FONTS
import os
import json
from PIL import Image
from PIL import ImageTk
from PIL import ImageDraw
from PIL import ImageFont
import UNLPimage.src.classes.log as logs
from UNLPimage.src.functions.files_functions import election, open_json_dict


def start(memes_names):
    """ muestra la ventana de template de memes

    Args:
        memes_names (list): contiene la lista
        con el nombre de los memes con templates

    Returns:
        PySimpleGUI.PySimpleGUI.Window: 
        devuelve la ventana
    """    
    sg.theme(THEME)
    layout = [
        [
            sg.Text("Elegir meme", font=FONT_TITLE),
            sg.Push(),
            sg.Image(PATH_BACK_ICO, subsample=2, enable_events=True, key="-RETURN-"),
        ],
        [
            sg.Text("Seleccionar template", font=FONT_BODY),
            sg.Push(),
            sg.Text("Previsualizacion", font=FONT_BODY),
        ],
        [
            sg.Listbox(
                values=memes_names, size=(40, 25), enable_events=True, key="-FILE-"
            ),
            sg.Push(),
            sg.Image(key="-IMAGE-"),
        ],
        [sg.Push(), sg.Button("Editar", key="-EDITE-", font=FONT_BODY)],
    ]
    return sg.Window(
        "UNLPimage - Elegir template",
        layout,
        size=WINDOW_FULL_SIZE,
        finalize=True,
        enable_close_attempted_event=True,
    )


def take_memes():
    """ Permite abrir el archivo, si no esta lo crea con los 
    templates predefinidos y toma los nombres de los memes

    Returns:
        list: devuelve la lista de nombres de los
        memes que pueden que tienen templates
    """ 
    names = []
    try:
        meme_list = open_json_dict("memes.json")
        for elem in meme_list:
            names.append(elem["name"])
    except FileNotFoundError:
        memes_data = [
            {
                "image": "monito.png",
                "name": "mono (1 text box)",
                "text_boxes": [
                    {
                        "top_left_x": 11,
                        "top_left_y": 42,
                        "bottom_right_x": 607,
                        "bottom_right_y": 128,
                    }
                ],
            },
            {
                "image": "botoncitos.png",
                "name": "botones y persona (3 text boxes)",
                "text_boxes": [
                    {
                        "top_left_x": 45,
                        "top_left_y": 111,
                        "bottom_right_x": 251,
                        "bottom_right_y": 151,
                    },
                    {
                        "top_left_x": 266,
                        "top_left_y": 74,
                        "bottom_right_x": 410,
                        "bottom_right_y": 104,
                    },
                    {
                        "top_left_x": 66,
                        "top_left_y": 770,
                        "bottom_right_x": 514,
                        "bottom_right_y": 832,
                    },
                ],
            },
            {
                "image": "cerebrones.png",
                "name": "cerebros (4 text boxes)",
                "text_boxes": [
                    {
                        "top_left_x": 7,
                        "top_left_y": 12,
                        "bottom_right_x": 228,
                        "bottom_right_y": 174,
                    },
                    {
                        "top_left_x": 5,
                        "top_left_y": 203,
                        "bottom_right_x": 225,
                        "bottom_right_y": 362,
                    },
                    {
                        "top_left_x": 3,
                        "top_left_y": 389,
                        "bottom_right_x": 224,
                        "bottom_right_y": 552,
                    },
                    {
                        "top_left_x": 6,
                        "top_left_y": 579,
                        "bottom_right_x": 223,
                        "bottom_right_y": 744,
                    },
                ],
            },
            {
                "image": "dragones.png",
                "name": "dragones (3 text boxes)",
                "text_boxes": [
                    {
                        "top_left_x": 9,
                        "top_left_y": 315,
                        "bottom_right_x": 153,
                        "bottom_right_y": 451,
                    },
                    {
                        "top_left_x": 273,
                        "top_left_y": 281,
                        "bottom_right_x": 395,
                        "bottom_right_y": 410,
                    },
                    {
                        "top_left_x": 507,
                        "top_left_y": 323,
                        "bottom_right_x": 640,
                        "bottom_right_y": 473,
                    },
                ],
            },
            {
                "image": "pibe_campera.png",
                "name": "Persona con campera (2 text boxes)",
                "text_boxes": [
                    {
                        "top_left_x": 614,
                        "top_left_y": 10,
                        "bottom_right_x": 1076,
                        "bottom_right_y": 570,
                    },
                    {
                        "top_left_x": 614,
                        "top_left_y": 626,
                        "bottom_right_x": 1078,
                        "bottom_right_y": 1192,
                    },
                ],
            },
        ]
        route = os.path.join(PATH_DATA_JSON, "memes.json")
        with open(route, "w", encoding="utf-8") as file:
            json.dump(memes_data, file, indent=4)
        for elem in memes_data:
            names.append(elem["name"])
    return names


def search_meme(name, path):
    """ Busca la informacion del meme
        y la retorna

    Args:
        name (str): contiene el nombre
        del meme
        path (str): contiene la
        direccion de la carpeta de
        memes

    Returns:
        dict: contiene la informacion
        del meme original
    """    
    meme_list = open_json_dict("memes.json")
    meme = {}
    for elem in meme_list:
        if elem["name"] == name:
            meme = elem
    image_path = os.path.join(path, meme["image"])
    if not os.path.exists(image_path):
        meme = {}
    return meme


def update_meme(window, meme_image, path):
    """ Muestra la imagen del meme en la 
        pantalla con su resize.

    Args:
        window (PySimpleGUI.PySimpleGUI.Window):
        contiene la ventana con la que se trabaja
        meme_image (str): contiene el nombre
        del meme
        path (str): contiene la direccion donde
        se encuentra el meme

    Returns:
        PySimpleGUI.PySimpleGUI.Window:
        retorna la copia de la imagen
    """    
    image_path = os.path.join(path, meme_image)
    img = Image.open(image_path)
    resized_image = img.resize((500, 500))
    img_tk = ImageTk.PhotoImage(resized_image)
    window["-IMAGE-"].update(data=img_tk)
    return img.copy()


def start_edit(quantity, colors):
    """muestra la ventana de editar imagenes.

    Args:
        quantity (int): la cantidad de
        cajas de texto en la imagen

    Returns:
        PySimpleGUI.PySimpleGUI.Window: 
        devuelve la ventana.
    """    
    sg.theme(THEME)
    layout = [
        [
            sg.Listbox( values= colors, key='f_color', enable_events=True),
            sg.Column(
                [
                    [sg.Text("Editar meme", font=FONT_TITLE, pad=(0, 20))],
                    [sg.Text("Seleccionar fuente")],
                    [
                        sg.Listbox(
                            values=os.listdir(PATH_FONTS),
                            key="-FONTS-",
                            enable_events=True,
                            size=(45, 5),
                        )
                    ],
                    [
                        sg.Column(
                            [
                                [
                                    sg.Text(f"Texto {i+1}"),
                                    sg.Multiline(size=(37, 4), key=f"-TEXT{i+1}-"),
                                ]
                                for i in range(quantity)
                            ]
                        )
                    ],
                ],
                vertical_alignment="top",
            ),
            sg.Push(),
            sg.Column(
                [
                    [
                        sg.Push(),
                        sg.Image(
                            PATH_BACK_ICO,
                            subsample=2,
                            enable_events=True,
                            key="-RETURN-",
                            pad=(0, 20),
                        ),
                    ],
                    [sg.Image(key="-IMAGE-")],
                    [
                        sg.Push(),
                        sg.Button("actualizar", key="-UPDATE-"),
                        sg.Button("guardar", key="-SAVE-", pad=(0, 20)),
                    ],
                ],
                vertical_alignment="top",
            ),
        ]
    ]
    return sg.Window(
        "UNLPimage - Editar meme",
        layout,
        size=WINDOW_FULL_SIZE,
        finalize=True,
        enable_close_attempted_event=True,
    )


def calculate_box(top_left_x, top_left_y, bottom_right_x, bottom_right_y):
    """ calcula el tamaño de la caja de texto.

    Args:
        top_left_x (int): contiene
        una de las coordenadas
        top_left_y (int): contiene
        una de las coordenadas
        bottom_right_x (int): contiene
        una de las coordenadas
        bottom_right_y (int): contiene
        una de las coordenadas

    Returns:
        tuple: devuelve la tupla con el
        tamaño de la caja
    """    
    return (bottom_right_x - top_left_x, bottom_right_y - top_left_y)


def fits(size_box, size_text_box):
    """ revisa si entra el texto en la caja.

    Args:
        size_box (tuple): contiene el
        tamañ de la caja original
        size_text_box (tuple): contiene
        el tamaño de la caja con la
        fuente actual

    Returns:
        boolean: si entra devuelve true y si no devuelve
        false
    """    
    return size_text_box[0] <= size_box[0] and size_text_box[1] <= size_box[1]


def calculate_font_size(draw, text, path_font, box):
    """ Permite el calculo del tamaño de fuente
        apropiado para cada caja de texto.
    Args:
        draw (PIL.ImageDraw.ImageDraw): contiene
        la imagen donde se puede calcular el
        tamanio de la fuente en una caja de texto
        text (str): contiene el texto que se planea
        escribir en la caja
        path_font (str): contiene la direccion
        donde se encuentra la fuente
        box (dict): contiene las dimensiones de la
        caja de texto

    Returns:
        PIL.ImageFont.FreeTypeFont: contiene la fuente
        a utilizar para la caja de texto
    """
    size_box = calculate_box(**box)
    for size in range(100, 5, -5):
        written_font = ImageFont.truetype(path_font, size)
        text_box = draw.textbbox((0, 0), text, font=written_font)
        size_text_box = calculate_box(*text_box)
        if fits(size_box, size_text_box):
            return written_font
    return written_font


def edition_meme(window, meme_info, written_text, copy, font, color):
    """ Permite guardar los cambios hechos en el meme y a su
        vez muestra los cambios realizados en la ventana de 
        edicion.

    Args:
        window (PySimpleGUI.PySimpleGUI.Window): contiene a
        la ventana en ejecucion
        meme_info (dict): contiene la informacion del meme original
        written_text (list): Contiene los escritos hechos por el
        usuario para cada caja de texto
        copy (PIL.Image.Image): contiene una copia de la imagen
        a  editar
        font (str): contiene la direccion de la fuente a usar
    """    
    draw = ImageDraw.Draw(copy)
    for i in range(len(meme_info["text_boxes"])):
        writting_font = calculate_font_size(
            draw, written_text[i], font, meme_info["text_boxes"][i]
        )
        draw.text(
            (
                meme_info["text_boxes"][i]["top_left_x"],
                meme_info["text_boxes"][i]["top_left_y"],
            ),
            written_text[i],
            font=writting_font,
            fill=color,
        )
    resized_image = copy.resize((500, 500))
    img_tk = ImageTk.PhotoImage(resized_image)
    window["-IMAGE-"].update(data=img_tk)


def save_meme(copy, path, meme_info):
    """ Permite ingresarle un titulo al meme y guardarlo
        como .jpg o .png.

    Args:
        copy (PIL.Image.Image): Contiene la copia de la
        imagen del meme que se esta editando
        path (str): contiene la direccion donde guardar el meme
        meme_info (dict): contiene la informacion sobre el 
        meme original.
    """    
    title = sg.PopupGetText("Ingrese el titulo del meme")
    if title != None and len(title.strip()) <= 30 and len(title.strip()) > 3:
        extension = election(copy, title, path)
        if extension != "":
            logs.Log.write_log("generó meme", meme_info["image"], meme_info["name"])
    else:
        if title != None:
            sg.popup("El titulo no es valido")
