import PySimpleGUI as sg
import pickle
from vending_machine import run_vending_machine
from restock import run_restock
from management import run_management
from pickle_method_vending import Vending_Machine


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

vending_machines = [1, 2]

windows = {
    'Choose Machine' : choose_vending_machine_window(vending_machines)
}
# Saving vending machine objects using pickle
# with open("vending_machine_1.pkl", "wb") as file: # vending machine #1
#     pickle.dump(vending_machine_1, file)

# with open("vending_machine_2.pkl", "wb") as file: # vending machine #2
#     pickle.dump(vending_machine_2, file)



# with open("vending_machine_2.pkl", "rb") as file:
#     loaded_vending_machine_2 = pickle.load(file)
#     print("Loaded Vending Machine 2 layout:", loaded_vending_machine_2.row, "x", loaded_vending_machine_2.column)
#     print("Loaded Vending Machine 2 ID:", loaded_vending_machine_2.get_vending_machine_id())
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
            # Loading vending machine objects from pickle files
            with open("vending_machine_{}.pkl".format(selected_machine), "rb") as file:
                loaded_vending_machine = pickle.load(file)
            # with open("restock_machine{}.pkl".format(selected_machine), "rb") as file:
            #     loaded_restock_machine = pickle.load(file)
            # with open("management_machine{}.pkl".format(selected_machine), "rb") as file:
            #     loaded_management_machine = pickle.load(file)
                # print("Loaded Vending Machine 1 layout:", loaded_vending_machine_1.row, "x", loaded_vending_machine_1.column)
                # print("Loaded Vending Machine 1 ID:", loaded_vending_machine_1.get_vending_machine_id())
        if event == 'Vending Machine':
            windows['Main'].hide()
            run_vending_machine(loaded_vending_machine)
            windows['Main'].un_hide()
        if event == 'Restock':
            windows['Main'].hide()
            # run_restock(loaded_restock_machine)
            windows['Main'].un_hide()
        if event == 'Manage':
            windows['Main'].hide()
            # run_management(loaded_management_machine, loaded_restock_machine, loaded_vending_machine) # order will matter in the future
            windows['Main'].un_hide()

    windows['Choose Machine'].close()

if __name__ == "__main__":
    main()
