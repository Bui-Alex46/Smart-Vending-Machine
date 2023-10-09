import PySimpleGUI as sg

from vending_machine import run_vending_machine
from restock import run_restock
from management import run_management

def create_main_window():
    sg.theme('LightGreen')
    
    layout_home = [ # home page of application
        [sg.T('This is my main application')],
        [sg.B(button_text='Vending Machine'), 
         sg.B(button_text='Restock'), 
         sg.B(button_text='Manage')],
    ]

    return sg.Window('Main Application', layout_home)

main_window = create_main_window()

def main():
    # remaining_balance : float = 0.00
    # previous_window, active_window = None, 'Main'
    # restock_instructions = pd.DataFrame
    
    while True:             # Event Loop
        event, values = main_window.read()
        if event in (None, 'Exit'): # maybe the x in top right shuts it down and there is a way to navigate between all pages with buttons
            break
        if event == 'Vending Machine':
            main_window.hide()
            run_vending_machine()
            main_window.un_hide()
        if event == 'Restock':
            main_window.hide()
            run_restock()
            main_window.un_hide()
        if event == 'Manage':
            main_window.hide()
            run_management()
            main_window.un_hide()

    main_window.close()

if __name__ == "__main__":
    main()
