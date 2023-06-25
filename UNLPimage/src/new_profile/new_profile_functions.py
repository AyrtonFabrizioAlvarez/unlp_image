import os
import json
from PIL import Image, ImageDraw
import PySimpleGUI as sg

from UNLPimage.common.path import PATH_DATA_JSON, PATH_IMAGE_AVATAR
from UNLPimage.src.functions.files_functions import open_json_dict


# FUNCION PARA DAR DE ALTA UN USUARIO
def new_user(window: sg.Window, value: dict) -> bool:
    """Esta funcion recibe la 'window', y 'valor'
    (diccionario con valores de los eventos), luego de validar datos
    ingresados, agrega el usuario nuevo al archivo 'usuarios.json

    Args:
        window (sg.Window): objeto window de PySimpleGUI
        value (dict): diccionario con valores de eventos

    Returns:
        bool: True si el usuario es valido, caso contrario False
    """   
    user = read_inputs(window, value)
    ok = validate_new_user(user, window)
    if ok:
        add_json_user(user)
        create_user_img(window["-AVATAR URL-"].get(), user["nick"])
    return (user, ok)


# ARMAMOS UN DICCIONARIO CON LOS VALORES INGRESADOS SEGUN SI ESTA O NO EL CHECKBOX
def read_inputs(window: sg.Window, value: dict, default="DEFAULT_ICON.png") -> dict:
    """Esta funcion va a tomar los datos del usuario en pantalla en funcion
    de si esta o no seleccionado el 'checkbox'.
    En el caso de los datos personales del usuario 'lee' los inputs
    correspondientes.

    Args:
        window (sg.Window): objeto window de PySimpleGUI
        value (dict): diccionario con valores de eventos
        default (str, optional): Defaults to "DEFAULT_ICON.png".

    Returns:
        dict: usuario a dar de alta
    """    
    """"""
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
            "avatar": f"{nick}.png",
        }
    else:
        user = {
            "nick": nick,
            "name": name,
            "age": age,
            "gender": gender_input,
            "avatar": f"{nick}.png",
        }
    return user


# FUNCION PARA VALIDAR SI PUEDO DAR DE ALTA UN USUARIO
def validate_new_user(user: dict, window: sg.Window) -> bool:
    """Esta funcion es para validar un usuario que esta
    cargado en los inputs de la ventana

    Args:
        user (dict): usuario a validar
        window (sg.Window): objeto window de PySimpleGUI

    Returns:
        bool: True si el usuario es valido, caso contrario False
    """
    if user_exist(user["nick"]):
        window["-NICK-"].update(background_color="IndianRed4")
        window["-NICK-"].update("el nick ingresado ya existe")
    else:
        if valid_user(user, window):
            return True
        else:
            return False


# FUNCION PARA VERIFICAR SI EL USUARIO INGRESADO ES VALIDO
def valid_user(user: dict, window: object) -> bool:
    """Esta funcion recibe un diccionario y retorna true si alguno de sus
    valores presenta un problema para dar de alta o editar un usuario.
    Tiene en cuenta:
    -nick:  si es vacio
    -name: si es vacio o si tiene numeros
    -age:   si es vacio, si tiene una letra o si esta en rango (18 > age < 75)
    -gender: si es vacio

    Args:
        user (dict): usuario a validar
        window (sg.Window): objeto window de PySimpleGUI

    Returns:
        bool: True si el usuario es valido, False en caso de cualquier error
    """    
    nick, name, age, gender, avatar = user.values()
    ok = True
    if (nick == "") or (len(nick) < 4) or (len(nick) > 12):
        validate_nick_input(nick, window["-NICK-"])
        ok = False
    if (name == "") or (not name.isalpha()) or (len(name) < 4) or (len(name) > 12):
        validate_name_input(name, window["-NAME-"])
        ok = False
    if (age == "") or (not age.isnumeric()) or ((int)(age) > 75) or ((int)(age) < 18):
        validate_age_input(age, window["-AGE-"])
        ok = False
    if gender == "":
        validate_gender_input(gender, window["-GENDER INPUT-"], window["-GENDER-"])
        ok = False
    return ok


