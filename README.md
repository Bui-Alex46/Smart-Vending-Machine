 Smart-Vending-Machine
Release 2
Group 3 Members:
* KEILLOR J
* KARLA R
* ALEX R
* ALEX B 
* JACK T

This project simulates the systems for a smart vending, and contains three sections. 
Section 1 contains the system for the vending machine itself where a customer can go, and buy snacks that are listed. To simulate money we incorporate buttons the user can add to their balance in order to perform transactions for testing. Section 2 is the system of the "Restock Tool" where the user can refill the inventory for the vending machine, based on the instruction that section is sent from the Management Tool (Section 3). Section 3 is the Management Tool, this system will manage the vending machine, and push restocks based on the current inventory, this system can also view the inventory of the vending machine at any time, and also view the purchase history for the vending machine.

Installation instructions: 
Extract all files into a folder. To run the main.py program you need to have Python 3 installed and included on the path. Also the library pysimplegui has to be installed.

Disclaimers:
As this is only release 2 there are some minor not super impactful bugs that exist. Such as when you set restock instructions we include every slot as instruction even if nothing is changed. The setup in management for making these restock instructions isn’t visually pleasant. 

Missing features:
When you attempt to submit a restock that isn’t valid, the submit button doesn’t do anything when it should be giving you an error message saying it's not valid.
Maybe this could be a source for the errors which currently don’t have any way to get any errors. 
Layouts were never really implemented, but was a concept that was looked into. The current version has no way to set up a layout or do anything with them. 
There is no actual checking for expired products and we don't give any suggestions when creating restock instructions to do so. 
It is complicated to be able to manage the inventory and create instructions because you can only view one window at a time.
When creating restock instructions there is supposed to be a confirmation window detailing the changes you are making. 

Instructions to run program:
There are no passwords at this time. Was not an important feature, but could be implemented for Release 3. The management and restock instructions would need a way to set up passwords. Close button is on almost every window and allows you to go back a window. In the vending machine, you select the item you want to buy and then click the monetary buttons to represent inserting money.
