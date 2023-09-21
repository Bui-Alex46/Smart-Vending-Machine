import PySimpleGUI as sg
#import pandas as pd

def create_vending_machine_window(itemTable, vendingmachine1): # : pd.DataFrame
    sg.theme('LightGreen')

    layout_vending_machine = [
        # vending machine page where items can be purchased, could be made into separate window which might be smart
        [sg.T('Vending Machine')],
        *[[sg.B(f'{itemTable.at[vendingmachine1.at[y + 5*(x-1), "Item ID"], "item name"]}', pad=(0,0), key=(y + 5*(x-1))) for y in range(1, 6)] for x in range(1, 9)],
        # need key and size and also change name to item, auto_size_button=True
    ]

    return sg.Window('Vending Machine', layout_vending_machine, resizable=True, finalize=True)

#another option is to create a new window?

def create_payment_window(item_name, purchase_cost : float):
    sg.theme('LightGreen')
    
    layout_purchase = [
        #[sg.T('Buying Item')],
        [sg.T(item_name)],
        [sg.T('${:.2f}'.format(purchase_cost), key='-remaining-cost-')],
        [sg.B("$5.00"), sg.B("$1.00"), sg.B("$0.50"), sg.B("$0.25")]
    ]
    
    return sg.Window('Buying Item', layout_purchase, resizable=True, finalize=True)
