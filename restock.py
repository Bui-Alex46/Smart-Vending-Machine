import PySimpleGUI as sg
from pandas import DataFrame

def create_restock_window(item_table : DataFrame, restock_instructions: DataFrame): # : pd.DataFrame
    # restock_instructions = {
    #    'slot 1' : {'item name' : 'string', 'total_amount' : 0-15} ? maybe amount_to_add?
    #    '...slot 40' : {'item name' : 1-40, 'items_to_put' : 0-15}
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
            [[sg.T('Item slot: {item_slot} Item name: {item_name} Number to be in stock: {num_in_slot}'
                   .format(item_slot=index, item_name=item_table.loc[row['item ID'], 'item name'], 
                    num_in_slot=row['number in stock']), pad=(0,0))] for index, row in restock_instructions.iterrows()],
            [sg.Submit(key='-submit-restock-')]
        ]
        return sg.Window('Restock', layout_restock) #, resizable=True) #, finalize=True)
