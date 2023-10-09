import PySimpleGUI as sg
import pandas as pd
from datetime import datetime

def change_to_previous_window(previous_window, current_window, windows):
    windows[current_window].close()
    del windows[current_window]
    windows[previous_window].un_hide()

def create_vending_machine_window(itemTable : pd.DataFrame, vendingMachine : pd.DataFrame): # : pd.DataFrame
    sg.theme('LightGreen')

    layout_vending_machine = [
        # vending machine page where items can be purchased, could be made into separate window which might be smart
        [sg.T('Vending Machine')],
        *[[sg.B(f'{itemTable.at[vendingMachine.at[y + 5*(x-1), "item ID"], "item name"]}', pad=(0,0), key=(y + 5*(x-1))) for y in range(1, 6)] for x in range(1, 9)],
        # how to make size of button change with screen
        [sg.B('Close')],
    ]

    return sg.Window('Vending Machine', layout_vending_machine, resizable=True, finalize=True)

#another option is to create a new window?

def create_payment_window(item_name : str, purchase_cost : float):
    sg.theme('LightGreen')
    
    layout_purchase = [
        #[sg.T('Buying Item')],
        [sg.T(item_name, key='-item-name-')],
        [sg.T('${:.2f}'.format(purchase_cost), key='-remaining-cost-')],
        [sg.B('$5.00'), sg.B('$1.00'), sg.B('$0.50'), sg.B('$0.25')],
        [sg.B('Change or Close', tooltip='Click this to get change back or stop transaction')], #change button to get back money spent so far
    ]
    
    return sg.Window('Buying Item', layout_purchase, finalize=True) # resizable=True

def end_transaction_window(in_stock : bool, remaining_balance : float): 
    # change can mean 2 things (leftover after buying, amount entered that didn't reach balance)
    sg.theme('LightGreen')
    
    if in_stock: # if an item was purchased
        if remaining_balance < 0: # if they paid more than cost of item
            layout_change_after_completed = [
                [sg.T('Thank you for your purchase')],
                [sg.T('Here is your change: ${:.2f}'.format(-remaining_balance))],
                [sg.B('Close')] # unsure how to name, 'Exit' is obvious choice but brings complexity
            ]
            
            return sg.Window('Item Bought', layout_change_after_completed) #, resizable=True)
        elif remaining_balance == 0.0: # if change was exact
            layout_completed_purchase = [
                [sg.T('Thank you for your purchase')],
                [sg.B('Close')]
            ]
            
            return sg.Window('Item Bought', layout_completed_purchase) #, resizable=True) don't think we need to resize most windows
        else: # if paid less than cost of item and pressed change
            layout_return_change = [
                [sg.T('Here is your change back: ${:.2f}'.format(remaining_balance))],
                [sg.B('Close')]
            ]
            
            return sg.Window('Return Change', layout_return_change)
    else: # if out of stock
        layout_out_of_stock = [
            [sg.T('This item is out of stock')],
            [sg.B('Close')]
        ]
        
        return sg.Window('Out of stock', layout_out_of_stock)
    
def complete_purchase(selected_item, vendingMachine, purchaseHistory):
    # change Inventory database
    vendingMachine.at[selected_item['item ID'], 'number in stock'] -= 1
    vendingMachine.to_csv("database\\VendingMachine1.csv", index_label='item slot')
    # add purchase history row
    purchaseHistory.loc[len(purchaseHistory.index)] = [len(purchaseHistory.index), selected_item['item ID'], pd.to_datetime(datetime.now()), 1]
    purchaseHistory.to_csv("database\\PurchaseHistory.csv", index=False)
    
def run_vending_machine():
    df_itemTable = pd.read_csv("database\\ItemTable.csv", index_col=0, header=0)
    df_vendingMachine1 = pd.read_csv("database\\VendingMachine1.csv", index_col=0, header=0)
    df_purchaseHistory = pd.read_csv("database\\PurchaseHistory.csv")
    
    windows = {
        'Vending Machine' : create_vending_machine_window(df_itemTable, df_vendingMachine1),
    }
    
    previous_window, active_window = 'Main', 'Vending Machine'
    
    while True:
        event, values = windows[active_window].read()
        if event in (None, 'Exit'):
            break
        if event == 'Close': # close button pushed on any window
            if previous_window == 'Main':
                break
            change_to_previous_window(previous_window, active_window, windows) # go back to previous window
            active_window = previous_window
            if previous_window == 'Vending Machine':
                previous_window = 'Main'
            
        if isinstance(event, int):
            if event > 0 and event < 41:
                if df_vendingMachine1.loc[event]['number in stock'] > 0:
                    selected_item = {
                        'item ID'   : df_vendingMachine1.loc[event]['item ID'], # waht is this it is wrong?
                        'item name' : df_itemTable.loc[event]['item name'],
                        'item cost' : df_itemTable.loc[event]['item cost']
                    }
                    remaining_balance = selected_item['item cost']
                    windows['Buying Item'] = create_payment_window(selected_item['item name'], remaining_balance)
                    windows['Vending Machine'].hide()
                    previous_window, active_window = 'Vending Machine', 'Buying Item'
                else: # if out of stock
                    windows['End Transaction'] = end_transaction_window(False, 0)
                    windows['Vending Machine'].hide()
                    previous_window, active_window = 'Vending Machine', 'End Transaction'
        if event in ("$5.00", "$1.00", "$0.50", "$0.25"): 
            # need confirmation window, maybe a initial cost and balance so far, also change button to get back money
            remaining_balance -= float(event[1:])
            windows['Buying Item']['-remaining-cost-'].update('${:.2f}'.format(remaining_balance))
            if remaining_balance <= 0:
                complete_purchase(selected_item, df_vendingMachine1, df_purchaseHistory)
                windows['End Transaction'] = end_transaction_window(in_stock=True, remaining_balance=remaining_balance)
                windows['Buying Item'].close()
                del windows['Buying Item']
                active_window = 'End Transaction' # don't want to go back to buying item so vending machine is still previous window
        if event == 'Change or Close': # receive change back or cancel purchase on vending machine
            change = selected_item['item cost'] - remaining_balance
            if change == 0.0: # if no change was entered and they just don't want to buy
                change_to_previous_window(previous_window, active_window, windows) # go back to previous window
                active_window = previous_window
                previous_window = 'Main'
            else: # close Buying Item and open change window
                windows['Buying Item'].close()
                del windows['Buying Item']
                windows['End Transaction'] = end_transaction_window(in_stock=True, remaining_balance=change)
                active_window = 'End Transaction' # don't want to go back to buying item so vending machine is still previous window

    windows['Vending Machine'].close()
