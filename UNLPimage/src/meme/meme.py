import PySimpleGUI as sg
import UNLPimage.src.meme.meme_edition as meme_window
from UNLPimage.src.meme.meme_function import take_memes
from UNLPimage.src.meme.meme_function import start
from UNLPimage.src.meme.meme_function import search_meme
from UNLPimage.src.meme.meme_function import update_meme
from UNLPimage.src.functions.files_functions import open_record


def run():
    """ Muestra la ventana y permite la seleccion
        seleccionar el template del meme y mostrar
        una previsualizacion del mismo, a su vez
        permite acceder a la siguiente ventana de
        edicion de memes.
    """    
    memes_names = take_memes()
    window = start(memes_names)
    meme = {}
    path = open_record()["-MEMEPATH-"]
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSE_ATTEMPTED_EVENT:
            confirm = sg.popup_yes_no("¿Está seguro que desea salir?")
            if confirm == "Yes":
                exit()
        if event == "-RETURN-":
            break
        if event == "-FILE-":
            meme = search_meme(values["-FILE-"][0], path)
            if meme != {}:
                update_meme(window, meme["image"], path)
            else:
                sg.PopupError("La imagen no se encuentra en el directorio")
                window["-IMAGE-"].Update()
        if event == "-EDITE-":
            if meme != {}:
                window.hide()
                meme_window.run(meme, path)
                window.un_hide()
            else:
                sg.popup("No elegiste una imagen")
    window.close()
