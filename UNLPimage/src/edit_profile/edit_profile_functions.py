import os
import json
from PIL import Image, ImageDraw

# CONSTANTES
from UNLPimage.common.path import PATH_IMAGE_AVATAR, PATH_DATA_JSON

# FUNCIONES PROPIAS
import UNLPimage.src.new_profile.new_profile_functions as new_functions


# FUNCION PARA EDITAR UN USUARIO EN EL ARCHIVO JSON
def edit_json_user(user: dict):
    """Esta funcion recibe un diccionario con los datos del usuario buscado.
    Al encontrarlo modifica los datos del mismo (excepto el campo nick)"""
    path = PATH_DATA_JSON
    path_file = os.path.join(path, "usuarios.json")

    with open(path_file, "r", encoding="utf8") as file:
        JSON = json.load(file)
        data = JSON

    for dicc in data:
        if dicc["nick"] == user["nick"]:
            dicc["name"] = user["name"]
            dicc["age"] = user["age"]
            dicc["gender"] = user["gender"]
            dicc["avatar"] = user["avatar"]

    with open(path_file, "w", encoding="utf8") as file:
        file.write(json.dumps(data, indent=4))


# ARMAMOS UN DICCIONARIO CON LOS VALORES INGRESADOS SEGUN SI ESTA 
# O NO EL CHECKBOX
def read_inputs_edit(window: object, value: dict, initial_user: dict) -> dict:
    """Esta funcion va a tomar los datos del usuario en pantalla en funcion
    de si esta o no seleccionado el 'checkbox'.
    En el caso de los datos personales del usuario 'lee' los inputs
    correspondientes, en el caso del avatar se llama a la funcion
    'get_img_name'la cual formatea la url completa para obtener solo el
    nombre de la imagen."""
    # FORMATEAMOS LA URL DEL AVATAR PARA SOLO GUARDAR SU NOMBRE
    avatar_url = window["-AVATAR URL-"].get()
    avatar_name = new_functions.get_img_name(avatar_url,
                                             initial_user["avatar"])
    if not (avatar_name == "user_img.png"):
        img = Image.open(avatar_url)
        image = img.resize((1024, 1024))

        # Crear una máscara de círculo
        mask = Image.new("L", image.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, image.size[0], image.size[1]), fill=255,
                     outline="black")

        # Aplicar la máscara a la imagen
        rounded_image = Image.new("RGBA", image.size, 0)
        rounded_image.paste(image, (0, 0), mask=mask)

        # Guardar la imagen redondeada
        avatar_name = f"{value['-NICK-'].lower().replace(' ', '')}.png"
        new_path = os.path.join(PATH_IMAGE_AVATAR, avatar_name)
        try:
            rounded_image.save(new_path)
        except ValueError:
            pass

    # ARMAMOS EN 'USUARIO' UN DICCIONARIO CON LOS VALORES INGRESADOS
    # SEGUN SI ESTA O NO EL CHECKBOX
    nick = value["-NICK-"].lower().replace(" ", "")
    name = value["-NAME-"].lower().replace(" ", "")
    age = value["-AGE-"].lower().replace(" ", "")
    gender = value["-GENDER-"].lower()
    gender_input = value["-GENDER INPUT-"].lower().replace(" ", "")

    if not window["-CHECKBOX-"].get():
        user = {
            "nick": nick,
            "name": name,
            "age": age,
            "gender": gender,
            "avatar": avatar_name,
        }
    else:
        user = {
            "nick": nick,
            "name": name,
            "age": age,
            "gender": gender_input,
            "avatar": avatar_name,
        }
    return user


# FUNCION PARA VALIDAR SI SE EDITARA O NO UN USUARIO EN EL ARCHIVO JSON
def edit_user(window: object, value: dict, initial_user: dict) -> tuple[(dict,
                                                                        bool)]:
    """Esta funcion recibe la 'window', y 'value'
    (diccionario con valores de los eventos)
    para luego editar el usuario existente en archivo 'usuarios.json'"""
    user = read_inputs_edit(window, value, initial_user)

    # VALIDACION Y EDIT DEL USUARIO
    if new_functions.validate_user(user):
        edit_json_user(user)
        return (user, True)
    else:
        new_functions.validate_inputs(window)
        return (user, False)


# FUNCION PARA VOLCAR EN PANTALLA LOS DATOS DEL USUARIO ACTIVO
def get_active_user_data(window: object, nick: str):
    """Esta funcion recibe la window, y el nick del usuario en sesion.
    verifica y coloca en pantalla los datos del usuario
    que tenemos en el archivo 'usuarios.json'"""

    def chosen_gender(gender: str) -> bool:
        """Esta funcion recibe el genero que tiene un usuario en el archivo
        'usuarios.json' si es una de las opciones del elemento combo (masculino
        , femenino, no binario) retornamos true, en cualquier otro caso
        retornamos false"""
        if (gender == "masculino" or gender == "femenino" or gender == "no binario"):
            return True
        else:
            return False

    # BUSCO LOS DATOS DEL USUARIO EN EL JSON
    user = new_functions.get_user(nick)

    # ACA PONGO AUTOMATICAMENTE LOS DATOS DEL USUARIO A EDITAR EN LOS IMPUT
    # DE LA PANTALLA EDITAR USUARIO
    window["-NICK-"].update(user["nick"])
    window["-NAME-"].update(user["name"])
    window["-AGE-"].update(user["age"])
    path_avatar = os.path.join(PATH_IMAGE_AVATAR, user["avatar"])
    window["-AVATAR URL-"].update(path_avatar)
    window["AVATAR"].update(source=path_avatar, subsample=4)
    if chosen_gender(
        user["gender"]
    ):  # VERIFICAMOS EL GENERO, SI ES UNO DE LOS GENEROS DEL COMBO, DE SER
        # ASI LO COLOCO EN EL MISMO
        window["-GENDER-"].update(user["gender"])
    else:  # SINO TILDAMOS EL CHECKBOX, HACEMOS VISIBLE EL INPUT OPCIONAL
        # Y VOLCAMOS LA INFO
        window["-CHECKBOX-"](value=True)
        window["-GENDER INPUT-"](visible=True)
        window["-GENDER INPUT-"].update(user["gender"])
