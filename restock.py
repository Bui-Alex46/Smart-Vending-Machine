import PySimpleGUI as sg
import pandas as pd

def create_restock_window(item_table : pd.DataFrame, restock_instructions: pd.DataFrame): # : pd.DataFrame
    # restock_instructions = {
    #   'item slot' : 1 to 40
    #   'add or remove' : either 'add' or 'remove'
    #   'item ID' : 1 to 40 at the moment
    #   'number to add' : 0 to 15
    #}

    sg.theme('LightGreen')

    if restock_instructions.empty: # print there are no instructions
        layout_no_restock = [
            [sg.T('RESTOCKING')],
            [sg.T('No changes to be made.')],
            [sg.B('Close')]
        ]
        return sg.Window('Restock', layout_no_restock)
    else:
        layout_restock = [
            [sg.T('RESTOCKING')], # table is probably better
            
            # This is all wrong for now changes to restock_instructions table
            [[sg.T('Item slot: {item_slot} Item name: {item_name} Number to be in stock: {num_in_slot}'
                   .format(item_slot=index, item_name=item_table.loc[row['item ID'], 'item name'], 
                    num_in_slot=row['number to add']), pad=(0,0))] for index, row in restock_instructions.iterrows()],
            [sg.Submit(key='-submit-restock-'), sg.B('Cancel')]
        ]
        return sg.Window('Restock', layout_restock) #, resizable=True) #, finalize=True)

def run_restock(vending_machine_num):
    df_itemTable = pd.read_csv("database\\ItemTable.csv", index_col=0, header=0)
    df_vendingMachine = pd.read_csv("database\\VendingMachine{}.csv".format(vending_machine_num), index_col=0, header=0)
    df_vendingMachine.index.name = "item slot"
    df_restockInstructions = pd.read_csv("database\\RestockInstructions{}.csv".format(vending_machine_num), index_col=0, header=0)
    df_restockInstructions.index.name = "item slot"
    
    restock_window = create_restock_window(df_itemTable, df_restockInstructions)
    
    while True:
        event, values = restock_window.read()
        if event in (None, 'Exit', 'Close', 'Cancel'):
            break
        if event == '-submit-restock-': # changes inventory after restock
            updated_inventory = [[row['item ID'], row['number to add'] + df_vendingMachine.loc[index]['number in stock']] 
                                    if row['add or replace'] == 'add' else [row['item ID'], row['number to add']]
             for index, row in df_restockInstructions.iterrows()]
            df_vendingMachine = pd.DataFrame(updated_inventory, index=([x for x in range(1, 41)]), columns=(['item ID', 'number in stock']))
            df_vendingMachine.index.name = 'item slot'
            df_vendingMachine.to_csv("database\\VendingMachine{}.csv".format(vending_machine_num), index_label='item slot')

            break
            
    restock_window.close()
