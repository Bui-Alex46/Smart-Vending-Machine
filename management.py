import PySimpleGUI as sg
import pandas as pd

from vending_machine import change_to_previous_window

def create_management_window():
    sg.theme('LightGreen')

    layout_manage = [ # management page, same as previous 2
        [sg.T('MANAGEMENT')],
        [sg.B('Purchase History'), sg.B('set restock instructions'),
         sg.B('View Inventory', key='management-view-inventory'), sg.B('View Status')], # viewing inventory from management side, and view status of vending machine
        [sg.B('Close')],
    ]

    return sg.Window('Management', layout_manage, resizable=True) #, finalize=True)

def create_purchase_history_window(itemTable : pd.DataFrame, purchaseHistory : pd.DataFrame):
    sg.theme('LightGreen')

    modified_purchaseHistory = purchaseHistory.merge(itemTable, left_on='purchased item ID', right_on='item ID', how='left')
    view_purchaseHistory = modified_purchaseHistory[['transaction ID', 'item name', 'time of transaction', 'vending machine ID']]
    
    layout_purchase_history = [
        # layout of purchase history
        [sg.Table(values=view_purchaseHistory.values.tolist(),
                  headings=view_purchaseHistory.columns.tolist(),
                  #auto_size_columns=False,
                  display_row_numbers=False,
                  justification='right',
                  #num_rows=min(25, len(purchaseHistory)),
        )],
        # how to make size of button change with screen
        [sg.B('Close')],
    ]

    return sg.Window('Purchase History', layout_purchase_history, finalize=False) #, finalize=True)

def create_view_inventory_window(itemTable : pd.DataFrame, vendingMachine : pd.DataFrame):
    sg.theme('LightGreen')

    modified_vendingMachine = vendingMachine.merge(itemTable, left_on='item ID', right_on='item ID', how='left')
    view_VendingMachine = modified_vendingMachine[['item slot', 'item name', 'number in stock']]
    
    layout_vending_machine = [
        [sg.Table(values=view_VendingMachine.values.tolist(),
                  headings=view_VendingMachine.columns.tolist(),
                  #auto_size_columns=False,
                  display_row_numbers=False,
                  justification='right',
                  #num_rows=min(40, len(vendingMachine)),
        )],
        # how to make size of button change with screen
        [sg.B('Close')],
    ]

    return sg.Window('Purchase History', layout_vending_machine, finalize=False) #, finalize=True)

def create_set_restock_instructions_window(itemTable : pd.DataFrame, vendingMachine : pd.DataFrame):
    sg.theme('LightGreen')

    # [print(index, row) for index, row in vendingMachine.iterrows()]

    column = [
        # list all elements, then list current amount in stock, then field to change amount to be restocked?
        # Slot 1 Current Item: text New item: Drop menu Current Quantity: (0-15)text New Amount: (0-15)spin
        *[[sg.T('Slot {slot_num} Current Item: {current_item} New Item: '.format(slot_num=index, current_item=itemTable.loc[row['item ID']]['item name'])),
            sg.Drop(values=itemTable['item name'].tolist(), default_value=itemTable.loc[row['item ID']]['item name'], key='-restock-item-name-{}-'.format(index)),
            sg.T(' Current Quantity: {current_amount} New Amount: '.format(current_amount=row['number in stock'])),
            sg.Spin(values=[i for i in range(16)], initial_value=row['number in stock'], size=(6, 1), key='-restock-new-amount-{}-'.format(index))] for index, row in vendingMachine.iterrows()],
    ]

    layout_set_restock_instructions = [
        # a way for management to set what the restocker should do. Will later influence inventory
        [sg.Column(column, scrollable=True, vertical_scroll_only=True)],
        [sg.Button("Save", key='-save-restock-changes-'), sg.Button("Close")],
    ] # how do we save these changes

    return sg.Window('Set Restock Instructions', layout_set_restock_instructions, finalize=False)

# def verify_restock_instructions(restock_instructions):
#     pass

def run_management():
    df_itemTable = pd.read_csv("database\\ItemTable.csv", index_col=0, header=0)
    df_itemTable.index.name = "item ID"
    df_vendingMachine1 = pd.read_csv("database\\VendingMachine1.csv", index_col=0, header=0)
    df_vendingMachine1.index.name = "item slot"
    df_purchaseHistory = pd.read_csv("database\\PurchaseHistory.csv", header=0)
    
    windows = {
        'Manage' : create_management_window(),
    }
    
    previous_window, active_window = 'Main', 'Manage'
    
    while True:
        event, values = windows[active_window].read()
        if event in (None, 'Exit'):
            break
        if event == 'Close': # close button pushed on any window
            if previous_window == 'Main': # if on (Vending Machine or Restock or Manage) needs to be changed to a close button
                break
            change_to_previous_window(previous_window, active_window, windows) # go back to previous window
            active_window = previous_window
            if previous_window == 'Manage':
                previous_window = 'Main'
        
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

            # [item slot,add or replace,item ID,number to add]
            restock_instructions = [['add', restock_data[x][0], restock_data[x][1] - df_vendingMachine1.loc[x+1]['number in stock']] 
                                    if restock_data[x][0] == df_vendingMachine1.loc[x+1]['item ID'] 
                                    else [x+1, 'replace', restock_data[x][0], restock_data[x][1]] for x in range(40)]
            # print(restock_instructions)
            
            # save to restockInstructions csv
            df_restock_instructions = pd.DataFrame(restock_instructions, index=([x for x in range(1, 41)]), columns=(['add or replace', 'item ID', 'number to add']))
            df_restock_instructions.index.name = 'item slot'
            df_restock_instructions.to_csv("database\\RestockInstructions.csv", index_label='item slot')
            # print(restock_instructions)
            change_to_previous_window(previous_window, active_window, windows)
            previous_window, active_window = 'Main', 'Manage'
        if event == 'management-view-inventory':
            windows['Manage'].hide()
            windows['View Inventory'] = create_view_inventory_window(df_itemTable, df_vendingMachine1)
            previous_window, active_window = 'Manage', 'View Inventory'
        if event == 'View Status':
            pass
            
    windows['Manage'].close()
