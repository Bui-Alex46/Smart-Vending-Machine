import PySimpleGUI as sg

from vending_machine import change_to_previous_window
from pickle_method_vending import *

def create_management_window():
    sg.theme('LightGreen')

    layout_manage = [ # management page, same as previous 2
        [sg.T('MANAGEMENT')],
        [sg.B('Purchase History'), sg.B('set restock instructions'),
         sg.B('View Inventory', key='management-view-inventory'), sg.B('View Status')], # viewing inventory from management side, and view status of vending machine
        [sg.B('Close')],
    ]

    return sg.Window('Management', layout_manage, resizable=True) #, finalize=True)

def create_purchase_history_window(purchase_history):
    sg.theme('LightGreen')
    
    layout_purchase_history = [
        # layout of purchase history
        [sg.Table(values=[[purchase.item.item_name, purchase.date_time_of_transaction] for purchase in purchase_history],
                  headings=['Item', 'Date & Time of Transaction'],
                  #auto_size_columns=False,
                  display_row_numbers=True,
                  justification='right',
                  #num_rows=min(25, len(purchaseHistory)),
        )],
        # how to make size of button change with screen
        [sg.B('Close')],
    ]

    return sg.Window('Purchase History', layout_purchase_history, finalize=False) #, finalize=True)

def create_view_inventory_window(inventory):
    sg.theme('LightGreen')
    
    column_table = [
        [sg.Table(values=[[slot.item_slot_num,
                           'out of stock' if len(slot.list) == 0 
                           else slot.product_title,len(slot.list)] 
                          for slot in inventory],
                  headings=['Item slot', 'Item name', 'Number in stock'], # need to add expiration date
                  auto_size_columns=True,
                  display_row_numbers=False,
                  justification='right',
                  # new window or table to show items in item slot
        )],
        # how to make size of button change with screen
    ]
    
    column_buttons = [
        *[[sg.Button('Show Items in Slot {slot_num}'.format(slot_num=slot.item_slot_num), key='show-items-{slot_num}'.format(slot_num=slot.item_slot_num))] for slot in inventory]
    ]
    
    layout_item_slot_table = [
        [sg.Table(values=[], headings=['Name', 'Price', 'Expiration date'],
                  display_row_numbers=True, justification='right', key='item-slot-data')]
    ]
     
    layout_vending_machine =[
        [sg.Column(column_table, size=(500, 300)), sg.Column(column_buttons, scrollable=True, vertical_scroll_only=True, size=(150, 300))], # , scrollable=True, vertical_scroll_only=True
        [layout_item_slot_table],
        [sg.B('Close')],
    ]

    return sg.Window('Vending Machine Inventory', layout_vending_machine, finalize=False) #, finalize=True)

def create_set_restock_instructions_window(vending_machine, restock_list, management_machine):
    sg.theme('LightGreen')

    column = [
        # list all elements, then list current amount in stock, then field to change amount to be restocked?
        # Slot 1 Current Item: text New item: Drop menu Current Quantity: (0-15)text New Amount: (0-15)spin
        *[[sg.T('Slot {slot_num} Current Item: {current_item} New Item: '.format(slot_num=restock.item_slot, 
                                                                                 current_item="None" if vending_machine.get_slot(restock.item_slot).get_first_item() == None 
                                                                                 else vending_machine.get_slot(restock.item_slot).get_first_item())),
            sg.Drop(values=management_machine.available_items, default_value=vending_machine.get_slot(restock.item_slot).get_first_item(), key='-restock-item-name-{}-'.format(restock.item_slot)),
            sg.T(' Current Quantity: {current_amount} New Amount: '.format(current_amount=len(vending_machine.get_slot(restock.item_slot).list))),
            sg.Spin(values=[i for i in range(16)], initial_value=len(vending_machine.get_slot(restock.item_slot).list), size=(6, 1), key='-restock-new-amount-{}-'.format(restock.item_slot))] for restock in restock_list],
    ]

    layout_set_restock_instructions = [
        # a way for management to set what the restocker should do. Will later influence inventory
        [sg.Column(column, scrollable=True, vertical_scroll_only=True)],
        [sg.Button("Save", key='-save-restock-changes-'), sg.Button("Close")],
    ] # how do we save these changes

    return sg.Window('Set Restock Instructions', layout_set_restock_instructions, finalize=False)

def create_view_status_window(vending_machine):
    sg.theme('LightGreen')

    layout_status = [
        [sg.T('Status of vending machine: {status}'.format(status=vending_machine.get_status()))],
        [sg.Table(
            values=vending_machine.get_errors(),
                  headings=['Error'], # need to add expiration date
                  auto_size_columns=True,
                  display_row_numbers=True,
                  justification='right',
                  # new window or table to show items in item slot
        )],
        [sg.B('Close')],
    ]

    return sg.Window('View Status', layout_status, finalize=False)

def update_restock(restock_machine, values, vending_machine):
    # print(values['-restock-item-name-{}-'.format(1)].get_name() == vending_machine.get_slot(1).get_product_title())
    restock_machine.restock_list = [Restock_Slot(x, values['-restock-item-name-{}-'.format(x)], 
            values['-restock-new-amount-{}-'.format(x)] - len(vending_machine.get_slot(x).list) 
            if values['-restock-item-name-{}-'.format(x)].get_name() == vending_machine.get_slot(x).get_product_title()
            else values['-restock-new-amount-{}-'.format(x)], 
            values['-restock-item-name-{}-'.format(x)].get_name() != vending_machine.get_slot(x).get_product_title()
            ) for x in range(1, 41)] # needs to say to remove items and add new ones if changing items
    # save to restockInstructions csv
    with open("restock_machine_{}.pkl".format(restock_machine.machine_id), "wb") as file: # vending machine #2
        pickle.dump(restock_machine, file)
        file.close()

def run_management(vending_machine : Vending_Machine, restock_machine : Restock, management_machine : Management):
    
    windows = {
        'Manage' : create_management_window()
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
            windows['Purchase History'] = create_purchase_history_window(vending_machine.purchase_history_list)
            previous_window, active_window = 'Manage', 'Purchase History'
        if event == 'set restock instructions': # management window for settting restock instructions
            windows['Manage'].hide()
            windows['Set Restock'] = create_set_restock_instructions_window(vending_machine, restock_machine.restock_list, management_machine)
            previous_window, active_window = 'Manage', 'Set Restock'
        if event == '-save-restock-changes-':
            update_restock(restock_machine, values, vending_machine)
            change_to_previous_window(previous_window, active_window, windows)
            previous_window, active_window = 'Main', 'Manage'
        if event == 'management-view-inventory':
            windows['Manage'].hide()
            windows['View Inventory'] = create_view_inventory_window(vending_machine.item_inventory_list)
            previous_window, active_window = 'Manage', 'View Inventory'
        if event == 'View Status':
            windows['Manage'].hide()
            windows['View Status'] = create_view_status_window(vending_machine)
            previous_window, active_window = 'Manage', 'View Status'
        for slot in vending_machine.item_inventory_list:
            if event == f'show-items-{slot.get_item_slot_num()}':
                # Populate the table with the items from the slot
                item_data = [[item.get_name(), '${:.2f}'.format(item.get_price()), item.get_expiration_date()] for item in slot.list]
                windows['View Inventory']['item-slot-data'].update(values=item_data)
            
    windows['Manage'].close()
