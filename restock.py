import PySimpleGUI as sg

def create_restock_window():
    sg.theme('LightGreen')

    layout_restock = [ # restock page which also should probably be made into another window
        [sg.T("RESTOCKING")],
    ]

    return sg.Window('Restock', layout_restock, resizable=True, finalize=True)
