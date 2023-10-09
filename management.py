import PySimpleGUI as sg
from main import main, create_vending_machine_window

layout = [
                [sg.Text("Select a theme: ",size=(15,1)),
                sg.Combo(sg.theme_list(),key="t",default_value="BlueMono",size=(10,1))],
                [sg.Text("Please enter in a Vending Machine ID: ",size=(15,1)),
                 
                sg.InputText(key="n",size=(10,1))],
                [sg.Checkbox("Capitalize",key="c",size=(15,1))],
                [sg.Text("Enter the Vending ID: ",size=(15,1))]

             ]
window = sg.Window("Controls",layout)

while True:
        event,values = window.read()
        if event == sg.WINDOW_CLOSED:
           break
        if event == "Show":
             pass
        if event == "Reset":
            pass
window.close()