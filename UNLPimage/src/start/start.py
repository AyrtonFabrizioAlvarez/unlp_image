import PySimpleGUI as sg
import UNLPimage.src.new_profile.new_profile as new_profile_window
import UNLPimage.src.main.main as main_window
from UNLPimage.src.start.start_functions import read_users
from UNLPimage.src.start.start_functions import button_imgs
from UNLPimage.src.start.start_functions import start
from UNLPimage.src.start.start_functions import profile_modifications


def run():
    """Esta funcion muestra la ventana de inicio y permite
    acceder a la ventana de nuevo perfil y a la ventana
    principal con el perfil seleccionado. A su vez muestra
    las fotos de los perfiles disponibles y en caso de que
    haya mas de 4 se puedue usar el boton (ver mas) para
    cambiar los perfiles que se presentan inicialmente"""
    users = read_users()
    qty_users = len(users) - 1
    counter = qty_users

    window = start()

    counter, profiles = button_imgs(qty_users, counter, window, users)

    while True:
        event, values = window.read()
        match event:
            case sg.WINDOW_CLOSE_ATTEMPTED_EVENT:
                close = sg.popup_yes_no("¿Esta seguro de que quiere salir?")
                if close == "Yes":
                    break
            case "-SEE_MORE-":
                counter, profiles = button_imgs(qty_users, counter, window, users)
            case "-CREATE-":
                window.Hide()
                new_profile_window.run()
                users = read_users()
                qty_users = len(users) - 1
                counter = qty_users
                counter, profiles = button_imgs(qty_users, counter, window, users)
                window.UnHide()
            case _:
                window.Hide()
                profile_number = int(event[-2])
                main_window.run(profiles[profile_number])
                profiles = profile_modifications(profiles, window, profile_number)
                window.UnHide()
    window.close()
