import PySimpleGUI as sg

def create_restock_window():
    sg.theme('LightGreen')

    layout_restock = [
        [sg.T('RESTOCKING')],
        [sg.B('Close')]
    ]

    return sg.Window('Restock', layout_restock, resizable=True) #, finalize=True)
