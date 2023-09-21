import PySimpleGUI as sg
import pandas as pd

from vending_machine import create_vending_machine_window, create_payment_window
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

df_itemTable = pd.read_csv("SMART-VENDING-MACHINE\\database\\ItemTable.csv", index_col=0, header=0)
df_vendingMachine1 = pd.read_csv("SMART-VENDING-MACHINE\\database\\VendingMachine1.csv", index_col=0, header=0)
df_purchaseHistory = pd.read_csv("SMART-VENDING-MACHINE\\database\\PurchaseHistory.csv")

windows = {
        'Main' : create_main_window(), 
    }
    
windows_state = {
    'Main' : True,
    'Vending Machine' : False,
    'Buying Item': False,
    'Restock' : False,
    'Manage' : False,
}

def hide_main_page(event):
    windows_state[event] = True
    windows_state['Main'] = False
    windows['Main'].hide()
    #windows[event].un_hide()
    
remaining_balance = 0.00

def main():
    while True:             # Event Loop
        for name, state in windows_state.items():
            if state:
                event, values = windows[name].read()
                break
        if event in (None, 'Exit'): # and windows_state['Main']:
            break
        #for win in windows:
        #    if event in (None, 'Exit') and windows_state['Main'] == False:
        #        windows[win].close()
        if event == 'Vending Machine' and not windows_state['Vending Machine']: # might be redundant because of hiding
            windows['Vending Machine'] = create_vending_machine_window(df_itemTable, df_vendingMachine1)
            hide_main_page(event)
        if event == 'Restock' and not windows_state['Restock']:
            windows['Restock'] = create_restock_window()
            hide_main_page(event)
        if event == 'Manage' and not windows_state['Manage']:
            windows['Manage'] = create_management_window()
            hide_main_page(event)
        try:
            if int(event) > 0 and int(event) < 41:
                remaining_balance = df_itemTable.at[event, 'item cost']
                windows['Buying Item'] = create_payment_window(df_itemTable.at[event, 'item name'], remaining_balance)
                windows['Vending Machine'].hide()
                windows_state['Vending Machine'] = False
                windows_state['Buying Item'] = True
        except:
            pass
        if event in ("$5.00", "$1.00", "$0.50", "$0.25"):
            remaining_balance = remaining_balance-float(event[1:])
            windows['Buying Item']['-remaining-cost-'].update('${:.2f}'.format(remaining_balance))
            if remaining_balance <= 0:
                if remaining_balance == 0:
                    print('Bought')
                else:
                    print('Bought here is your change:', '${:.2f}'.format(-remaining_balance))
                windows['Buying Item'].close()
                windows['Vending Machine'].un_hide()
                windows_state['Buying Item'] = False
                windows_state['Vending Machine'] = True

    windows['Main'].close()

main()