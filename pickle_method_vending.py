import pickle
import pandas as pd

class Vending_Machine:

    def __init__(self, row, column, status, item_inventory_list, machine_id) -> None: # Has the Properties of the vending machine
        self.row = row
        self.column = column
        self.status = status
        self.item_inventory_list = item_inventory_list
        self.machine_id = machine_id
        
    
    def set_vending_machine_layout(self, row, column, item_inventory_list): # here we will define the dimensions (layout) of a vending machine
        self.column = column
        self.row = row
        self.item_inventory_list = item_inventory_list


    def get_vending_machine_layout(self, column, row, item_inventory_list): # returns the vending machine layout
        return self.column, self.row, item_inventory_list
    
    def set_status(self, status): # pass a status string to a vending machine
        self.status = status

    def get_status(self): # returns the current status of the vending machine
        return self.status

    def set_vending_machine_id(self, machine_id): # pass string to set the vending machine id
        self.machine_id = machine_id
    
    def get_vending_machine_id(self):
        return self.machine_id
## END of Vending Machine Class


class Item:
    def __init__(self, item_slot, price, item_name, expiration_date) -> None:
        self.item_slot = item_slot
        self.price = price
        self.item_name = item_name
        self.expiration_date = expiration_date

## END of Item Class
class Restock: # restock tool
    def __init__(self, item_slot, item_name, expiration_date, machine_id ) -> None:
        self.item_slot = item_slot
        self.item_name = item_name
        self.expiration_date = expiration_date
        self.machine_id = machine_id

## END of Restock class

class Management: # management tool
    def __init__(self, machine_id, row, column) -> None:
        pass

## END of Management Class

class ItemSlot:
    def __init__(self, list) -> None:
        self.list = list
