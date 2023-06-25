import PySimpleGUI as sg
from UNLPimage.src.meme.meme_function import start_edit
from UNLPimage.src.meme.meme_function import update_meme
from UNLPimage.src.meme.meme_function import edition_meme
from UNLPimage.src.meme.meme_function import save_meme
import os
from UNLPimage.common.path import PATH_FONTS
import UNLPimage.src.classes.log as logs


def run(meme_info, path):
    """ Muestra la ventana de edicion en la que
        permite elegir la fuente entre las disponibles,
        escribir en las cajas de texto del meme y un boton
        de actualizar para guardar y mostrar los cambios para
        finalmente guardar con un titulo y como .jpg y .png.

    Args:
        meme_info (dict): la informacion sobre el meme
        path (str): la direccion de la carpeta donde esta el meme
    """
    colors = ['black', 'white', 'red', 'green']
    logs.Log.try_open_logs()
    window = start_edit(len(meme_info["text_boxes"]), colors)
    meme = update_meme(window, meme_info["image"], path)
    font = ""
    copy = None
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSE_ATTEMPTED_EVENT:
            confirm = sg.popup_yes_no("¿Está seguro que desea salir?")
            if confirm == "Yes":
                exit()
        if event == "-RETURN-":
            break
        if event == "-FONTS-":
            font = values["-FONTS-"][0]
            font = os.path.join(PATH_FONTS, font)
        if event == "-SAVE-":
            if copy != None:
                save_meme(copy, path, meme_info)
            else:
                sg.popup_error("No se han realizado cambios")
        if event == "-UPDATE-":
            if font != "" and len(values['f_color'][0]) != 0:
                answer = sg.popup_yes_no("Desea guardar los cambios?")
                if answer == "Yes":
                    copy = meme.copy()
                    written_text = []
                    for i in range(len(meme_info["text_boxes"])):
                        written_text.append(values[f"-TEXT{i+1}-"])
                    edition_meme(window, meme_info, written_text, copy, font, values['f_color'][0])
            else:
                sg.popup_error("Seleccione una fuente")
    window.close()
