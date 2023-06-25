import csv
import os
from datetime import datetime
import PySimpleGUI as sg
from PIL import Image, ImageTk, UnidentifiedImageError
from UNLPimage.common.path import PATH_CSV
from UNLPimage.src.classes.log import Log
from UNLPimage.src.functions.files_functions import open_csv_list
from UNLPimage.src.functions.files_functions import open_csv


def error_window(text: str):
    """    Crea una ventana aparte la cual te muestra un texto de error,
    se usa en vez de un popup porque permite más customizacion.

    Args:
        text (str): Un string que contiene el mensaje de error
    que queremos mostrar.
    """
    error_layout = [
        [sg.Text(text, text_color="Red")],
        [sg.Button("OK", button_color="Red", size=(6, 1))],
    ]
    window = sg.Window("ERROR", error_layout, finalize=True, element_justification="c")
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "OK":
            break
    window.close()


def edit_img_csv(data: dict):
    """    Recibe la informacion a escribir en el csv,
    abrimos el csv (que sabemos que existe porque se creo al
    entrar en la pantalla),

    Args:
        data (dict): Un diccionario que contiene la información
    a escribir en el csv.
    """
    try:
        csv_info = open_csv_list("metadata.csv")
    except FileNotFoundError:
        sg.popup_error(
            """El archivo de metadata no se pudo crear con anterioridad, 
            no podemos guardar los datos."""
        )
    else:
        with open(
            os.path.join(PATH_CSV, "metadata.csv"), "w", newline="", encoding="utf-8"
        ) as file:
            writer = csv.writer(file)
            found = False
            for line in csv_info:
                if data["relative_path"] in line:
                    writer.writerow(
                        [
                            data["current_user"],
                            data["relative_path"],
                            data["resolution"],
                            data["format"],
                            data["last_update"],
                            data["tags"],
                            data["size_mb"],
                            data["description"],
                        ]
                    )
                    found = True
                    Log.write_log("Modificación a imagen previamente clasificada")
                else:
                    writer.writerow(line)
            if not found:
                writer.writerow(
                    [
                        data["current_user"],
                        data["relative_path"],
                        data["resolution"],
                        data["format"],
                        data["last_update"],
                        data["tags"],
                        data["size_mb"],
                        data["description"],
                    ]
                )
                Log.write_log("Nueva imagen clasificada")


def show_image(name: str, images_directories: str, window: object):
    """Esta se producira cada vez que se clickee una imagen en el
    filelist, entonces tomamos su nombre,
    la unimos con el camino hacia el respositorio de imagenes elegido
    y con ello la abrimos y actualizamos el objeto
    imagen, además mostramos los metadatos.

    Args:
        name (str): nombre del archivo.
        images_directories (str): un string con el camino al
        repositorio de imagenes.
        window (object): La ventana actual.
    """    """"""
    image_path = os.path.abspath(os.path.join(images_directories, name))
    try:
        img = Image.open(image_path)
    except UnidentifiedImageError:
        error_window(
            """La imagen que desea abrir esta corrupta o se saco del
              directorio en ejecución"""
        )
    else:
        resized_image = img.resize((400, 400))
        img_tk = ImageTk.PhotoImage(resized_image)
        try:
            # csv_info = open_csv_list("metadata.csv")
            csv_info = open_csv("metadata.csv")
        except FileNotFoundError:
            sg.popup_error(
                """No se pudo crear el archivo de metadata, no podemos mostrar
                los datos."""
            )
        else:
            found = False
            for line in csv_info:
                if name in line["relative_path"]:
                    window["-LABELS-"].update(line["tags"].replace(";", ","))
                    window["-DESCRIPTION-"].update(line["description"])
                    found = True
            window["-IMGNAME-"].update(f"Nombre: {name}")
            window["-IMGSIZE-"].update(f"Dimensiones: {img.size} px")
            window["-IMGMB-"].update(
                f"Tamaño: {round((os.path.getsize(image_path) / 1024) / 1024, 3)} mb"
            )
            if not found:
                window["-LABELS-"].update("")
                window["-DESCRIPTION-"].update("")
            window["-IMAGE-"].update(data=img_tk)


def update_csv(values: dict, images_directories: str, current_user: str):
    """Recibe la imagen seleccionada, las tags y la descripccion, en base a
    la imagen consige sus metadatos y los pone en
    un diccionario, despues llama edit_img_csv data para manejar la escritura.

    Args:
        values (dict):  Diccionario con todos los datos de al ventana.
        images_directories (str):  Directorio de las imagenes.
        current_user (str):  El usuario que hizo el cambio.
    """    
    try:
        image_path = os.path.abspath(
            os.path.join(images_directories, values["-FILELIST-"][0])
        )
        image = Image.open(image_path)
    except IndexError:
        error_window("ERROR: imagen no seleccionada")
    except UnidentifiedImageError:
        error_window("ERROR: no se puede guardar una imagen corrupta")
    else:
        data = {
            "current_user": current_user,
            "relative_path": os.path.relpath(image_path, os.getcwd()).replace('\\', '/'),
            "resolution": image.size,
            "format": image.format,
            "last_update": datetime.timestamp(datetime.now()),
            "tags": values["-LABELS-"].replace(",", ";"),
            "size_mb": round((os.path.getsize(image_path) / 1024) / 1024, 3),
            "description": values["-DESCRIPTION-"],
        }

        edit_img_csv(data)
