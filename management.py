import PySimpleGUI as sg
import pandas as pd

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

def create_set_restock_instructions_window(itemTable : pd.DataFrame, vendingMachine : pd.DataFrame):
    sg.theme('LightGreen')

    # [print(index, row) for index, row in vendingMachine.iterrows()]

    column = [
        # list all elements, then list current amount in stock, then field to change amount to be restocked?
        # Slot 1 Current Item: text New item: Drop menu Current Quantity: (0-15)text New Amount: (0-15)spin
        *[[sg.T('Slot {slot_num} Current Item: {current_item} New Item: '.format(slot_num=index, current_item=itemTable.loc[row['item ID']]['item name'])),
            sg.Drop(values=itemTable['item name'].tolist(), default_value=itemTable.loc[row['item ID']]['item name'], key='-restock-item-name-{}-'.format(index)),
            sg.T(' Current Quantity: {current_amount} New Amount: '.format(current_amount=row['number in stock'])),
            sg.Spin(values=[i for i in range(16)], initial_value=row['number in stock'], size=(6, 1), key='-restock-new-amount-{}-'.format(index))] for index, row in vendingMachine.iterrows()], # for x in range(1, 41)],
        #[sg.Drop(values=('BatchNorm', 'other'), auto_size_text=True)],
    ]

    layout_set_restock_instructions = [
        # a way for management to set what the restocker should do. Will later influence inventory
        [sg.Column(column, scrollable=True, vertical_scroll_only=True)],
        [sg.Button("Save", key='-save-restock-changes-'), sg.Button("Close")],
    ] # how do we save these changes

    return sg.Window('Set Restock Instructions', layout_set_restock_instructions, finalize=False)