# FUNCION PARA VERIFICAR SI EL NICK INGRESADO ES VALIDO
def validate_nick_input(nick: str, input: sg.Input) -> None:
    """Esta funcion colorea el input nick si hay un error
    - campo obligatorio
    - entre 4 y 12 caracteres

    Args:
        nick (str): nick del usuario
        input (sg.Input): Input de PySimpleGUI
    """    
    # SOLO VOY A VALIDAR EL NICK CUANDO ES UN NUEVO PERFIL
    # EN EDIT TENDRIA ERROR DE NICK EXISTENTE
    if input.ReadOnly == False:
        if nick == "":
            input.update(background_color="IndianRed4")
            input.update("el campo es obligatorio")
        elif (len(nick) < 4) or (len(nick) > 12):
            input.update(background_color="IndianRed4")
            input.update("El nick debe tener entre 4 y 12 letras")


# FUNCION PARA VERIFICAR SI EL NAME INGRESADO ES VALIDO
def validate_name_input(name: str, input: sg.Input) -> None:
    """Esta funcion colores el input name si hay un error
    - campo obligatorio
    - solo letras
    - entre 4 y 12 caracteres
    
    Args:
        name (str): nombre del usuario
        input (sg.Input): Input de PySimpleGUI
    """
    match (name):
        case "":
            input.update(background_color="IndianRed4")
            input.update("el campo es obligatorio")
        case _ if not name.isnumeric():
            input.update(background_color="IndianRed4")
            input.update("El nombre debe contener solo letras")
        case _ if (len(name) < 4) or (len(name) > 12):
            input.update(background_color="IndianRed4")
            input.update("El nombre debe tener entre 4 y 12 letras")


# FUNCION PARA VERIFICAR SI AGE INGRESADO ES VALIDO
def validate_age_input(age: str, input: sg.Input) -> None:
    """Esta funcion colorea el input age si hay un error
    - campo obligatorio
    - solo numeros
    - entre 18 y 75 años
    
    Args:
        age (str): edad del usuario
        input (sg.Input): Input de PySimpleGUI
    """
    match (age):
        case "":
            input.update(background_color="IndianRed4")
            input.update("el campo es obligatorio")
        case _ if not age.isnumeric():
            input.update(background_color="IndianRed4")
            input.update("El campo solo acepta numeros")
        case _ if (int)(input.get().replace(" ", "")) > 75:
            input.update(background_color="IndianRed4")
            input.update("Ingrese edad entre 18 y 75 años")
        case _ if (int)(input.get().replace(" ", "")) < 18:
            input.update(background_color="IndianRed4")
            input.update("Ingrese edad entre 18 y 75 años")


# FUNCION PARA VERIFICAR SI EL GENDER INGRESADO ES VALIDO
def validate_gender_input(gender: str, input: sg.Input, combo: sg.Combo) -> None:
    """Esta funcion colorea el input de genero opcional si hay un error
    - campo obligatorio (combo)
    - campo obligatorio (input opcional)
    
    Args:
        gender (str): genero del usuario
        input (sg.Input): Input de PySimpleGUI
        combo (sg.Combo): Combo de PySimpleGUI
    """
    if gender == "":
        input.update(background_color="IndianRed4")
        input.update("el campo es obligatorio")
        combo.BackgroundColor = "IndianRed4"
    # COMO CAMBIAR DE COLOR EL COMBO DESPUES DE QUE YA ESTE DECLARADO(EN LA DECLARACION FUNCIONA)
    # YA PROBE .UPDATE(BACK....) Y BACKGROUND_COLOR = ...


# FUNCION QUE MODIFICA EL NOMBRE DE UNA IMAGEN
def rename_img(old_name: str, new_name: str) -> None:
    """Esta funcion recibe un nombre viejo y un nombre nuevo e intercambia
    el nombre del viejo por el nuevo (archivos .png) en la carpeta de avatares
    
    Args:
        old_name (str): nombre de url antiguo
        new_name (str): nombre de url nuevo
    """
    actual_path = os.path.join(PATH_IMAGE_AVATAR, old_name)
    new_path = os.path.join(PATH_IMAGE_AVATAR, f"{new_name}.png")
    os.rename(actual_path, new_path)


