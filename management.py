import PySimpleGUI as sg
import pandas as pd

# reading .csv files
vending_machine_inventory = pd.read_csv("database\\VendingMachine1.csv")

# this is the management_tool


def management_layout():
    sg.theme("DarkBlue3")

    # Ask for the vending machine number,
    layout = [
        [sg.Text("Please Enter Vending Machine ID: ")],
        [sg.Input("", enable_events=True, key="-INPUT-")], # user types in the vending machine ID number
        [sg.Button("Enter", key="-ENTER-"), sg.Button("Exit")] # user clicks Enter
    ]

    window = sg.Window("Management Tool", layout)

    while True:
        event, values = window.read()

        print(event, values)  # will output what was entered in

        if (event == sg.WIN_CLOSED or event == "Exit"):  # takes care of window crashing error
            break
        else:
            if event == "-ENTER-":  # when the user types something in
                [sg.Text("Select an Option")],
                [sg.Button("", key="-INVENTORY-"), sg.Button("View Current Machine Inventory")],
                [sg.Button("", key="-STATUS-"), sg.Button("View Machine Status")]  
                if event == "-INVENTORY-": # 
                    
                    vending_machine_inventory = pd.read_csv("database\VendingMachine{}.csv".format(values["-INPUT-"]), header=0)
                elif event == "-STATUS-":
                    pass
                    # View Machine Status
           


management_layout()
