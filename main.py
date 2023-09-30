import PySimpleGUI as sg
import pandas as pd

from vending_machine import create_vending_machine_window
from restock import create_restock_window
from management import create_management_window

def create_main_window():
    sg.theme('LightGreen')
    
    layout_home = [ # home page of application
        [sg.T('This is my main application')],
        [sg.B(button_text='Vending Machine'), 
         sg.B(button_text='Restock'), 
         sg.B(button_text='Manage')],
    ]

    return sg.Window('Main Application', layout_home)

df_itemTable = pd.read_csv("database\\ItemTable.csv", index_col=0, header=0)
df_vendingMachine1 = pd.read_csv("database\\VendingMachine1.csv", index_col=0, header=0)
df_purchaseHistory = pd.read_csv("database\\PurchaseHistory.csv")

windows = {
        'Main' : create_main_window(), 
    }
    
windows_state = {
    'Main' : True,
    'Vending Machine' : False,
    'Restock' : False,
    'Manage' : False,
}

def hide_main_page(event):
    windows_state[event] = True
    windows_state['Main'] = False
    windows[event].un_hide()
    windows['Main'].hide()

def main():
    while True:             # Event Loop
        for name, state in windows_state.items():
            if state:
                event, values = windows[name].read()
                break
        if event in (None, 'Exit'):
            break
        if event == 'Vending Machine' and not windows_state['Vending Machine']: # might be redundant because of hiding
            windows['Vending Machine'] = create_vending_machine_window(df_itemTable, df_vendingMachine1)
            hide_main_page(event)
        if event == 'Restock' and not windows_state['Restock']:
            windows['Restock'] = create_vending_machine_window(df_itemTable, df_vendingMachine1)
            hide_main_page(event)
        if event == 'Manage' and not windows_state['Manage']:
            windows['Manage'] = create_vending_machine_window(df_itemTable, df_vendingMachine1)
            hide_main_page(event)
        try:
            if int(event) < 41 and int(event) > 0:
                print('buying item number: ', event)
        except:
            pass

    windows['Main'].close()

main()