import pickle as pickle


class Vending_Machine:

    def __init__(self, row, column, status, item_inventory_list, machine_id ) -> None: # Has the Properties of the vending machine
        self.row = row
        self.column = column
        self.status = status
        self.item_inventory_list = item_inventory_list
        self.machine_id = machine_id
    
    def vending_machine_layout(self, row, column, item_inventory_list): # here we will define the dimensions (layout) of a vending machine
        self.column = column
        self.row = row
        self.item_inventory_list = item_inventory_list

        item_inventory_list = [] # empty list
        vending_machine_inventory = item_inventory_list

    def get_vending_machine_layout(self, column, row, item_inventory_list): # returns the vending machine layout
        return self.column, self.row, item_inventory_list

    def get_status(self): # returns the current status of the vending machine
        return self.status

class Item:
    def __init__(self, item_slot, price, name, expiration_date) -> None:
        self.item_slot = item_slot
        self.price = price
        self.name = name
        self.expiration_date = expiration_date

class Restock: # restock tool
    def __init__(self, ) -> None:
        pass

class Management: # management tool
    def __init__(self) -> None:
        pass


def main(): # below are 2 vending machine objects defined with different layout dimensions

    vending_machine_layout_1 = Vending_Machine.vending_machine_layout(8,15) # sets the dimension layout as 8x15
    Vending_Machine.get_vending_machine_layout(vending_machine_layout_1) # returns the dimension of the 1st vending machine
    vending_machine_layout_2 = Vending_Machine.vending_machine_layout(4,4) # sets the layout as 4x4
    Vending_Machine.get_vending_machine_layout(vending_machine_layout_2) # returns the dimension of the 2nd vending machine
