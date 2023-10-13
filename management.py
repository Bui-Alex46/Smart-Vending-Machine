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
        [sg.Input("", enable_events=True, key="-INPUT-")],
        [sg.Button("Enter", key="-Enter-"), sg.Button("Exit")]
    ]

    window = sg.Window("Management Tool", layout)

    while True:
        event, values = window.read()

        print(event, values)  # will output what was entered in

        if (event == sg.WIN_CLOSED or event == "Exit"):  # takes care of window crashing error
            break
        else:
            if event == "-Enter-":  # when the user types something in
                vending_machine_inventory = pd.read_csv("database\VendingMachine{}.csv".format(values["-INPUT-"]), header=0)
            
                window.Close()


management_layout()
