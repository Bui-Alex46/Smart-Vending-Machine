import PySimpleGUI as sg
from pandas import DataFrame

def create_vending_machine_window(itemTable : DataFrame, vendingmachine1 : DataFrame): # : pd.DataFrame
    sg.theme('LightGreen')

    layout_vending_machine = [
        # vending machine page where items can be purchased, could be made into separate window which might be smart
        [sg.T('Vending Machine')],
        *[[sg.B(f'{itemTable.at[vendingmachine1.at[y + 5*(x-1), "Item ID"], "item name"]}', pad=(0,0), key=(y + 5*(x-1))) for y in range(1, 6)] for x in range(1, 9)],
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
        [sg.B('Change', tooltip='Click this to get change back or stop transaction')], #change button to get back money spent so far
    ]
    
    return sg.Window('Buying Item', layout_purchase, finalize=True) # resizable=True

def end_transaction_window(completed : bool, change : float): 
    # change can mean 2 things (leftover after buying, amount entered that didn't reach balance)
    sg.theme('LightGreen')
    
    if completed:
        if change > 0:
            layout_change_after_completed = [
                [sg.T('Thank you for your purchase')],
                [sg.T('Here is your change: ${:.2f}'.format(change))],
                [sg.B('Close')] # unsure how to name, 'Exit' is obvious choice but brings complexity
            ]
            
            return sg.Window('Item Bought', layout_change_after_completed) #, resizable=True)
        else:
            layout_completed_purchase = [
                [sg.T('Thank you for your purchase')],
                [sg.B('Close')]
            ]
            
            return sg.Window('Item Bought', layout_completed_purchase) #, resizable=True) don't think we need to resize most windows
    else:
        layout_return_change = [
            [sg.T('Here is your change back: ${:.2f}'.format(change))],
            [sg.B('Close')]
        ]
        
        return sg.Window('Return Change', layout_return_change)
    
    
