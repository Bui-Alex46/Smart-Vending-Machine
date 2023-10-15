import PySimpleGUI as sg

from vending_machine import run_vending_machine
from restock import run_restock
from management import run_management

def choose_vending_machine_window(vending_machines):
    sg.theme('LightGreen')
    
    layout_vending_choose = [
        [sg.T('Choose a vending machine')],
        [sg.Drop(values=vending_machines, default_value=1, key='-vending-machine-id-')],
        # how to make size of button change with screen
        [sg.B('Select')],
    ]

    return sg.Window('Vending Machine Choice', layout_vending_choose)

def create_main_window():
    sg.theme('LightGreen')
    
    layout_home = [ # home page of application
        [sg.T('This is my main application')],
        [sg.B(button_text='Vending Machine'), 
         sg.B(button_text='Restock'), 
         sg.B(button_text='Manage')],
        [sg.B('Close')],
    ]

    return sg.Window('Main Application', layout_home)

vending_machines = [1, 2, 3]

windows = {
    'Choose Machine' : choose_vending_machine_window(vending_machines)
}

def main():
    active_window = 'Choose Machine'
    
    while True:             # Event Loop
        event, values = windows[active_window].read()
        if event in (None, 'Exit'): # maybe the x in top right shuts it down and there is a way to navigate between all pages with buttons
            break
        if event == 'Close':
            windows['Main'].close()
            windows['Choose Machine'].un_hide()
            active_window = 'Choose Machine'
        if event == 'Select':
            windows['Choose Machine'].hide()
            windows['Main'] = create_main_window()
            active_window = 'Main'
            selected_machine = values['-vending-machine-id-']
        if event == 'Vending Machine':
            windows['Main'].hide()
            run_vending_machine()
            windows['Main'].un_hide()
        if event == 'Restock':
            windows['Main'].hide()
            run_restock()
            windows['Main'].un_hide()
        if event == 'Manage':
            windows['Main'].hide()
            run_management(selected_machine)
            windows['Main'].un_hide()

    windows['Choose Machine'].close()

if __name__ == "__main__":
    main()
