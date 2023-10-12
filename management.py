import PySimpleGUI as sg
import pandas as pd
from vending_machine
from management_tool import  # gets the functions/functionality from the management tool



def management_layout():
   sg.theme("DarkBlue3")

   vending_machine_ids = [1, 2, 3]
   
   layout = [
            [sg.Text("Please Enter Vending Machine ID: ")],      
            [sg.Input('', enable_events= True, key = '-INPUT-')],
            [sg.Button("Enter", key="-Enter-"), sg.Button("Exit")]]
   
   window = sg.Window("Management Tool", layout)

   while True:
      
      event, values = window.read()

      print(event, values)

      if event == sg.WIN_CLOSED or event == "Exit":
            break
      else:
          if event == "Enter":
              if values ["-INPUT-"] == values in vending_machine_ids:
                  pass
              else:
                  sg.popup("Invalid Vending Machine ID. . . ")    
   window.close()






management_layout()