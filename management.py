import PySimpleGUI as sg
from main import main, create_vending_machine_window

sg.theme("BlueMono") #changing the color

vending_machine_ids = ['1', '2', '3'] # just some example stuff we can use a .csv table to make things easier

layout = [
               
                [sg.text("Welcome to the Smart Vending Machine's Management System!")],
                [sg.text("Please enter in a Vending Machine ID: "), sg.InputText()],

         ]
window = sg.Window("Test",layout).Finalize()

while True:
        event,values = window.read()
        if event == sg.WINDOW_CLOSED: # close crash error
           break
        if event == '-INPUT-': # When the user enters in a vending machine ID
             if values['INPUT'] not in vending_machine_ids:
                  pass # check to see if the vending machine id is valid
            # IF Yes, then we will go to look into the inventory of a particulatr vending machine
window.close()