# Here is where we are going to be be performing view inventory, and etc
import sys
import PySimpleGUI as sg


def view_inventory():
    print("view the inventoy here")


def push_restock():
    sg.popup('Restock instructions have been sent!')
    print('Restock has been pushed')


layout = [[sg.Text('Demo of Button Callbacks')],
          [sg.Button('Button 1'), sg.Button('Button 2')]]

window = sg.Window('Button Callback Simulation', layout)


while True:             # Event Loop
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    elif event == 'View Current Inventory':
        callback_function1()        # call the "view_inventory" function
    elif event == 'Push a Restock':
        push_restock()        # call the "Callback" function

window.close()