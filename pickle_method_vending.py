from datetime import datetime, date, timedelta
import pickle

class Vending_Machine:
    vending_machine_layout = []

    def __init__(self, num_rows, num_columns, status, item_inventory_list, purchase_history_list, machine_id, errors_list) -> None: # Has the Properties of the vending machine
        self.num_rows = num_rows
        self.num_columns = num_columns
        self.status = status
        self.item_inventory_list = item_inventory_list
        self.purchase_history_list = purchase_history_list
        self.machine_id = machine_id
        self.errors_list = errors_list
    
    def set_vending_machine_layout(self, item_inventory_list): # here we will define the dimensions (layout) of a vending machine
        # needs to be at least one item in inventory for there to be an item in layout
        self.vending_machine_layout = ['out of stock' if len(slot.list) == 0 else slot.list[0]
                                    for slot in item_inventory_list]

    def get_vending_machine_layout(self): # returns the vending machine layout
        return self.vending_machine_layout
    
    def set_status(self, status): # pass a status string to a vending machine
        self.status = status

    def get_status(self): # returns the current status of the vending machine
        return self.status

    def set_vending_machine_id(self, machine_id): # pass string to set the vending machine id
        self.machine_id = machine_id
    
    def get_vending_machine_id(self):
        return self.machine_id
    
    def get_slot(self, slot_num):
        return self.item_inventory_list[slot_num - 1]
    
    def get_errors(self):
        return self.errors_list
    
    def process_purchase(self, item_slot):
        self.purchase_history_list.append(Purchase_History(item_slot.list[0], datetime.now()))
        self.get_slot(item_slot.get_item_slot_num()).list.pop(0)
        
    def restock_machine(self, restock_changes): # not sure if this is going to be 
        # print(not (restock_changes[0].remove_current_items))
        for x in range(len(restock_changes)):
            if not (restock_changes[x].remove_current_items): # adjust current items. how do we deal with expiration dates
                if restock_changes[x].number_to_add < 0:
                    self.item_inventory_list[x].replace_list(self.get_slot(x + 1).list[abs(restock_changes[x].number_to_add):])
                    # print("Remove items")
                if restock_changes[x].number_to_add > 0:
                    new_item = self.get_slot(x + 1).get_first_item()
                    new_items = [Item(new_item.price, new_item.item_name, new_item.expiration_days) for i in range(restock_changes[x].number_to_add)]
                    [item.set_expiration_date() for item in new_items]
                    # print(len(new_items))
                    # print(new_items[0].expiration_date)
                    self.item_inventory_list[x].list.extend(new_items)
            else: # replace all items with new ones
                # print("Replace items")
                new_item = restock_changes[x].change_to_item
                new_items = [Item(new_item.price, new_item.item_name, new_item.expiration_days) for i in range(restock_changes[x].number_to_add)]
                [item.set_expiration_date() for item in new_items]
                self.item_inventory_list[x].replace_list(new_items)
                self.item_inventory_list[x].product_title = restock_changes[x].change_to_item.get_name()
## END of Vending Machine Class

class ItemSlot:
    # previous_item = '' # trying to think of a way to save item layout more efficiently
    # what do we need for layout. just the name or an item object
    
    def __init__(self, list, item_slot_num, product_title) -> None:
        self.list = list
        self.item_slot_num = item_slot_num
        self.product_title = product_title
        
    def get_first_item(self):
        return None if len(self.list) == 0 else self.list[0]
    
    def get_item_slot_num(self) -> int:
        return self.item_slot_num
    
    def get_product_title(self):
        return self.product_title
    
    def set_product_title(self, title):
        self.product_title = title
        
    def replace_list(self, new_list):
        self.list = new_list


class Item:
    expiration_date : date
    
    def __init__(self, price, item_name, expiration_days) -> None:
        self.price = price
        self.item_name = item_name
        self.expiration_days = expiration_days
        
    def get_name(self):
        return self.item_name
    
    def get_price(self):
        return self.price
    
    def set_expiration_date(self):
        self.expiration_date = date.today() + timedelta(days=self.expiration_days)
        
    def get_expiration_date(self):
        return self.expiration_date
        
    def __str__(self) -> str:
        return self.get_name()

## END of Item Class
class Restock_Slot: # restock tool
    def __init__(self, item_slot, change_to_item, number_to_add, remove_current_items) -> None: # need a way to create new item / set new expiration date
        self.item_slot = item_slot # number for now
        self.change_to_item = change_to_item # Item class
        self.number_to_add = number_to_add # if not changing item adding more, 
        self.remove_current_items = remove_current_items # if you want to take out current items replace with new stuff
        # if changing taking everything else out and putting in this number

## END of Restock class

class Restock:
    def __init__(self, restock_list, machine_id) -> None:
        self.restock_list = restock_list # list of Restock_Slot objects
        self.machine_id = machine_id

# def redefine_restock_machine_1(restock_machine):
#     restock_machine = Restock([Restock_Slot], 1)

#     with open("restock_machine_1.pkl", "wb") as file: # vending machine #1
#         pickle.dump(restock_machine_1, file)
#         file.close()


class Management: # management tool
    def __init__(self, available_items) -> None:
        self.available_items = available_items

## END of Management Class

class Purchase_History:
    def __init__(self, item, date_time_of_transaction):
        self.item = item
        self.date_time_of_transaction = date_time_of_transaction

### modifying / redefining Vending_Machine object
def redefine_vending_machine_1(vending_machine):
    vending_machine_1_slots = []
    for item_slot in vending_machine.item_inventory_list:
        item_list = [Item(item_slot.list[0].price, item_slot.list[0].item_name, item_slot.list[0].expiration_days) for x in range(len(item_slot.list))]
        [item.set_expiration_date() for item in item_list]
        vending_machine_1_slots.append(ItemSlot(item_list, item_slot.item_slot_num, item_list[0].get_name()))
    # Creating vending machine objects
    vending_machine_1 = Vending_Machine(8, 5, "active", 
    vending_machine_1_slots, vending_machine.purchase_history_list, machine_id="1", errors_list=[])

    with open("vending_machine_1.pkl", "wb") as file: # vending machine #1
        pickle.dump(vending_machine_1, file)
        file.close()