# FUNCION PARA DAR DE ALTA UN USUARIO EN EL ARCHIVO 'USUARIOS.JSON'
def add_json_user(user: dict) -> None:
    """Esta funcion recibe un usuario(dict) y lo agrega a usuarios.json

    Args:
        user (dict): {"nick":str,"name":str,"age":str,"gender":str} usuario a dar de alta
    """    
    #"""Esta funcion recibe un diccionario
    #{"nick":str,"name":str,"age":str,"gender":str}
    #y lo da de alta en el archivo 'usuarios.json'"""
    path = PATH_DATA_JSON
    path_file = os.path.join(path, "usuarios.json")

    try:
        data = open_json_dict("usuarios.json")
        data.append(user)
    except FileNotFoundError:
        data = [user]

    with open(path_file, "w+", encoding="utf8") as file:
        file.write(json.dumps(data, indent=4))


# FUNCION QUE BLANQUEA EL INPUT
def clear_input(input: sg.Input) -> None:
    """Esta funcion verifica la cantidad de caracteres en el input,
    ya que puede haber sido coloreado por un error anteriormente
    (car < 3 entonces input = #86a6df)
    
    Args:
        input (sg.Input): Input de PySimpleGUI
    """
    if len(input.get()) < 3:
        input.update(background_color="#86a6df")


# FUNCION PARA VERIFICAR SI UN NICK EXISTE EN EL ARCHIVO 'USUARIOS.JSON'
def user_exist(nick: str) -> bool:
    """Esta funcion verifica retorna si existe o no un nick

    Args:
        nick (str): nick ingresado (a validar)

    Returns:
        bool: True si el nick existe, caso contrario False
    """    
    try:
        data = open_json_dict("usuarios.json")
        for dicc in data:
            if dicc["nick"] == nick:
                return True
    except FileNotFoundError:
        return False


# FUNCION QUE TOMA UNA IMAGEN, LA REDONDEA Y LUEGO LO GUARDA
# EN IMAGE/IMAGE/AVATAR COMO "nick_usuario.png"
def create_user_img(img_path: str, name="DEFAULT_ICON") -> str:
    """Esta funcion recibe la ruta de una imagen,
    genera una nueva imagen, la guarda en '/image/image/avatar'
    con forma redondeada, con un resize de (1024x1024), y con un nombre
    recibido por parametro, en caso de no recibir nombre deja el de
    la imagen "DEFAULT_ICON.PNG"

    Args:
        img_path (str): url de imagen original
        name (str, optional): nombre opcional de la nueva imagen Defaults to "DEFAULT_ICON".
    """    
    img = Image.open(img_path)
    image = img.resize((1024, 1024))

    mask = Image.new("L", image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, image.size[0], image.size[1]), fill=255, outline="black")

    rounded_image = Image.new("RGBA", image.size, 0)
    rounded_image.paste(image, (0, 0), mask=mask)

    path = os.path.join(PATH_IMAGE_AVATAR, name + ".png")
    try:
        rounded_image.save(path)
    except ValueError:
        pass


# FUNCION QUE ELIMINA LA IMAGEN DEL USUARIO QUE NO LLEGO A CREARSE
def delete_img_before_back(nick: str) -> None:
    """Esta funcion verifica si es necesario eliminar
    una imagen antes de volver al menu de inicio sin crear un perfil
    
    Args:
        nick (str): nombre de la imagen a eliminar (en la carpeta images/avatar)
    """
    if not nick == "":
        to_delete_nick = f"{nick}.png"
        if os.path.exists(os.path.join(PATH_IMAGE_AVATAR, to_delete_nick)):
            os.remove(os.path.join(PATH_IMAGE_AVATAR, to_delete_nick))


# FUNCION QUE MANEJA CHECKBOX O INPUT DE GENERO
def change_gender_input(input: sg.Input, combo: sg.Combo) -> None:
    """Esta funcion cambia el estado del checkbox (tildado y destildado)
    en funcion de eso, tambien hara visible el input opcional de genero

    Args:
        input (sg.Input): input de PySimpleGUI
        combo (sg.Combo): combo de PySimpleGUI
    """    
    input.update(visible=(not input.visible))
    combo.update(disabled=(not combo.Disabled))
