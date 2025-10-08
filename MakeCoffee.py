from data import menu
from data.menu import *
from exception.stock_exception import OutOfStockError
from collections import defaultdict
from logger import logger

# Function to make coffee
'''
    1. Check stock availability
    2. If stock available, make coffee
    3. Update stock
    4. Process payment
    5. Print order summary at the end
    6. Done
'''

# Global variables
order_count = 0
order_summary = {}
total_bill = 0

#work on this to make common function based on coffee item passed
def checkStockAvailability():
    canMake = True   
        #check for stock availability
    for required_item, required_quantity in blackCoffee.items():
        instock_quantity = instock.get(required_item,0) 
        logger(f"{required_item}: Required {required_quantity}, In Stock {instock_quantity}")
        if  required_quantity > instock_quantity:
            canMake = False
            print(f"Stock not enough to make your {required_item}. Please check log file for details.")
            logger(f"\n Need: {required_quantity} and Stock: {instock_quantity}") 
            raise OutOfStockError(f"Not enough {required_item} in stock to make your order.")
    return canMake

def makePayment(menu_item):
    global total_bill
    print("\n**Please proceed to payment**")
    print("Item:", menu_item)
    print("Amount: $", bill[menu_item])
    confirmPayment = input("Confirm payment? (Y/N): ")
    if confirmPayment.lower() != 'y':
        print("Payment not confirmed, order cancelled!")
        return False
    else:
        print("Payment confirmed, preparing your order!")
        total_bill += bill[menu_item]
        logger(f"Total bill so far: ${total_bill:.2f}")
        return True

def makeBlackCoffee(menu_item):
    #check stock availability before making coffee 
    logger("Checking stock availability for " + str(menu_item))
    if checkStockAvailability() == False :
        print("Not enough stock to make your order, please try again later!")
    else:
        for required_item, required_quantity in blackCoffee.items():
            if(instock[required_item] >= required_quantity):
                instock[required_item] -= required_quantity
        logger("Updated stock")
        for item, quantity in instock.items():
            logger(f"{item}: {quantity}")

def makeLatte(menu_item):
        #check stock availability before making coffee 
    logger("Checking stock availability for " + str(menu_item))
    if checkStockAvailability() == False :
        print("Not enough stock to make your order, please try again later!")
    else:
        for required_item, required_quantity in latte.items():
            if(instock[required_item] >= required_quantity):
                instock[required_item] -= required_quantity
        logger("Updated stock")
        for item, quantity in instock.items():
            logger(f"{item}: {quantity}")

def makeCappuccino(menu_item):
    #check stock availability before making coffee 
    logger("Checking stock availability for " + str(menu_item))
    if checkStockAvailability() == False :
        print("Not enough stock to make your order, please try again later!")
    else:
        for required_item, required_quantity in cappuccino.items():
            if(instock[required_item] >= required_quantity):
                instock[required_item] -= required_quantity
        logger("Updated stock")
        for item, quantity in instock.items():
            logger(f"{item}: {quantity}")

def showMenu():
    print("\n**Welcome to the Coffee Bot**\nChoose from 1-3 to order:\nType 'exit' to cancel:")
    print("\n----- Menu -----")
    for order_id, (item, price) in enumerate(bill.items(), start=1):
        print(f"{order_id}. {item} - ${price:.2f}")
    print("----------------")
    return input("\n> ")

    
def main():
    choice = None
    global order_count
    global order_summary
        
    order_summary = defaultdict(int)

    while choice != "exit":

        choice = showMenu()
        try:
            if choice == "1":
                makeBlackCoffee(menu.item[0])
                if makePayment(menu.item[0]):
                    order_count += 1
                    order_summary[menu.item[0]] += 1
            elif choice == "2":
                makeLatte(menu.item[1])
                if makePayment(menu.item[1]):
                    order_count += 1
                    order_summary[menu.item[1]] += 1
            elif choice == "3":
                makeCappuccino(menu.item[2])
                if makePayment(menu.item[2]):
                    order_count += 1
                    order_summary[menu.item[2]] += 1
            elif choice == "exit":
                if order_count == 0:
                    print("You did not place any order. Thank you and visit again!")
                else:
                    print("\n----- Order Summary -----")
                    for item, qty in order_summary.items():
                        print(f"{item}: {qty} x ${bill[item]} = ${qty * bill[item]}")
                    print(f"Total items: {order_count}")
                    print(f"Total bill: ${total_bill}")
                    print("----------------")

                break
            else:
                print("Oops! Incorrect choice. Please try again.")
        except OutOfStockError as e:
            logger(f"Order could not be completed: {e}")

#Function call to run project
main()
