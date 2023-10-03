import PySimpleGUI as sg

def create_restock_window():
    sg.theme('LightGreen')
    event = windows[active_window].read()


    layout_restock = [
        [sg.T('RESTOCKING')],
        [sg.B('Close')]
    ]
    #if event == sg.WIN_CLOSED:
    #    pass

    return sg.Window('Restock', layout_restock, resizable=True) #, finalize=True)
