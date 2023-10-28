import PySimpleGUI as sg

from restocker_instructs import Restocker
from pickle_method_vending import send_instructions, send_email

def create_restock_window():
    sg.theme('LightGreen')
   

    layout_restock = [

        [sg.T('RESTOCKING')],
        [sg.B('Close')]
    ]
    #if event == sg.WIN_CLOSED:
    #    pass

    return sg.Window('Restock', layout_restock, resizable=True) #, finalize=True)
