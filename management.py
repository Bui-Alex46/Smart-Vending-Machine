import PySimpleGUI as sg
import pandas as pd

# reading .csv files
vending_machine_inventory = pd.read_csv("database\\VendingMachine1.csv")

# this is the management_tool
vending_machine_layout = [
    ["A1", "A2", "A3", "A4", "A5"],
    ["B1", "B2", "B3", "B4", "B5"],
    ["C1", "C2", "C3", "C4", "C5"],
    ["D1", "D2", "D3", "D4", "D5"], 
    ["E1", "E2", "E3", "E4", "E5"], 
    ["F1", "F2", "F3", "F4", "F5"],
    ["G1", "G2", "G3", "G4", "G5"],
    ["H1", "H2", "H3", "H4", "H5"]
]

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
                [sg.Button("", key="-STATUS-"), sg.Button("View Machine Status")],
                [sg.Button("", key="-LAYOUT-"), sg.Button("View Machine Layout")]  
                if event == "-INVENTORY-": # View the Inventory
                    
                    vending_machine_inventory = pd.read_csv("database\VendingMachine1.csv")
                    print(vending_machine_inventory)

                elif event == "-STATUS-": # View the machine status
                    pass
                    # View Machine Status
                elif event == "-LAYOUT-":
                    vending_machine_inventory = pd.read_csv("database\VendingMachine1.csv")
                    # Sample vending machine layout DataFrame (replace this with your actual vending machine layout DataFrame)
                    # vending_machine_layout_df = pd.DataFrame(...)

                    # Merge the inventory DataFrame with the vending machine layout DataFrame based on the "Location" column
                    merged_df = pd.merge(vending_machine_layout, vending_machine_inventory, on="Location", how="left")   

                    # Display the merged DataFrame
                    print("Machine Layout:")
                    print(merged_df)
           


management_layout()
