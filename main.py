import PySimpleGUI as sg
import pandas as pd
from datetime import datetime

from vending_machine import create_vending_machine_window, create_payment_window, end_transaction_window
from restock import create_restock_window
from management import create_management_window, create_purchase_history_window, create_set_restock_instructions_window

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

# need a change into previous window function
def change_to_previous_window(previous_window, current_window):
    windows[current_window].close()
    del windows[current_window]
    windows[previous_window].un_hide()
    #for now no way to change the current, previous window because not ordered Dict
    #current process looks like this:
    # change_to_previous_window(previous_window, active_window)
    # previous_window, active_window = None, 'Main'

def complete_purchase(selected_item, remaining_balance):
    # change Inventory database
    df_vendingMachine1.at[selected_item['item ID'], 'number in stock'] -= 1
    df_vendingMachine1.to_csv("database\\VendingMachine1.csv", index_label='item slot')
    # add purchase history row
    df_purchaseHistory.loc[len(df_purchaseHistory.index)] = [len(df_purchaseHistory.index), selected_item['item ID'], pd.to_datetime(datetime.now()), 1]
    df_purchaseHistory.to_csv("database\\PurchaseHistory.csv", index=False)
    # also need checking for if an item has no items left
    # window creation could maybe happen outside this function
    return end_transaction_window(completed=True, change=remaining_balance)

def verify_restock_instructions(restock_instructions):
    pass

def main():
    remaining_balance : float = 0.00
    previous_window : str = None
    active_window : str = 'Main'
    restock_instructions = pd.DataFrame
    
    while True:             # Event Loop
        event, values = windows[active_window].read()
        if event in (None, 'Exit'): # maybe the x in top right shuts it down and there is a way to navigate between all pages with buttons
            break
        if event == 'Vending Machine':
            windows['Vending Machine'] = create_vending_machine_window(df_itemTable, df_vendingMachine1)
            previous_window, active_window = 'Main', event
            windows['Main'].hide()
        if event == 'Restock':
            windows['Restock'] = create_restock_window(df_itemTable, restock_instructions)
            previous_window, active_window = 'Main', event
            windows['Main'].hide()
        if event == 'Manage':
            windows['Manage'] = create_management_window()
            previous_window, active_window = 'Main', event
            windows['Main'].hide()
        if isinstance(event, int):
            if event > 0 and event < 41:
                selected_item = {
                    'item ID'   : df_vendingMachine1.loc[event]['item ID'], # waht is this it is wrong?
                    'item name' : df_itemTable.loc[event]['item name'],
                    'item cost' : df_itemTable.loc[event]['item cost']
                }
                remaining_balance = selected_item['item cost']
                windows['Buying Item'] = create_payment_window(selected_item['item name'], remaining_balance)
                windows['Vending Machine'].hide()
                previous_window, active_window = 'Vending Machine', 'Buying Item'
        if event in ("$5.00", "$1.00", "$0.50", "$0.25"): 
            # need confirmation window, maybe a initial cost and balance so far, also change button to get back money
            remaining_balance -= float(event[1:])
            windows['Buying Item']['-remaining-cost-'].update('${:.2f}'.format(remaining_balance))
            if remaining_balance <= 0:
                windows['End Transaction'] = complete_purchase(selected_item, -remaining_balance)
                windows['Buying Item'].close()
                del windows['Buying Item']
                active_window = 'End Transaction' # don't want to go back to buying item so vending machine is still previous window
        if event == 'Change or Close': # receive change back or cancel purchase on vending machine
            change = selected_item['item cost'] - remaining_balance
            if change == 0.0: # if no change was entered and they just don't want to buy
                event = 'Close'
            else: # close Buying Item and open change window
                windows['Buying Item'].close()
                windows['End Transaction'] = end_transaction_window(completed=False, change=change)
                active_window = 'End Transaction' # don't want to go back to buying item so vending machine is still previous window
        if event == 'Close': # close button pushed on any window
            change_to_previous_window(previous_window, active_window) # go back to previous window
            active_window = previous_window
            if previous_window == 'Main': # if on (Vending Machine or Restock or Manage) needs to be changed to a close button
                previous_window = None
            if previous_window == 'Vending Machine' or previous_window == 'Manage':
                previous_window = 'Main'
        if event == '-submit-restock-': # changes inventory after restock
            # need to change inventory here using values probably a dataframe in values or use "restock_instructions"
            change_to_previous_window(previous_window, active_window)
            active_window = previous_window
            previous_window = None
            # update inventory
        if event == 'Purchase History': # displays purchase history on management tool
            windows['Manage'].hide()
            windows['Purchase History'] = create_purchase_history_window(df_itemTable, df_purchaseHistory)
            previous_window, active_window = 'Manage', 'Purchase History'
        if event == 'set restock instructions': # management window for settting restock instructions
            windows['Manage'].hide()
            windows['Set Restock'] = create_set_restock_instructions_window(df_itemTable, df_vendingMachine1)
            previous_window, active_window = 'Manage', 'Set Restock'
        if event == '-save-restock-changes-':
            # print(df_itemTable.loc[df_itemTable['item name'] == values['-restock-item-name-15-']].index[0])
            restock_data = [[df_itemTable.loc[df_itemTable['item name'] == values['-restock-item-name-{}-'.format(x)]].index[0], 
              values['-restock-new-amount-{}-'.format(x)]]
             for x in range(1, 41)]
            restock_instructions = pd.DataFrame(restock_data, index=([x for x in range(1, 41)]), columns=(['item ID', 'number in stock']))
            restock_instructions.index.name = 'item slot'
            # print(restock_instructions)
            change_to_previous_window(previous_window, active_window)
            previous_window, active_window = 'Main', 'Manage'

    windows['Main'].close()

main()
