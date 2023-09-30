import PySimpleGUI as sg

def create_management_window():
    sg.theme('LightGreen')

    layout_manage = [ # management page, same as previous 2
        [sg.T('MANAGEMENT')],
        [sg.B('Close')],
    ]

    return sg.Window('Management', layout_manage, resizable=True) #, finalize=True)
