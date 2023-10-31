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

# def main(): # below are 2 vending machine objects defined with different layout dimensions
#     vending_machine_inventory = pd.read_csv("database\\VendingMachine1.csv")
#     df_itemTable = pd.read_csv("database\\ItemTable.csv", index_col=0, header=0)
    
#     vending_machine_1_slots = []
#     for items in vending_machine_inventory.values.tolist():
#         print(items)
#         item_list = [Item(items[0], df_itemTable.loc[items[1]]["item cost"], df_itemTable.loc[items[1]]["item name"], "11/01/23") for x in range(items[2])]
#         vending_machine_1_slots.append(ItemSlot(item_list))
#     # Creating vending machine objects
#     vending_machine_1 = Vending_Machine(8, 5, "active", 
#     vending_machine_1_slots, "69")
#    # vending_machine_2 = Vending_Machine(4, 4, "active", 
#    # ["A1", "A2", "A3", "A4",
#    # "B1", "B2", "B3", "B4",
#    # "C1", "C2", "C3", "C4",
#    # "D1", "D2", "D3", "D4",], "42")

#     # Saving vending machine objects using pickle
#     with open("vending_machine_1.pkl", "wb") as file: # vending machine #1
#         pickle.dump(vending_machine_1, file)
#         file.close()

#     # with open("vending_machine_2.pkl", "wb") as file: # vending machine #2
#     #     pickle.dump(vending_machine_2, file)

#     # Loading vending machine objects from pickle files
#     with open("vending_machine_1.pkl", "rb") as file:
#         loaded_vending_machine_1 = pickle.load(file)
#         print("Loaded Vending Machine 1 layout:", loaded_vending_machine_1.row, "x", loaded_vending_machine_1.column)
#         print("Loaded Vending Machine 1 ID:", loaded_vending_machine_1.get_vending_machine_id())

#     # with open("vending_machine_2.pkl", "rb") as file:
#     #     loaded_vending_machine_2 = pickle.load(file)
#     #     print("Loaded Vending Machine 2 layout:", loaded_vending_machine_2.row, "x", loaded_vending_machine_2.column)
#     #     print("Loaded Vending Machine 2 ID:", loaded_vending_machine_2.get_vending_machine_id())

# if __name__ == "__main__":
#     main()
