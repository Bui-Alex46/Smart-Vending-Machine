import PySimpleGUI as sg
import pickle

from pickle_method_vending import Restock, Restock_Slot, Vending_Machine

def create_restock_window(restock_machine):
    sg.theme('LightGreen')

    if len(restock_machine.restock_list) == 0: # print there are no instructions
        layout_no_restock = [
            [sg.T('RESTOCKING')],
            [sg.T('No changes to be made.')],
            [sg.B('Close')]
        ]
        return sg.Window('Restock', layout_no_restock)
    else:
        column = [
            *[[sg.T('Item slot: {item_slot} Item name: {item_name} {replace_instructions}: {num_in_slot}'.format(
                item_slot=restock.item_slot, 
                replace_instructions=(
                    "Replace all with" if restock.remove_current_items else
                    "Add to machine" if restock.number_to_add >= 0 else
                    "Remove from machine"
                ),
                item_name=restock.change_to_item,
                num_in_slot=restock.number_to_add
                ), pad=(0, 0))]
            for restock in restock_machine.restock_list], # also need a way to deal with expired items
        ]
        layout_restock = [
            [sg.T('RESTOCKING')], # table is probably better
            [sg.Column(column, scrollable=True, vertical_scroll_only=True)],
            [sg.Submit(key='-submit-restock-'), sg.B('Cancel')]
        ]
        return sg.Window('Restock', layout_restock) #, resizable=True) #, finalize=True)
    
def restock_is_valid(restock_list, vending_machine):
    for restock in restock_list:
        new_amount = len(vending_machine.get_slot(restock.item_slot).list) + restock.number_to_add
        if new_amount > 15 or new_amount < 0:
            return False
    return True

def run_restock(restock_machine : Restock, vending_machine : Vending_Machine):
    restock_window = create_restock_window(restock_machine)
    
    while True:
        event, values = restock_window.read()
        if event in (None, 'Exit', 'Close', 'Cancel'):
            break
        if event == '-submit-restock-': # changes inventory after restock
            if restock_is_valid(restock_machine.restock_list, vending_machine):
                vending_machine.restock_machine(restock_machine.restock_list)
                with open("vending_machine_{}.pkl".format(vending_machine.get_vending_machine_id()), "wb") as file:
                    pickle.dump(vending_machine, file)
                    file.close()
                break
            
    restock_window.close()
