import os
import json
from PIL import Image, ImageDraw

# CONSTANTES
from UNLPimage.common.path import PATH_DATA_JSON, PATH_IMAGE_AVATAR


# FUNCION PARA DAR DE ALTA UN USUARIO EN EL ARCHIVO 'USUARIOS.JSON'
def new_json_user(user: dict):
    """Esta funcion recibe un diccionario
    {"nick":"nickNuevo2","name":"nameNuevo2","age":25,"gender":"no binario"}
    y lo da de alta en el archivo 'usuarios.json'"""
    path = PATH_DATA_JSON
    path_file = os.path.join(path, "usuarios.json")

    try:
        with open(path_file, "r", encoding="utf8") as file:
            data = json.load(file)
            data.append(user)
    except FileNotFoundError:
        data = [user]

    with open(path_file, "w+", encoding="utf8") as file:
        file.write(json.dumps(data, indent=4))


# VALIDAR CAMPOS DE USUARIO
def validate_user(user: dict) -> bool:
    """Esta funcion recibe un diccionario y retorna true si alguno de sus
    valores presenta un problema para dar de alta o editar un usuario.

    Tiene en cuenta:
    -nick:  si es vacio
    -name: si es vacio o si tiene numeros
    -age:   si es vacio, si tiene una letra o si esta en rango (18 > age < 75)
    -gender: si es vacio"""

    nick, name, age, gender, avatar = user.values()
    ok = True
    if (nick == "") or (len(nick) < 4) or (len(nick) > 12):
        ok = False
    elif (name == "") or (not name.isalpha()) or (len(name) < 4) or (len(name) > 12):
        ok = False
    elif (age == "") or (not age.isnumeric()) or ((int)(age) > 75) or ((int)(age) < 18):
        ok = False
    elif gender == "":
        ok = False

    return ok


# FUNCION QUE MARCA LOS CAMPOS QUE FALTAN COMPLETAR EN NUEVO PERFIL
def validate_inputs(window: object):
    """Esta funcion 'lee' los inputs ingresados, y cuando hay un error
    en la validacion luego avisar al usuario el inconveniente ocurrido"""
    nick = window["-NICK-"].get().replace(" ", "")  # NICK - STRING
    name = window["-NAME-"].get().replace(" ", "")  # NAME - STRING
    ageStr = window["-AGE-"].get().replace(" ", "")  # AGE - STRING

    if (
        window["-NICK-"].ReadOnly == False
    ):  # SOLO VOY A VALIDAR EL NICK CUANDO ES UN NUEVO PERFIL, EN EDIT TENDRIA ERROR DE NICK EXISTENTE
        if nick == "":  # VALIDO SI EL NICK ES UN STRING VACIO
            window["-NICK-"].update(background_color="IndianRed4")
            window["-NICK-"].update("el campo es obligatorio")
        elif (len(nick) < 4) or (
            len(nick) > 12
        ):  # VALIDO SI EL NICK TIENE ENTRE 4 Y 12 CARACTERES
            window["-NICK-"].update(background_color="IndianRed4")
            window["-NICK-"].update("El nick debe tener entre 4 y 12 letras")

    if name == "":  # VALIDO SI EL NOMBRE ES UN STRING VACIO
        window["-NAME-"].update(background_color="IndianRed4")
        window["-NAME-"].update("el campo es obligatorio")
    elif not name.isalpha():  # VALIDO SI EL NOMBRE TIENE NUMEROS (NO SE PUEDE)
        window["-NAME-"].update(background_color="IndianRed4")
        window["-NAME-"].update("El nombre debe contener solo letras")
    elif (len(name) < 4) or (
        len(name) > 12
    ):  # VALIDO SI EL NOMBRE TIENE ENTRE 4 Y 12 CARACTERES
        window["-NAME-"].update(background_color="IndianRed4")
        window["-NAME-"].update("El nombre debe tener entre 4 y 12 letras")

    if ageStr == "":  # VALIDO SI LA EDAD SE INGRESO COMO UN STRING VACIO
        window["-AGE-"].update(background_color="IndianRed4")
        window["-AGE-"].update("el campo es obligatorio")
    elif (
        not ageStr.isnumeric()
    ):  # VALIDO SI LA EDAD SE INGRESO CON LETRAS O NUMEROS NEGATIVOS
        window["-AGE-"].update(background_color="IndianRed4")
        window["-AGE-"].update("El campo solo acepta numeros")
    elif (int)(window["-AGE-"].get().replace(" ", "")) > 75 or (int)(
        window["-AGE-"].get().replace(" ", "")
    ) < 18:  # VALIDO SI LA EDAD ESTA ENTRE 18 Y 75 AÑOS
        window["-AGE-"].update(background_color="IndianRed4")
        window["-AGE-"].update("Ingrese edad entre 18 y 75 años")


# ARMAMOS UN DICCIONARIO CON LOS VALORES INGRESADOS SEGUN SI ESTA O
# NO EL CHECKBOX
def read_inputs_new(window: object, value: dict) -> dict:
    """Esta funcion va a tomar los datos del usuario en pantalla en funcion
    de si esta o no seleccionado el 'checkbox'.
    En el caso de los datos personales del usuario 'lee' los inputs
    correspondientes,en el caso del avatar se llama a la funcion 'get_img_name'
    la cual formatea la url completa para obtener solo el nombre de la imagen.
    Luego se crea una imagen redondeada en /images/avatar con
    'nombreDelUsuario.png'"""

    nick = value["-NICK-"].lower().replace(" ", "")
    name = value["-NAME-"].lower().replace(" ", "")
    age = value["-AGE-"].lower().replace(" ", "")
    gender = value["-GENDER-"].lower()
    gender_input = value["-GENDER INPUT-"].lower().replace(" ", "")

    # FORMATEAMOS LA URL DEL AVATAR PARA SOLO GUARDAR SU NOMBRE
    avatar_url = window["-AVATAR URL-"].get()
    avatar_name = get_img_name(avatar_url)
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


# FUNCION PARA VALIDAR SI SE DARA DE ALTA O NO UN NUEVO USUARIO EN EL
# ARCHIVO JSON
def new_user(window: object, value: dict) -> bool:
    """Esta funcion recibe la 'window', y 'valor'
    (diccionario con valores de los eventos), luego de validar datos
    ingresados, agrega el usuario nuevo al archivo 'usuarios.json'"""

    user = read_inputs_new(window, value)

    # VALIDACION Y ALTA DEL USUARIO INGRESADO
    if user_exist(user["nick"]):
        window["-NICK-"].update(background_color="IndianRed4")
        window["-NICK-"].update("el nick ingresado ya existe")
    else:
        if validate_user(user):
            new_json_user(user)
            return True
        else:
            validate_inputs(window)
            return False


# FUNCION QUE BLANQUEA LOS INPUTS SI ESTAN VACIOS NUEVO PERFIL
def clear_inputs(window: object):
    """Esta funcion verifica la cantidad de caracteres en el input,
    ya que pueden haber sido coloreados por un error posterior
    (car < 3 entonces input = blanco)"""
    if len(window["-NICK-"].get()) < 3:
        window["-NICK-"].update(
            background_color="white"
        )  # COLOR QUE ACORDEMOS CON EL GRUPO
    if len(window["-NAME-"].get()) < 3:
        window["-NAME-"].update(
            background_color="white"
        )  # COLOR QUE ACORDEMOS CON EL GRUPO
    if len(window["-AGE-"].get()) < 3:
        window["-AGE-"].update(
            background_color="white"
        )  # COLOR QUE ACORDEMOS CON EL GRUPO


# IR A BUSCAR DATOS DE UN USUARIO SELECCIONADO
def get_user(nick: str) -> dict:
    """Esta funcion recibe un string que representa la clave 'nick'
    y si lo encuentra retorna un diccionario que representa al usuario"""
    ruta = PATH_DATA_JSON
    rutaArchivo = os.path.join(ruta, "usuarios.json")

    with open(rutaArchivo, "r", encoding="utf8") as archivo:
        data = list(json.load(archivo))

    user = list(filter((lambda x: x["nick"] == nick), data))

    return user[0]


# FUNCION PARA VERIFICAR SI UN nick EXISTE EN EL ARCHIVO 'USUARIOS.JSON'
def user_exist(nick: str) -> bool:
    """Esta funcion recibe un nick y retorna true si el usuario existe
    en el archivo 'usuarios.json', de lo contrario retorna false"""
    path = PATH_DATA_JSON
    path_file = os.path.join(path, "usuarios.json")

    try:
        with open(path_file, "r", encoding="utf8") as file:
            JSON = json.load(file)
            data = JSON

        for dicc in data:
            if dicc["nick"] == nick:
                return True

    except FileNotFoundError:
        return False


# FUNCION QUE FORMATEA LA RUTA DEL AVATAR
def get_img_name(url: str, default="DEFAULT_ICON.png") -> str:
    """Esta funcion recibe un string con el path de un archivo y
    un parametro por opcional que
    - si el url ingresado es vacio va a retornar el avatar default
    o el valor ingresado como parametro opcional

    retorna solo el nombre del archivo.
    Tiene en cuenta 2 situaciones dependiendo del sistema operativo.
    1- si los directorios estan separados con '/'
    2- si los directorios estan separados con \\"""
    if url == "":
        return default  # IMAGEN_DEFECTO NECESITO LA CONSTANTE
    if "/" in url:
        name = url.split("/")[-1]
    elif "\\" in url:
        name = url.split("\\")[-1]
    return name


# FUNCION QUE TOMA UNA IMAGEN, LA REDONDEA Y LUEGO LO GUARDA
# EN IMAGE/IMAGE/AVATAR
def user_img(window: object, img_path: str, name="user_img") -> str:
    """Esta funcion recibe una ventana y una ruta de imagen,
    genera una nueva imagen, la guarda en '/image/image/avatar'
    con forma redondeada y con un resize de (1024x1024)"""
    # Cargar la imagen
    img = Image.open(img_path)
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
    path = os.path.join(PATH_IMAGE_AVATAR, name + ".png")
    try:
        rounded_image.save(path)
    except ValueError:
        pass
    return path


# FUNCION QUE VERIFICA SI ES NECESARIO ELIMINAR UNA IMAGEN ANTES DE VOLVER
# A LA PESTAÑA ANTERIOR
def delete_img_before_back(window: object):
    """Esta funcion verifica si es necesario eliminar
    una imagen antes de volver al menu de inicio sin crear un perfil"""
    nick = window["-NICK-"].get()
    if not nick == "":
        to_delete_nick = f"{window['-NICK-'].get().lower().replace(' ', '')}.png"
        if os.path.exists(os.path.join(PATH_IMAGE_AVATAR, to_delete_nick)):
            os.remove(os.path.join(PATH_IMAGE_AVATAR, to_delete_nick))
